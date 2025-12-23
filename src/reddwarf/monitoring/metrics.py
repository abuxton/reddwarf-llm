"""Performance metrics tracking."""

import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any

try:
    import torch

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


@dataclass
class PerformanceMetrics:
    """Captures resource usage and timing metrics."""

    timestamp: datetime
    inference_time_ms: float
    vram_mb: float
    ram_mb: float
    tokens_per_second: float
    model_id: str
    quantization: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "inference_time_ms": self.inference_time_ms,
            "vram_mb": self.vram_mb,
            "ram_mb": self.ram_mb,
            "tokens_per_second": self.tokens_per_second,
            "model_id": self.model_id,
            "quantization": self.quantization,
        }

    @staticmethod
    def capture(
        model_id: str,
        quantization: str,
        inference_start_time: float,
        tokens_generated: int,
    ) -> "PerformanceMetrics":
        """Capture current performance metrics.

        Args:
            model_id: Model identifier
            quantization: Quantization level used
            inference_start_time: Start time from time.time()
            tokens_generated: Number of tokens generated

        Returns:
            PerformanceMetrics instance
        """
        inference_time_ms = (time.time() - inference_start_time) * 1000
        tokens_per_second = (
            tokens_generated / (inference_time_ms / 1000) if inference_time_ms > 0 else 0.0
        )

        # Measure VRAM (GPU memory)
        vram_mb = 0.0
        if TORCH_AVAILABLE and torch.cuda.is_available():
            vram_mb = torch.cuda.memory_allocated() / (1024**2)
        elif TORCH_AVAILABLE and torch.backends.mps.is_available():
            # MPS doesn't expose memory usage easily
            vram_mb = 0.0

        # Measure RAM
        ram_mb = 0.0
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            ram_mb = process.memory_info().rss / (1024**2)

        return PerformanceMetrics(
            timestamp=datetime.utcnow(),
            inference_time_ms=inference_time_ms,
            vram_mb=vram_mb,
            ram_mb=ram_mb,
            tokens_per_second=tokens_per_second,
            model_id=model_id,
            quantization=quantization,
        )
