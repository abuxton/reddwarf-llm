# https://github.com/krisnova/Makefile/blob/main/Makefile

-include .env
REPO_TOP=$(shell git rev-parse --show-toplevel)
CORE=${REPO_TOP}/common/mk/core.mk
BIN_DIR=${REPO_TOP}/common/bin
MK_DIR=${REPO_TOP}/common/mk

gh: ## GitHub CLI helper
	@if ! command -v gh >/dev/null 2>&1; then \
		echo "GitHub CLI (gh) is not installed. Please install it from https://cli.github.com/"; \
		exit 1; \
	else \
		echo "GitHub CLI (gh) is installed."; \
	fi


.PHONY: help-git
help-git:  ## Show help messages for make targets in ${BIN_DIR}/git.mk
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MK_DIR)/git.mk) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}'
