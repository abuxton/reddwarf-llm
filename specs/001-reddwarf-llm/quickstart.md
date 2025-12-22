# Red Dwarf Tiny LLM - Quickstart Guide

**Welcome aboard Red Dwarf!** This guide will get you up and running with Holly's brain—er, the tiny LLM—faster than Lister can say "vindaloo."

---

## Prerequisites

- **Python 3.10+** (Holly's upgraded software requires modern infrastructure)
- **8GB RAM minimum** (4GB+ VRAM recommended for GPU acceleration)
- **15GB free disk space** (for model weights and cache)
- **VS Code with Dev Containers extension** (for devcontainer development)
- **Docker and Docker Compose** (for containerized deployment)
- **CUDA toolkit** (NVIDIA GPUs, Linux) or **Metal support** (Apple Silicon, macOS)

---

## Option 1: Devcontainer Development (Recommended for Contributors)

### 1. Clone the Repository

```bash
git clone https://github.com/abuxton/reddwarf-llm.git
cd reddwarf-llm
```

### 2. Open in VS Code with Devcontainer

```bash
code .
```

When prompted, click **"Reopen in Container"** or run:
- `Cmd+Shift+P` (macOS) / `Ctrl+Shift+P` (Linux/Windows)
- Select: **"Dev Containers: Reopen in Container"**

The devcontainer will:
- Build Python 3.10+ environment
- Install all dependencies (`pip install -e '.[dev]'`)
- Configure GPU passthrough (if available)
- Set up pre-commit hooks (black, mypy, ruff)

**Note**: GPU passthrough only works on Linux with `nvidia-container-toolkit`. macOS users will use CPU inference (slower but functional).

### 3. Download Models

Inside the devcontainer terminal:

```bash
make download-models
```

This downloads TinyLlama-1.1B and Phi-2 models to `data/models/` (~2-3GB total).

### 4. Run Tests

```bash
make test
```

You should see tests pass with Red Dwarf-themed output:

```
tests/unit/test_quote_selector.py::test_no_repeat_within_session PASSED [Holly] No repeat quotes detected
tests/integration/test_end_to_end.py::test_lister_curry_scenario PASSED [Lister] Vindaloo mentioned: ✓
```

### 5. Start the API Server

```bash
make run
```

Server starts at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

### 6. Test Inference

```bash
curl -X POST http://localhost:8000/api/v1/infer \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the best curry recipe?",
    "max_tokens": 150
  }'
```

Response:
```json
{
  "request_id": "a1b2c3d4...",
  "formatted_response": "Everybody's dead, Dave.\n\nThe best curry recipe requires vindaloo paste, chicken, and a healthy disregard for food safety regulations...\n\nSmoke me a kipper, I'll be back for breakfast!",
  "opening_quote": {
    "text": "Everybody's dead, Dave.",
    "character": "Holly"
  },
  "closing_quote": {
    "text": "Smoke me a kipper, I'll be back for breakfast!",
    "character": "Ace Rimmer"
  }
}
```

---

## Option 2: Docker Deployment (Recommended for Users)

### 1. Clone and Build

```bash
git clone https://github.com/abuxton/reddwarf-llm.git
cd reddwarf-llm
make docker-build
```

This creates a Docker image with all dependencies. Model weights are **not** included (downloaded on first run).

### 2. Run with Docker Compose

```bash
make docker-run
```

Or manually:

```bash
docker-compose -f docker/docker-compose.yml up
```

**GPU Support (Linux NVIDIA)**:
- Requires `nvidia-container-toolkit` installed on host
- Uncomment GPU section in `docker/docker-compose.yml`

**macOS**: GPU acceleration not available in containers. CPU inference works but is slower.

### 3. Download Models

In a separate terminal while container is running:

```bash
docker exec -it reddwarf-llm-1 make download-models
```

Or use the provided script:

```bash
docker exec -it reddwarf-llm-1 python scripts/download-models.sh
```

### 4. Test Inference

Same `curl` command as devcontainer option (server on `http://localhost:8000`).

---

## Option 3: Local Python Environment (Advanced)

### 1. Set Up Virtual Environment

```bash
python3.10 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install -e '.[dev]'
```

### 3. Download Models

```bash
make download-models
```

### 4. Configure GPU (Optional)

**CUDA (NVIDIA)**:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

**Metal (macOS)**:
```bash
# Already included in torch 2.0+
```

### 5. Run Server

```bash
make run
```

---

## Common Commands (Makefile)

All commands work in devcontainer, Docker, or local environments:

```bash
make help              # Show all available commands
make test              # Run test suite with coverage
make lint              # Run type checking and linting (mypy, ruff)
make format            # Format code (black, isort)
make run               # Start FastAPI server
make docker-build      # Build Docker image
make docker-run        # Run Docker container
make download-models   # Fetch models from HuggingFace
make clean             # Remove cache and build artifacts
```

---

## Configuration

### Model Selection

Edit `src/reddwarf/config/defaults.yaml`:

```yaml
model:
  model_id: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # or "microsoft/phi-2"
  quantization: "4bit"  # Options: "none", "4bit", "8bit"
  device: "cuda"        # Options: "cuda", "mps", "cpu"
  max_memory_mb: 8000   # Memory limit
```

Or set environment variables:

```bash
export REDDWARF_MODEL_ID="microsoft/phi-2"
export REDDWARF_QUANTIZATION="8bit"
export REDDWARF_DEVICE="cuda"
```

### API Server

Environment variables (`.env` file or export):

```bash
REDDWARF_HOST=0.0.0.0       # Bind address
REDDWARF_PORT=8000          # Port
REDDWARF_LOG_LEVEL=info     # Logging level
REDDWARF_INFERENCE_TIMEOUT=10  # Timeout in seconds
```

---

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### Generate Inference
```bash
curl -X POST http://localhost:8000/api/v1/infer \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum mechanics",
    "max_tokens": 200,
    "temperature": 0.8
  }'
```

### List Available Models
```bash
curl http://localhost:8000/api/v1/models
```

### Get Current Model Status
```bash
curl http://localhost:8000/api/v1/models/current
```

### Get Random Quote
```bash
curl http://localhost:8000/api/v1/quotes
```

### Quote Database Statistics
```bash
curl http://localhost:8000/api/v1/quotes/stats
```

---

## Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI with:
- Interactive request testing
- Schema documentation
- Example payloads
- Error response formats

---

## Performance Tips

### For Best Speed (<2s inference)
- Use **4-bit quantization** (`quantization: "4bit"`)
- Use **TinyLlama-1.1B** for fastest responses
- Ensure GPU acceleration is enabled (`device: "cuda"` or `device: "mps"`)
- Keep `max_tokens` at 512 or below

### For Best Quality
- Use **8-bit quantization** or **no quantization** (`quantization: "none"`)
- Use **Phi-2** for more coherent responses
- Increase `temperature` to 0.8-1.0 for creativity

### If Low on Memory (<8GB VRAM)
- Use **4-bit quantization** (mandatory)
- Use **TinyLlama-1.1B** (smaller model)
- Close other GPU applications
- Set `max_memory_mb: 7000` to reserve headroom

### CPU Fallback (No GPU)
- Set `device: "cpu"`
- Expect 5-10s inference times (slower but functional)
- Use 4-bit quantization to reduce RAM usage
- Consider using Docker on a machine with GPU instead

---

## Troubleshooting

### "Model not loaded" Error
```bash
# Download models if missing
make download-models

# Check model cache
ls -lh data/models/
```

### "CUDA out of memory" Error
```yaml
# Reduce quantization in config
quantization: "4bit"  # More aggressive compression
max_memory_mb: 7000   # Lower limit
```

### "Inference timeout" Error
```bash
# Increase timeout (default: 10s)
export REDDWARF_INFERENCE_TIMEOUT=20
```

### Devcontainer GPU Not Working (Linux)
```bash
# Install nvidia-container-toolkit on host
sudo apt-get install nvidia-container-toolkit
sudo systemctl restart docker

# Verify GPU accessible
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### macOS Metal Not Accelerating
```python
# Verify MPS availability in Python
import torch
print(torch.backends.mps.is_available())  # Should be True on Apple Silicon

# If False, check PyTorch version
pip install --upgrade torch
```

---

## Next Steps

- **Read API documentation**: `/docs` endpoint or `contracts/openapi.yaml`
- **Explore code structure**: See `specs/001-reddwarf-llm/plan.md`
- **Add new quotes**: Edit `src/reddwarf/quotes/quotes.json`
- **Run benchmarks**: `python scripts/benchmark.py`
- **Contribute**: See `CONTRIBUTING.md` (future)

---

## Getting Help

- **Issues**: https://github.com/abuxton/reddwarf-llm/issues
- **Discussions**: https://github.com/abuxton/reddwarf-llm/discussions
- **Red Dwarf Community**: http://www.reddwarf.co.uk/

---

**Remember**: This is a fan project for entertainment. If Holly starts giving you serious life advice, you've configured something wrong. Or maybe you just need to reboot with an IQ increase. Good luck, dude! 🚀
