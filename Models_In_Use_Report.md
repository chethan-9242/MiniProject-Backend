### Models in use: algorithm, accuracy, status, improvements

| Name | Algorithm/Technology | Reported Accuracy | In Use Now | Status | Needs Improvement |
|---|---|---:|---|---|---|
| Symptom Analysis | Flan‑T5 Large + RAG | 75–85% | Yes | Production Ready | Domain fine‑tuning; continuous eval/monitoring |
| Dosha Analysis (AI) | Flan‑T5 Large + Ayurvedic KB | 80–85% | Yes | Active | Expand KB; prompt tuning; human evals |
| Chatbot & Recommendations | Flan‑T5 Large + RAG | 85–90% | Yes | Active | Add citations/grounding; safety/guardrails; latency tuning |
| Skin Analysis (AI) | Flan‑T5 Large + Vision context | 70–80% | Yes | Active | Add vision embeddings; curated eval set |
| Hair Analysis (AI, enhanced) | Flan‑T5 Large + RAG | 75–80% | Yes | Active | Enrich domain KB; compare vs CV outputs; guardrails |
| RAG Retrieval (supporting) | SentenceTransformers + ChromaDB (TF‑IDF fallback) | 90%+ retrieval precision | Yes | Active | KB hygiene/versioning; retrieval eval harness |
| Knowledge Base (supporting) | Vector DB + pattern matching | 95%+ information accuracy | Yes | Active | Provenance, QA, citation linking |
| Hair Analysis (CV) | ResNet50 CNN | TBD | Conditional (when weights ready) | In Development | Complete training/validation; calibration |
| Skin Disease Detection (CV) | Deep CNN (ResNet18/50 variants) | TBD | Not yet (mock currently) | In Development | Train/evaluate; replace mock; class mapping QA |


