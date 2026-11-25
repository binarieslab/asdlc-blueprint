help: ## Lists the commands
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

feature-map: ## Checks that the feature map is consistent (feature-map/AGENTS.md)
	python3 feature-map/scripts/check.py

lint: feature-map ## Feature map check, then the comment ban, analyzer and format check (docs/architecture/code-style-and-lint.md)
	./tool/lint.sh

test: feature-map ## Feature map check, then the tests and the lint tool's own tests
	python3 -m unittest discover -s tool/tests
	{{TEST_COMMAND}}

check: lint test ## The Gate in one command: lint, then test

.PHONY: help feature-map lint test check
