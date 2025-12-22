# https://github.com/krisnova/Makefile/blob/main/Makefile
# GitHub Specify: https://github.com/specify/specify

-include .env

REPO_TOP=$(shell git rev-parse --show-toplevel)
MK_DIR=${REPO_TOP}/common/mk
# Specify binary check
SPECIFY_BIN := $(shell command -v specify 2> /dev/null)

# Check if specify is installed
.PHONY: specify-installed
specify-installed:
	@if [ -z "$(SPECIFY_BIN)" ]; then \
		echo "Error: specify is not installed or not in PATH"; \
		echo "Please install specify first"; \
		exit 1; \
	fi

# Install specify (manual instructions)
.PHONY: specify-install
specify-install:  ## Show instructions to install Specify CLI
	@echo "To install Specify, follow the instructions at:"
	@echo "https://github.com/specify/specify"
	@echo ""
	@echo "Common installation methods:"
	@echo "  - Download from releases: https://github.com/specify/specify/releases"
	@echo "  - Using Go: go install github.com/specify/specify@latest"

# Initialize a new Specify project (interactive)
.PHONY: specify-init
specify-init: specify-installed  ## Initialize a new Specify project from the latest template (interactive)
	@echo "Initializing Specify project..."
	@specify init
	@echo "Specify project initialized successfully"

# Initialize in current directory
.PHONY: specify-init-here
specify-init-here: specify-installed  ## Initialize Specify in current directory (interactive AI selection)
	@echo "Initializing Specify in current directory..."
	@specify init --here
	@echo "Specify project initialized in current directory"

# Initialize in current directory with force
.PHONY: specify-init-here-force
specify-init-here-force: specify-installed  ## Initialize Specify in current directory (force, skip confirmation)
	@echo "Force initializing Specify in current directory..."
	@specify init --here --force
	@echo "Specify project initialized in current directory"

# Initialize with specific AI (use: make specify-init-ai AI=claude)
.PHONY: specify-init-ai
specify-init-ai: specify-installed  ## Initialize with specific AI assistant (usage: make specify-init-ai AI=claude)
	@if [ -z "$(AI)" ]; then \
		echo "Error: AI parameter required. Usage: make specify-init-ai AI=<assistant>"; \
		echo "Available: claude, gemini, copilot, cursor-agent, qwen, opencode, codex, windsurf, kilocode, auggie, codebuddy, amp, shai, q, bob, qoder"; \
		exit 1; \
	fi
	@echo "Initializing Specify with AI: $(AI)..."
	@specify init --ai $(AI)

# Initialize here with specific AI (use: make specify-init-here-ai AI=claude)
.PHONY: specify-init-here-ai
specify-init-here-ai: specify-installed  ## Initialize in current directory with specific AI (usage: make specify-init-here-ai AI=claude)
	@if [ -z "$(AI)" ]; then \
		echo "Error: AI parameter required. Usage: make specify-init-here-ai AI=<assistant>"; \
		echo "Available: claude, gemini, copilot, cursor-agent, qwen, opencode, codex, windsurf, kilocode, auggie, codebuddy, amp, shai, q, bob, qoder"; \
		exit 1; \
	fi
	@echo "Initializing Specify in current directory with AI: $(AI)..."
	@specify init --here --ai $(AI)

# Initialize without git
.PHONY: specify-init-no-git
specify-init-no-git: specify-installed  ## Initialize Specify without git repository
	@echo "Initializing Specify without git..."
	@specify init --no-git

# Initialize here without git
.PHONY: specify-init-here-no-git
specify-init-here-no-git: specify-installed  ## Initialize Specify in current directory without git
	@echo "Initializing Specify in current directory without git..."
	@specify init --here --no-git

# Common presets - Initialize with popular AI assistants
.PHONY: specify-init-claude
specify-init-claude: specify-installed  ## Initialize with Claude AI
	@echo "Initializing Specify with Claude..."
	@specify init --here --ai claude

.PHONY: specify-init-copilot
specify-init-copilot: specify-installed  ## Initialize with GitHub Copilot
	@echo "Initializing Specify with GitHub Copilot..."
	@specify init --here --ai copilot

.PHONY: specify-init-gemini
specify-init-gemini: specify-installed  ## Initialize with Gemini AI
	@echo "Initializing Specify with Gemini..."
	@specify init --here --ai gemini

# Check that all required tools are installed
.PHONY: specify-check
specify-check: specify-installed  ## Check that all required tools are installed
	@echo "Checking Specify requirements..."
	@specify check
	@echo "Specify check complete"

# Display version and system information
.PHONY: specify-version
specify-version: specify-installed  ## Display Specify version and system information
	@specify version

# Clean Specify generated files (common patterns)
.PHONY: specify-clean
specify-clean:  ## Clean Specify generated files
	@echo "Cleaning Specify generated files..."
	@if [ -d ".specify" ]; then \
		echo "Removing .specify directory..."; \
		rm -rf .specify; \
	fi
	@if [ -f "specify.yaml" ]; then \
		echo "Found specify.yaml (not removing, use specify-clean-all)"; \
	fi
	@if [ -f "specify.yml" ]; then \
		echo "Found specify.yml (not removing, use specify-clean-all)"; \
	fi
	@echo "Clean complete"

# Clean all including config
.PHONY: specify-clean-all
specify-clean-all:  ## Clean all Specify files including configuration
	@echo "Cleaning all Specify files..."
	@rm -rf .specify
	@rm -f specify.yaml specify.yml
	@echo "All Specify files removed"

# Full setup workflow
.PHONY: specify-setup
specify-setup:  ## Complete Specify setup (check + init)
	@echo "Setting up Specify..."
	@$(MAKE) specify-check
	@$(MAKE) specify-init
	@echo "Specify setup complete!"

# Verify installation and show info
.PHONY: specify-info
specify-info: specify-installed  ## Show Specify installation information
	@echo "Specify binary location:"
	@command -v specify
	@echo ""
	@specify version

# print help for specify targets in this file
.PHONY: help-specify
help-specify:  ## Show help messages for make targets in ${MK_DIR}/specify.mk
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MK_DIR)/specify.mk) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}'
