VENV_DIR ?= .venv
SYSTEM_PYTHON ?= python3
PYTHON ?= $(SYSTEM_PYTHON)
BUILD_DIR := build

.PHONY: build clean venv sdk update-sdk

venv:
	$(SYSTEM_PYTHON) -m venv $(VENV_DIR)

build:
	$(PYTHON) scripts/plugin_build.py config.json plugin $(BUILD_DIR)/plugin.plugin

sdk update-sdk: scripts/update_sdk.py
	$(SYSTEM_PYTHON) scripts/update_sdk.py

clean:
	rm -rf $(BUILD_DIR)
