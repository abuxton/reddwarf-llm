# https://github.com/krisnova/Makefile/blob/main/Makefile

-include .env
REPO_TOP=$(shell git rev-parse --show-toplevel)
CORE=${REPO_TOP}/common/mk/core.mk
BIN_DIR=${REPO_TOP}/common/bin
MK_DIR=${REPO_TOP}/common/mk

all: help help-git help-specify help-reddwarf

-include ${MK_DIR}/git.mk
-include ${MK_DIR}/specify.mk
-include ${MK_DIR}/reddwarf.mk

xargs: ## xargs helper for cross-platform compatibility
	@if [ "$(shell uname)" = "Darwin" ]; then \
		echo "Using macOS (Darwin) xargs options."; \
		alias xargs='xargs -n 1'; \
	else \
		echo "Using Linux xargs options."; \
		alias xargs='xargs -r'; \
	fi
jq: ## jq helper
	@if ! command -v jq >/dev/null 2>&1; then \
		echo "jq is not installed. Please install it from https://stedolan.github.io/jq/"; \
		exit 1; \
	else \
		echo "jq is installed."; \
	fi

.PHONY: help
help:  ## Show help messages for make targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(CORE)) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}'


