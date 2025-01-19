# Variables
PIP := python3 -m pip
SRC_CORE := ./  # Path to your source code directory
FLASK_APP := app.py  # Default Flask entry point
PYTHON := python3

# Commands
.PHONY: help install start

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using pipreqs and freeze
	@echo "⚙️ Upgrading pip..."
	@$(PIP) install --upgrade pip
	@echo "⚙️ Installing pipreqs..."
	@$(PIP) install pipreqs==0.4.13
	@echo "⚙️ Generating pipreqs.txt based on imports..."
	@pipreqs ./services ./app.py --force --savepath pipreqs.txt
	@echo "⚙️ Adjusting pipreqs.txt..."
	@sed -i '' 's/==.*//' pipreqs.txt
	@echo "⚙️ Installing dependencies from pipreqs.txt..."
	@$(PIP) install -r pipreqs.txt --verbose
	@echo "⚙️ Installing dev dependencies from requirements-dev.txt..."
	@if [ -f requirements-dev.txt ]; then $(PIP) install -r requirements-dev.txt --verbose; else echo "requirements-dev.txt not found, skipping."; fi
	@echo "⚙️ Freezing dependencies into requirements.txt..."
	@$(PIP) freeze > requirements.txt
	@echo "✅ All dependencies installed and frozen into requirements.txt!"

run: ## Start the Flask application
	@echo "🚀 Starting Flask application..."
	@$(PYTHON) $(FLASK_APP)

