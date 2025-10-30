# Colab script: Flan-T5 (Google) + GraphRAG (ChromaDB) LoRA training and inference
# How to use in Google Colab:
# 1) Open Colab -> File -> Upload this file, then run all cells (Runtime -> Run all)
# 2) Optionally upload your JSONL dataset when prompted (input/output pairs). If you skip, a small demo dataset is used.
# 3) After training finishes, download the LoRA adapter zip and place it into backend/models/flan_t5_dosha_lora on your machine.
# 4) Backend will auto-load the adapter; recommendations will be personalized and vary per input. GraphRAG retrieval is used at inference.

import os, json, random, shutil, zipfile, io
from typing import Dict, List

# Install dependencies (Colab-safe)
import sys
if 'google.colab' in sys.modules:
    !pip -q install "transformers>=4.44.0" datasets peft accelerate sentencepiece \
        "chromadb>=0.5.0" "sentence-transformers>=3.0.1"

import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model, PeftModel, prepare_model_for_kbit_training

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# -------------------------------
# Configuration
# -------------------------------
BASE_MODEL = os.getenv("BASE_MODEL", "google/flan-t5-small")
ADAPTER_OUT_DIR = os.getenv("ADAPTER_OUT_DIR", "/content/flan_t5_dosha_lora")
DB_DIR = os.getenv("CHROMA_DIR", "/content/chroma_db")
SEED = 42
MAX_SOURCE_LEN = 512
MAX_TARGET_LEN = 256

random.seed(SEED)
torch.manual_seed(SEED)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# -------------------------------
# Ayurvedic Knowledge Base (for GraphRAG)
# -------------------------------
AYURVEDA_KNOWLEDGE: List[Dict] = [
    {"id": "dosha_vata", "category": "Doshas", "title": "Vata Dosha Characteristics",
     "content": "Vata governs movement, circulation, breathing, and nerve impulses. Imbalance -> anxiety, dry skin, constipation.",
     "metadata": {"type": "constitution", "dosha": "vata"}},
    {"id": "dosha_pitta", "category": "Doshas", "title": "Pitta Dosha Characteristics",
     "content": "Pitta governs digestion, metabolism, temperature. Imbalance -> inflammation, anger, heartburn, skin issues.",
     "metadata": {"type": "constitution", "dosha": "pitta"}},
    {"id": "dosha_kapha", "category": "Doshas", "title": "Kapha Dosha Characteristics",
     "content": "Kapha governs structure, lubrication, stability. Imbalance -> weight gain, lethargy, congestion.",
     "metadata": {"type": "constitution", "dosha": "kapha"}},
    {"id": "herb_ashwagandha", "category": "Herbs", "title": "Ashwagandha",
     "content": "Adaptogen: reduces stress/anxiety, improves sleep and cognition. Balances Vata/Kapha.",
     "metadata": {"type": "herb"}},
    {"id": "herb_turmeric", "category": "Herbs", "title": "Turmeric",
     "content": "Anti-inflammatory/antioxidant; supports skin, joints, liver. Works across doshas.",
     "metadata": {"type": "herb"}},
    {"id": "treatment_skin_pitta", "category": "Treatments", "title": "Pitta Skin Treatment",
     "content": "Cooling herbs (neem, aloe), avoid hot/spicy/acidic foods, use coconut oil, cooling foods.",
     "metadata": {"type": "treatment", "dosha": "pitta", "condition": "skin"}},
    {"id": "diet_vata", "category": "Diet", "title": "Vata Diet",
     "content": "Warm, moist, grounding foods; ghee; root vegetables; sweet/sour/salty tastes; avoid cold/dry.",
     "metadata": {"type": "diet", "dosha": "vata"}},
    {"id": "diet_pitta", "category": "Diet", "title": "Pitta Diet",
     "content": "Cool, hydrating, mildly spiced; coconut, cucumber; avoid hot/fried/acidic foods.",
     "metadata": {"type": "diet", "dosha": "pitta"}},
    {"id": "diet_kapha", "category": "Diet", "title": "Kapha Diet",
     "content": "Light, warm, stimulating; pungent/bitter/astringent; reduce heavy/oily/sweet.",
     "metadata": {"type": "diet", "dosha": "kapha"}},
    {"id": "practice_abhyanga", "category": "Practices", "title": "Abhyanga",
     "content": "Daily self-massage: sesame oil (Vata), coconut (Pitta), mustard/sunflower (Kapha).",
     "metadata": {"type": "practice"}},
]

# -------------------------------
# Build ChromaDB
# -------------------------------
def init_chromadb(persist_dir: str = DB_DIR):
    os.makedirs(persist_dir, exist_ok=True)
    client = chromadb.Client(Settings(persist_directory=persist_dir, anonymized_telemetry=False))
    try:
        collection = client.get_collection("ayurveda_knowledge")
    except Exception:
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        collection = client.create_collection(name="ayurveda_knowledge", embedding_function=ef,
                                              metadata={"description": "Ayurveda KB for RAG"})
        collection.add(
            documents=[d["content"] for d in AYURVEDA_KNOWLEDGE],
            metadatas=[d["metadata"] for d in AYURVEDA_KNOWLEDGE],
            ids=[d["id"] for d in AYURVEDA_KNOWLEDGE],
        )
    return client, collection

client, collection = init_chromadb()
print(f"ChromaDB initialized. Docs: {collection.count()}")

# -------------------------------
# Dataset handling
# -------------------------------
DEMO_DATA = [
    {
        "input": "Dosha: Vata\nSymptoms: anxiety, dry skin, constipation\nContext: adult, moderate",
        "output": "Health:\n- Maintain warm routine and regular schedule.\nDiet:\n- Warm, moist foods with ghee.\nLifestyle:\n- Abhyanga with sesame oil.\nWarnings:\n- If constipation persists > 2 weeks, consult doctor.",
    },
    {
        "input": "Dosha: Pitta\nSymptoms: rash, burning sensation, irritability\nContext: adult, mild",
        "output": "Health:\n- Reduce heat and stress.\nDiet:\n- Cooling foods (cucumber, coconut).\nLifestyle:\n- Avoid midday sun; use aloe.\nWarnings:\n- If rash spreads rapidly, seek care.",
    },
    {
        "input": "Dosha: Kapha\nSymptoms: fatigue, congestion, weight gain\nContext: adult, mild",
        "output": "Health:\n- Daily vigorous exercise.\nDiet:\n- Light, warm, pungent foods.\nLifestyle:\n- Wake up before 6 AM.\nWarnings:\n- If breathlessness or edema, consult physician.",
    },
]

def load_jsonl_to_dataset(path: str) -> Dataset:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            rows.append({"input": obj["input"], "target": obj["output"]})
    return Dataset.from_list(rows)

# In Colab, allow upload (optional)
if 'google.colab' in sys.modules:
    from google.colab import files
    print("Optional: Upload your JSONL dataset now (with fields: input, output). Or skip to use demo dataset.")
    uploaded = files.upload()
    if uploaded:
        fname = list(uploaded.keys())[0]
        ds = load_jsonl_to_dataset(fname)
    else:
        ds = Dataset.from_list(DEMO_DATA)
else:
    ds = Dataset.from_list(DEMO_DATA)

# Prepare train/val
ds = ds.map(lambda ex: {"input_text": (
    "You are an Ayurvedic assistant. Generate concise, specific, non-repetitive recommendations.\n"
    "Return sections: Health, Diet, Lifestyle, Warnings.\n\n"
    f"{ex['input']}\n\nAnswer:"),
    "labels": ex["target"]
})

split = ds.train_test_split(test_size=0.1, seed=SEED)
train_ds, val_ds = split["train"], split["test"]

# Tokenizer/model
print("Loading base model:", BASE_MODEL)
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
base = AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL)
base = prepare_model_for_kbit_training(base)

# LoRA config
lora_cfg = LoraConfig(
    r=16, lora_alpha=32, target_modules=["q", "k", "v", "o"],
    lora_dropout=0.05, bias="none", task_type="SEQ_2_SEQ_LM"
)
model = get_peft_model(base, lora_cfg)
model = model.to(device)

# Tokenization

def tokenize_batch(batch):
    model_inputs = tokenizer(batch["input_text"], max_length=MAX_SOURCE_LEN, truncation=True)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(batch["labels"], max_length=MAX_TARGET_LEN, truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)
train_tok = train_ds.map(tokenize_batch, batched=True, remove_columns=train_ds.column_names)
val_tok = val_ds.map(tokenize_batch, batched=True, remove_columns=val_ds.column_names)

# Training
args = TrainingArguments(
    output_dir=ADAPTER_OUT_DIR,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    gradient_accumulation_steps=2,
    learning_rate=2e-4,
    num_train_epochs=3,
    eval_strategy="steps",
    logging_steps=50,
    eval_steps=200,
    save_steps=200,
    save_total_limit=2,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    weight_decay=0.01,
    bf16=torch.cuda.is_available(),
    fp16=not torch.cuda.is_available(),
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_tok,
    eval_dataset=val_tok,
    tokenizer=tokenizer,
    data_collator=collator,
)

print("Starting LoRA training...")
trainer.train()

os.makedirs(ADAPTER_OUT_DIR, exist_ok=True)
model.save_pretrained(ADAPTER_OUT_DIR)
tokenizer.save_pretrained(ADAPTER_OUT_DIR)
print(f"Saved LoRA adapter to: {ADAPTER_OUT_DIR}")

# -------------------------------
# GraphRAG Inference: retrieve + generate
# -------------------------------

def retrieve_context(query: str, n_results: int = 5) -> List[str]:
    res = collection.query(query_texts=[query], n_results=n_results)
    docs = res.get("documents", [[]])[0]
    return docs or []

@torch.no_grad()
def generate_with_rag(user_input: str, max_len: int = 280) -> str:
    # Build retrieval query from user_input
    retrieved = retrieve_context(user_input, n_results=5)
    context = "\n\n".join([f"Source {i+1}: {d}" for i, d in enumerate(retrieved)])
    prompt = (
        "Based on the following Ayurvedic knowledge, generate concise, specific recommendations.\n"
        "Return sections: Health, Diet, Lifestyle, Warnings.\n\n"
        f"Context:\n{context}\n\nInput:\n{user_input}\n\nAnswer:"
    )
    inputs = tokenizer(prompt, return_tensors="pt", max_length=MAX_SOURCE_LEN, truncation=True).to(device)
    out = model.generate(
        **inputs,
        max_length=max_len, min_length=80,
        num_beams=5, early_stopping=True,
        temperature=0.9, do_sample=True,
        top_k=60, top_p=0.92,
        repetition_penalty=1.25, no_repeat_ngram_size=3,
    )
    return tokenizer.decode(out[0], skip_special_tokens=True)

# Demo inference
print("\nDemo inference with RAG:")
demo_input = "Dosha: Vata-Pitta\nSymptoms: bloating, anxiety\nContext: adult, moderate severity"
print(generate_with_rag(demo_input))

# -------------------------------
# Pack adapter for download
# -------------------------------
if 'google.colab' in sys.modules:
    zip_path = "/content/flan_t5_dosha_lora.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(ADAPTER_OUT_DIR):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, ADAPTER_OUT_DIR)
                zf.write(full, arcname=os.path.join("flan_t5_dosha_lora", rel))
    print(f"Adapter zipped at: {zip_path} (download from Colab files pane)")

print("\nDone. Upload flan_t5_dosha_lora to backend/models/ and restart the backend.")
