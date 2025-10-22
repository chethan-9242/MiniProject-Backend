# SwasthVedha Backend Docker Container
# This file tells Docker how to build your app

# Use Python 3.9 as base (like a starting template)
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Install additional packages for AI models
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy your entire backend code
COPY . .

# Create directories for models and data
RUN mkdir -p models data uploads

# Expose port 8000 (where your FastAPI runs)
EXPOSE 8000

# Health check to ensure container is working
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Command to run when container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]