"""Model configuration."""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ModelConfig:
    """Configuration for loading and running a language model."""

    model_id: str
    quantization: Literal["none", "4bit", "8bit"]
    device: Literal["cuda", "mps", "cpu"]
    max_memory_mb: int | None = None
    torch_dtype: str = "float16"
    trust_remote_code: bool = False

    def __post_init__(self) -> None:
        """Validate configuration."""
        if self.max_memory_mb is not None and self.max_memory_mb < 500:
            raise ValueError(f"max_memory_mb too low: {self.max_memory_mb} (minimum 500)")
