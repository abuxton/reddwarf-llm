"""Model registry mapping names to HuggingFace IDs."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelInfo:
    """Information about a supported model."""

    name: str
    huggingface_id: str
    description: str
    size_gb: float
    min_vram_gb: int
    recommended_quantization: str


# Supported models
_MODEL_REGISTRY: dict[str, ModelInfo] = {
    "tinyllama": ModelInfo(
        name="TinyLlama-1.1B",
        huggingface_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        description="Tiny LLM with 1.1B parameters, excellent for consumer hardware",
        size_gb=2.2,
        min_vram_gb=1,
        recommended_quantization="4bit",
    ),
    "phi2": ModelInfo(
        name="Phi-2",
        huggingface_id="microsoft/phi-2",
        description="Microsoft's 2.7B parameter model with strong reasoning",
        size_gb=5.4,
        min_vram_gb=2,
        recommended_quantization="4bit",
    ),
}


def list_available_models() -> list[ModelInfo]:
    """Get list of all available models.

    Returns:
        List of ModelInfo objects
    """
    return list(_MODEL_REGISTRY.values())


def get_model_info(name_or_id: str) -> ModelInfo | None:
    """Get model info by name or HuggingFace ID.

    Args:
        name_or_id: Model name key or full HuggingFace ID

    Returns:
        ModelInfo if found, None otherwise
    """
    # Try as key first
    name_key = name_or_id.lower().replace("-", "").replace("_", "")
    if name_key in _MODEL_REGISTRY:
        return _MODEL_REGISTRY[name_key]

    # Try as HuggingFace ID
    for info in _MODEL_REGISTRY.values():
        if info.huggingface_id == name_or_id:
            return info

    return None
