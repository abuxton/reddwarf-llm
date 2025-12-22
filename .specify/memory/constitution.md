<!--
SYNC IMPACT REPORT
==================
Version: 0.0.0 → 1.0.0
Rationale: Initial constitution establishment with complete governance framework

Modified Principles:
- [NEW] I. Tiny & Maintainable - Code quality principles for small, focused codebase
- [NEW] II. Test Coverage & Quality - Testing standards with 80% coverage target
- [NEW] III. User Experience Consistency - Holly personality and Red Dwarf authenticity
- [NEW] IV. Performance Requirements - Sub-2s inference and memory constraints
- [NEW] V. Entertainment First - Fun-focused development philosophy

Added Sections:
- Core Principles (5 principles)
- Technical Standards
- Development Philosophy
- Governance

Templates Status:
- ✅ plan-template.md: Constitution Check section aligns with new principles
- ✅ spec-template.md: Requirements and success criteria support entertainment + quality focus
- ✅ tasks-template.md: Task categorization supports model, agent, MCP server, and test work
- ⚠️  commands/*.md: No commands directory present - N/A

Follow-up TODOs:
- Create README.md with project overview and DBAD license reference
- Add LICENSE file with DBAD license text
- Consider adding docs/holly-personality.md for character consistency guidelines
-->

# reddwarf-llm Constitution

## Core Principles

### I. Tiny & Maintainable

**Small, focused, maintainable codebase befitting a "tiny" LLM project.**

- Code MUST remain small and focused—avoid feature creep and unnecessary complexity
- Clear separation of concerns: model training, inference, Holly agent logic, MCP server
- Python-first development with type hints (PEP 484) for all public functions and classes
- Code MUST be readable and well-documented so contributors can understand it quickly
- Humorous comments and docstrings are encouraged, but MUST NOT sacrifice clarity
- Each module should have a single, well-defined purpose
- Prefer composition over inheritance; avoid deep class hierarchies

**Rationale**: A "tiny" LLM project should have a tiny codebase. Maintainability ensures the project remains fun and approachable for contributors, not a bureaucratic nightmare Holly would mock.

### II. Test Coverage & Quality

**Comprehensive testing with 80% coverage for critical paths, Red Dwarf themed test data.**

- Unit tests MUST cover all core LLM functions, utilities, and data processing
- Integration tests MUST verify Holly agent interactions and personality consistency
- MCP server endpoint tests MUST validate all API contracts
- Test data SHOULD include Red Dwarf quotes, scenarios, and character interactions
- Minimum 80% code coverage for critical paths (model inference, agent logic, MCP endpoints)
- Model evaluation metrics MUST track response quality and character consistency
- Tests MUST be runnable locally without external dependencies where possible
- Test failures MUST be treated as blockers for merges

**Rationale**: Even entertainment projects need quality assurance. Tests ensure Holly stays consistent and the LLM doesn't start talking like Talkie Toaster.

### III. User Experience Consistency

**Holly's personality and Red Dwarf authenticity MUST be preserved across all interactions.**

- Holly's personality MUST align with the show: senile computer, IQ 6000 (formerly), sarcastic yet occasionally helpful
- Responses MUST feel authentic to the Red Dwarf universe—references, tone, humor style
- API interfaces MUST be intuitive and thoroughly documented with examples
- Error messages MAY be humorous but MUST clearly explain the problem and solution
- Progressive enhancement philosophy: basic features work excellently before advanced features
- No breaking character: Holly wouldn't use modern slang or break the fourth wall inappropriately
- User documentation MUST be entertaining to read while remaining genuinely useful

**Rationale**: Fans will notice if Holly sounds wrong. Consistency = authenticity = entertainment value.

### IV. Performance Requirements

**Fast inference suitable for interactive chat on personal hardware.**

- Model inference MUST target < 2 seconds response time for interactive chat
- Memory footprint MUST be suitable for personal/hobbyist hardware (< 8GB GPU VRAM target)
- Efficient tokenization and embedding strategies MUST be prioritized
- Lazy loading of model weights where possible to reduce startup time
- Monitoring and logging MUST detect performance regressions
- MCP server content retrieval SHOULD be sub-second for typical queries
- Batch processing for training MAY sacrifice speed for resource efficiency
- Performance benchmarks MUST be tracked in tests and CI/CD

**Rationale**: An LLM that takes 30 seconds to respond isn't interactive—it's just Rimmer giving a lecture. Personal hardware constraints keep the project accessible to hobbyists.

### V. Entertainment First

**Fun is paramount—this is fan content for entertainment, not a commercial product.**

- Entertainment value MUST be the primary driver of feature decisions
- This is a fun-first project; production-grade reliability is secondary
- Respect Red Dwarf IP: this is fan content, non-commercial use only
- Community-friendly development under DBAD (Don't Be A Dick) license
- Documentation SHOULD be entertaining while remaining useful
- Humor MUST be safe and respectful—no punching down, no offensive content
- Contributors should enjoy working on this; if it stops being fun, reassess
- Embrace the spirit of Red Dwarf: irreverent but fundamentally optimistic

**Rationale**: Red Dwarf is comedy sci-fi. If reddwarf-llm becomes tedious corporate software, we've missed the point. Keep it fun, keep it respectful, keep it smeggin' entertaining.

## Technical Standards

**Technology Stack**:
- Python 3.10+ as primary development language
- PyTorch or similar for model development
- FastAPI or similar for MCP server implementation
- pytest for testing framework
- Type hints mandatory for all public APIs
- Black + isort for code formatting (with max line length 100)
- mypy for static type checking

**Code Organization**:
- Clear module separation: `src/model/`, `src/agent/`, `src/mcp_server/`, `src/utils/`
- Tests mirror source structure: `tests/unit/`, `tests/integration/`, `tests/contract/`
- Model artifacts and training data in separate `data/` and `models/` directories
- Configuration via environment variables or config files, never hardcoded

**Performance Standards**:
- All PRs MUST include performance benchmarks if touching inference or API paths
- Model quantization and optimization MUST be considered for deployment
- Memory profiling SHOULD be performed for major changes

## Development Philosophy

**Open Source Ethos**:
- Welcoming to new contributors; provide helpful feedback, not gatekeeping
- Issues SHOULD be well-documented with reproduction steps
- PRs SHOULD be small and focused; large changes require prior discussion
- Code reviews MUST be constructive and kind (DBAD license applies to reviews too!)

**Documentation Requirements**:
- README MUST explain what reddwarf-llm is and how to get started
- Docstrings MUST explain the "why" not just the "what"
- Breaking changes MUST be documented in CHANGELOG
- API documentation MUST include examples and expected behavior

**Quality Gates**:
- All code MUST pass linting (black, isort, mypy)
- All tests MUST pass before merge
- Coverage MUST NOT decrease below 80% for critical paths
- Manual testing of Holly personality consistency for agent changes

## Governance

**Amendment Process**:
- Constitution amendments require documented rationale and community discussion
- Breaking changes to core principles require MAJOR version bump
- New principles or sections require MINOR version bump
- Clarifications and typo fixes require PATCH version bump
- All amendments MUST update `LAST_AMENDED_DATE`

**Compliance Verification**:
- All PRs MUST verify alignment with Core Principles I-V
- Technical Standards MUST be enforced via CI/CD (linting, tests, coverage)
- Performance Requirements SHOULD be verified via automated benchmarks
- UX Consistency (Principle III) requires manual review for agent/personality changes

**Complexity Justification**:
- Any violation of "Tiny & Maintainable" (Principle I) MUST be justified in PR description
- Adding new dependencies MUST explain why existing tools are insufficient
- Architecture changes MUST document simpler alternatives considered and rejected

**Constitution Authority**:
- This constitution supersedes all other documentation in case of conflict
- When in doubt, refer to Core Principles for decision-making guidance
- Entertainment First (Principle V) is the tiebreaker when principles conflict

**Version**: 1.0.0 | **Ratified**: 2025-12-22 | **Last Amended**: 2025-12-22
