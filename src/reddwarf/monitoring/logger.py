"""Structured logging for Red Dwarf LLM."""

import json
import logging
from typing import Any


class StructuredLogger:
    """Logger that outputs structured JSON logs."""

    def __init__(self, name: str) -> None:
        """Initialize logger.

        Args:
            name: Logger name (typically module name)
        """
        self.logger = logging.getLogger(name)

    def log_inference(
        self,
        prompt_length: int,
        response_length: int,
        inference_time_ms: float,
        memory_mb: float,
        model: str,
        session_id: str | None = None,
    ) -> None:
        """Log inference event with structured data.

        Args:
            prompt_length: Length of input prompt in tokens
            response_length: Length of generated response in tokens
            inference_time_ms: Generation time in milliseconds
            memory_mb: Memory usage in MB
            model: Model identifier
            session_id: Optional session ID
        """
        self.logger.info(
            json.dumps(
                {
                    "event": "inference",
                    "prompt_tokens": prompt_length,
                    "response_tokens": response_length,
                    "inference_ms": inference_time_ms,
                    "memory_mb": memory_mb,
                    "model": model,
                    "session_id": session_id,
                }
            )
        )

    def log_error(self, error_type: str, error_message: str, context: dict[str, Any]) -> None:
        """Log error with context.

        Args:
            error_type: Error type/code
            error_message: Human-readable error message
            context: Additional context dictionary
        """
        self.logger.error(
            json.dumps(
                {
                    "event": "error",
                    "error_type": error_type,
                    "error_message": error_message,
                    **context,
                }
            )
        )
