# Red Dwarf Tiny LLM API Contracts

This directory contains API contract specifications for the Red Dwarf LLM service.

## Files

- **openapi.yaml**: OpenAPI 3.0 specification for REST endpoints
- **examples/**: Sample request/response payloads

## API Versioning

- Current version: `v1`
- Base path: `/api/v1`
- All endpoints versioned to support future MCP server migration

## Authentication

- **Phase 1**: No authentication (local single-user deployment)
- **Future**: Optional API key for multi-user/hosted deployments

## Rate Limiting

- **Phase 1**: No rate limiting (single-user)
- **Future**: Consider rate limiting if exposing publicly

## Error Handling

All error responses follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional context (optional)"
    }
  }
}
```

Error codes:
- `INVALID_REQUEST`: Validation error (400)
- `MODEL_NOT_LOADED`: Model not available (503)
- `INFERENCE_FAILED`: Generation error (500)
- `INFERENCE_TIMEOUT`: Exceeded time limit (504)
- `INSUFFICIENT_MEMORY`: Out of VRAM/RAM (507)
