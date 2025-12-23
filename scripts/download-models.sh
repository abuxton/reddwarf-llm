#!/bin/bash
# Download models from HuggingFace Hub
# Usage: bash scripts/download-models.sh

set -e

echo "🧠 Red Dwarf LLM - Model Download Script"
echo "=========================================="

# Set cache directory
CACHE_DIR="${TRANSFORMERS_CACHE:-./data/models}"
echo "📁 Cache directory: $CACHE_DIR"
mkdir -p "$CACHE_DIR"

# Models to download
MODELS=(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    "microsoft/phi-2"
)

echo ""
echo "📦 Models to download:"
for model in "${MODELS[@]}"; do
    echo "  - $model"
done
echo ""

# Check if Python and required packages are available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.10+."
    exit 1
fi

# Download models using HuggingFace CLI or Python
for model in "${MODELS[@]}"; do
    echo "⬇️  Downloading $model..."

    python3 -c "
from huggingface_hub import snapshot_download
import os

os.environ['TRANSFORMERS_CACHE'] = '${CACHE_DIR}'
print('Downloading ${model}...')
try:
    snapshot_download(repo_id='${model}', cache_dir='${CACHE_DIR}')
    print('✅ Downloaded ${model}')
except Exception as e:
    print(f'❌ Failed to download ${model}: {e}')
    exit(1)
" || {
        echo "❌ Failed to download $model"
        echo "   Make sure transformers/huggingface_hub is installed:"
        echo "   pip install transformers huggingface-hub"
        exit 1
    }
    echo ""
done

echo "✅ All models downloaded successfully!"
echo "🎉 Holly's brain is ready for action!"
echo ""
echo "💡 Tip: Set TRANSFORMERS_CACHE env var to change cache location"
