# Red Dwarf Tiny LLM 🚀

> *"Everybody's dead, Dave. Everybody's dead, Dave."* - Holly

A tiny LLM inference service that bookends responses with Red Dwarf quotes. Because Holly's IQ is declining, but yours doesn't have to.

## 🎯 What Is This?

Red Dwarf LLM is a humorous, community-driven project that runs tiny language models (TinyLlama-1.1B, Phi-2) on consumer hardware with automatic Red Dwarf quote formatting. Perfect for hobbyist developers who want to experiment with AI without enterprise-grade GPUs.

### Features

- 🤖 **Tiny models** that run on <8GB VRAM (or CPU if you're patient)
- 🎭 **Red Dwarf quotes** automatically bookend all responses
- 🐳 **Docker & devcontainer** support for easy setup
- 📊 **Performance monitoring** with structured logs
- 🔧 **Model selection** between TinyLlama and Phi-2
- 🧪 **80%+ test coverage** with pytest
- 📝 **Full type hints** validated by mypy --strict

## 🚧 Project Status

**Current Phase: MVP Implementation (Phase 3)**

- ✅ Phase 1: Project scaffolding and setup (Complete)
- ✅ Phase 2: Foundational infrastructure (Complete)
- 🔄 Phase 3: Core inference engine (In Progress)
- ⏳ Phase 4-10: Additional features (Pending)

See [specs/001-reddwarf-llm/tasks.md](specs/001-reddwarf-llm/tasks.md) for detailed task breakdown.

## 📦 Installation

### Prerequisites

- Python 3.10+
- 8GB RAM minimum (4GB+ VRAM recommended)
- 15GB free disk space

### Quick Start (Development)

```bash
# Clone the repository
git clone https://github.com/abuxton/reddwarf-llm.git
cd reddwarf-llm

# Install in editable mode with dev dependencies
make -f Makefile.reddwarf install

# Download models (TinyLlama + Phi-2, ~2-3GB)
make -f Makefile.reddwarf download-models

# Run tests
make -f Makefile.reddwarf test

# Start API server
make -f Makefile.reddwarf run
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🐳 Docker Deployment

```bash
# Build image
make -f Makefile.reddwarf docker-build

# Run container
make -f Makefile.reddwarf docker-run
```

## 🎮 Usage

### API Example

```bash
curl -X POST http://localhost:8000/api/v1/infer \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the best curry recipe?",
    "max_tokens": 150,
    "temperature": 0.8
  }'
```

**Response:**
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
  },
  "inference_time_ms": 1245.7,
  "tokens_generated": 78
}
```

## 🏗️ Architecture

```
src/reddwarf/
├── config/         # Settings and configuration
├── quotes/         # Red Dwarf quote database
├── model/          # Model loading and registry
├── inference/      # Inference engine (Phase 3)
├── formatting/     # Response formatting with quotes
├── api/            # FastAPI endpoints
└── monitoring/     # Metrics and logging

tests/
├── unit/           # Unit tests (>90% coverage)
├── integration/    # End-to-end tests
├── contract/       # API contract tests
├── performance/    # Speed and memory benchmarks
└── fixtures/       # Test data and scenarios
```

## 📚 Documentation

- [Quick Start Guide](specs/001-reddwarf-llm/quickstart.md)
- [API Reference](specs/001-reddwarf-llm/contracts/openapi.yaml)
- [Task Breakdown](specs/001-reddwarf-llm/tasks.md)
- [Research & Decisions](specs/001-reddwarf-llm/research.md)

## 🧪 Testing

```bash
# Run all tests with coverage
make -f Makefile.reddwarf test

# Run specific test suites
make -f Makefile.reddwarf test-unit
make -f Makefile.reddwarf test-integration
make -f Makefile.reddwarf test-contract
make -f Makefile.reddwarf test-performance

# Type checking and linting
make -f Makefile.reddwarf lint

# Code formatting
make -f Makefile.reddwarf format
```

## 🔧 Configuration

Settings can be configured via `src/reddwarf/config/defaults.yaml` or environment variables:

```bash
export REDDWARF_MODEL_ID="microsoft/phi-2"
export REDDWARF_QUANTIZATION="8bit"
export REDDWARF_DEVICE="cuda"
export REDDWARF_MAX_MEMORY_MB=8000
```

## 🤝 Contributing

This is a fan project for entertainment and learning. Contributions welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/smeghead-feature`)
3. Write tests for your changes
4. Ensure `make -f Makefile.reddwarf lint` and `make -f Makefile.reddwarf test` pass
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details (coming soon).

## 📝 License

DBAD (Don't Be A Dick) License - See [LICENSE](LICENSE)

## 🙏 Acknowledgments

- Red Dwarf subtitle database from [reddwarfsubs](https://github.com/???/reddwarfsubs)
- Built with [FastAPI](https://fastapi.tiangolo.com/), [PyTorch](https://pytorch.org/), and [Transformers](https://huggingface.co/transformers/)
- Inspired by the genius of Grant Naylor Productions

## ⚠️ Disclaimer

This is a fan project for entertainment and educational purposes. Red Dwarf is owned by Grant Naylor Productions. If Holly starts giving you serious life advice, you've configured something wrong. Or maybe you just need to reboot with an IQ increase.

**Remember**: This is a community project for entertainment. Have fun, write clean code, and may your curry always be vindaloo! 🚀

---

*"What a guy!"* - Everyone who uses this project (hopefully)
