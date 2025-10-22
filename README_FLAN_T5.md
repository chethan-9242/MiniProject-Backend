# Google Flan-T5 Large Integration for SwasthVedha

This document explains how to use the Google Flan-T5 Large model integration in your SwasthVedha healthcare chatbot.

## Overview

The integration replaces the previous rule-based chatbot with Google's Flan-T5 Large model, providing more intelligent and contextual responses for Ayurvedic healthcare queries.

## Setup Instructions

### 1. Install Dependencies

First, install the new dependencies:

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit the `.env` file with your preferences:

```env
# Flan-T5 Model Configuration
FLAN_T5_MODEL_NAME=google/flan-t5-large
FLAN_T5_DEVICE=auto  # Options: auto, cuda, cpu
FLAN_T5_MAX_LENGTH=512
FLAN_T5_TEMPERATURE=0.7
FLAN_T5_CACHE_DIR=./models/cache

# Model Performance Settings
FLAN_T5_LOW_CPU_MEM_USAGE=true
FLAN_T5_TORCH_DTYPE=float16  # Options: float16, float32
FLAN_T5_USE_CACHE=true
```

### 3. Start the Server

Start your FastAPI server:

```bash
py main.py
```

The model will automatically download and load when first accessed (this may take a few minutes).

## API Endpoints

### Chat Message
- **POST** `/api/chat/message`
- Process healthcare queries using Flan-T5

### Model Status
- **GET** `/api/chat/model-status`
- Check if the model is loaded and get model information

### Reload Model
- **POST** `/api/chat/reload-model`
- Reload the model (useful for troubleshooting)

### Configuration Validation
- **GET** `/config/validate`
- Validate environment configuration

## Model Variants

You can use different Flan-T5 model sizes by changing the `FLAN_T5_MODEL_NAME` in your `.env` file:

- `google/flan-t5-small` (80M parameters) - Fastest, least memory
- `google/flan-t5-base` (250M parameters) - Good balance
- `google/flan-t5-large` (780M parameters) - Better quality (default)
- `google/flan-t5-xl` (3B parameters) - Best quality, more resources needed
- `google/flan-t5-xxl` (11B parameters) - Requires powerful hardware

## Fine-tuning (Optional)

### Why Fine-tune?

Fine-tuning can improve the model's performance on Ayurvedic healthcare topics by training it on domain-specific data.

### Running Fine-tuning

1. **Prepare your training data** (optional):
   Create a JSON file with your training examples:
   ```json
   [
     {
       "input": "What are the benefits of turmeric in Ayurveda?",
       "target": "Turmeric is highly valued in Ayurveda for its anti-inflammatory, antimicrobial, and antioxidant properties..."
     }
   ]
   ```
   
   Save it as `./data/training/ayurvedic_qa.json`

2. **Run the fine-tuning script**:
   ```bash
   py scripts/fine_tune_flan_t5.py
   ```

3. **Update your configuration** to use the fine-tuned model:
   ```env
   FLAN_T5_MODEL_NAME=./models/fine_tuned/flan-t5-ayurveda
   ```

### Fine-tuning Configuration

You can modify fine-tuning parameters in the script:

- `num_train_epochs`: Number of training epochs (default: 3)
- `learning_rate`: Learning rate (default: 5e-5)
- `per_device_train_batch_size`: Batch size per device (default: 4 for GPU, 2 for CPU)

## Performance Optimization

### For CPU-only systems:
```env
FLAN_T5_DEVICE=cpu
FLAN_T5_TORCH_DTYPE=float32
```

### For GPU systems:
```env
FLAN_T5_DEVICE=cuda
FLAN_T5_TORCH_DTYPE=float16
```

### Memory optimization:
```env
FLAN_T5_LOW_CPU_MEM_USAGE=true
```

## Troubleshooting

### Common Issues

1. **Out of Memory Error**:
   - Try a smaller model variant (flan-t5-base or flan-t5-small)
   - Reduce batch size in fine-tuning
   - Use CPU instead of GPU

2. **Slow Response Times**:
   - Use GPU if available
   - Try flan-t5-base for faster inference
   - Enable caching

3. **Model Not Loading**:
   - Check internet connection for first download
   - Verify cache directory permissions
   - Check the configuration validation endpoint

### Debug Endpoints

- Check model status: `GET /api/chat/model-status`
- Validate configuration: `GET /config/validate`
- Reload model: `POST /api/chat/reload-model`

## Model Information

- **Model Type**: Google Flan-T5 (Text-to-Text Transfer Transformer)
- **Architecture**: Encoder-Decoder Transformer
- **Training**: Instruction-tuned on diverse tasks
- **Context Window**: 512 tokens
- **Languages**: Primarily English, with some multilingual capabilities

## Integration Details

The integration includes:

1. **FlanT5Service**: Core service class for model management
2. **Configuration Management**: Environment-based configuration
3. **Caching**: Model and response caching
4. **Error Handling**: Graceful fallback for errors
5. **Monitoring**: Model status and health checks

## Best Practices

1. **Prompt Engineering**: The system automatically adds Ayurvedic context to prompts
2. **Response Filtering**: Automatic disclaimer addition for health-related responses
3. **Caching**: Enable caching for better performance
4. **Resource Management**: Monitor GPU memory usage
5. **Regular Updates**: Keep transformers library updated

## Support

For issues or questions:

1. Check the configuration validation endpoint
2. Review the logs for error details
3. Try the reload model endpoint
4. Verify your environment configuration

## License

This integration uses the Transformers library and Google's Flan-T5 models. Please check their respective licenses for usage terms.