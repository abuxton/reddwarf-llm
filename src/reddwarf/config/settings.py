"""Settings management with Pydantic validation and environment variable overrides."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, field_validator


class ModelSettings(BaseModel):
    """Model configuration settings."""

    model_id: str = Field(default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    quantization: Literal["none", "4bit", "8bit"] = Field(default="4bit")
    device: Literal["cuda", "mps", "cpu"] = Field(default="cuda")
    max_memory_mb: int = Field(default=8000, ge=500)
    torch_dtype: str = Field(default="float16")
    trust_remote_code: bool = Field(default=False)

    @field_validator("quantization")
    @classmethod
    def validate_quantization(cls, v: str, info: dict) -> str:
        """Ensure quantization is only used with GPU."""
        # Note: device not available in info.data during validation
        # This check will be done at runtime in load_settings
        return v


class InferenceSettings(BaseModel):
    """Inference generation settings."""

    max_tokens: int = Field(default=512, ge=1, le=2048)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    top_k: int = Field(default=50, ge=1, le=100)
    do_sample: bool = Field(default=True)
    timeout_seconds: int = Field(default=10, ge=1)


class APISettings(BaseModel):
    """API server settings."""

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, ge=1, le=65535)
    log_level: Literal["debug", "info", "warning", "error"] = Field(default="info")
    reload: bool = Field(default=False)


class CacheSettings(BaseModel):
    """Cache and file path settings."""

    transformers_cache: str = Field(default="./data/models")
    quote_database_path: str = Field(default="src/reddwarf/quotes/quotes.json")


class MonitoringSettings(BaseModel):
    """Monitoring and logging settings."""

    enable_metrics: bool = Field(default=True)
    enable_structured_logs: bool = Field(default=True)
    log_inference_details: bool = Field(default=True)


class Settings(BaseModel):
    """Complete application settings."""

    model: ModelSettings = Field(default_factory=ModelSettings)
    inference: InferenceSettings = Field(default_factory=InferenceSettings)
    api: APISettings = Field(default_factory=APISettings)
    cache: CacheSettings = Field(default_factory=CacheSettings)
    monitoring: MonitoringSettings = Field(default_factory=MonitoringSettings)

    class Config:
        """Pydantic configuration."""

        frozen = False
        validate_assignment = True


def load_settings(config_path: str | None = None) -> Settings:
    """Load settings from YAML file and environment variables.

    Priority (highest to lowest):
    1. Environment variables (REDDWARF_*)
    2. Custom config file (if provided)
    3. Default config file (src/reddwarf/config/defaults.yaml)

    Args:
        config_path: Optional path to custom YAML config file

    Returns:
        Settings instance with merged configuration

    Raises:
        FileNotFoundError: If config file not found
        ValueError: If configuration is invalid
    """
    # Load default config
    default_config_path = Path(__file__).parent / "defaults.yaml"
    with open(default_config_path) as f:
        config_data = yaml.safe_load(f)

    # Merge custom config if provided
    if config_path:
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(config_file) as f:
            custom_config = yaml.safe_load(f)
            # Deep merge custom config
            _deep_merge(config_data, custom_config)

    # Create settings instance
    settings = Settings(**config_data)

    # Override with environment variables
    _apply_env_overrides(settings)

    # Runtime validation
    _validate_runtime_constraints(settings)

    return settings


def _deep_merge(base: dict, override: dict) -> None:
    """Deep merge override dict into base dict."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def _apply_env_overrides(settings: Settings) -> None:
    """Apply environment variable overrides."""
    # Model settings
    if model_id := os.getenv("REDDWARF_MODEL_ID"):
        settings.model.model_id = model_id
    if quantization := os.getenv("REDDWARF_QUANTIZATION"):
        settings.model.quantization = quantization  # type: ignore
    if device := os.getenv("REDDWARF_DEVICE"):
        settings.model.device = device  # type: ignore
    if max_memory := os.getenv("REDDWARF_MAX_MEMORY_MB"):
        settings.model.max_memory_mb = int(max_memory)

    # Inference settings
    if max_tokens := os.getenv("REDDWARF_MAX_TOKENS"):
        settings.inference.max_tokens = int(max_tokens)
    if temperature := os.getenv("REDDWARF_TEMPERATURE"):
        settings.inference.temperature = float(temperature)
    if timeout := os.getenv("REDDWARF_INFERENCE_TIMEOUT"):
        settings.inference.timeout_seconds = int(timeout)

    # API settings
    if host := os.getenv("REDDWARF_HOST"):
        settings.api.host = host
    if port := os.getenv("REDDWARF_PORT"):
        settings.api.port = int(port)
    if log_level := os.getenv("REDDWARF_LOG_LEVEL"):
        settings.api.log_level = log_level  # type: ignore

    # Cache settings
    if cache_dir := os.getenv("TRANSFORMERS_CACHE"):
        settings.cache.transformers_cache = cache_dir


def _validate_runtime_constraints(settings: Settings) -> None:
    """Validate runtime constraints that span multiple settings.

    Raises:
        ValueError: If constraints are violated
    """
    # Quantization requires GPU
    if settings.model.quantization != "none" and settings.model.device == "cpu":
        raise ValueError(
            f"Quantization '{settings.model.quantization}' requires GPU "
            f"(device must be 'cuda' or 'mps', got '{settings.model.device}')"
        )
