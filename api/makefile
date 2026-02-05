SHELL := /bin/bash

prepare-venvironment:
	@echo Preparando ambiente virtual e dependencias
	@if exist venv rmdir /s /q venv
	@python -m venv venv
	@venv\Scripts\python -m pip install --upgrade pip
	@venv\Scripts\pip install -r requirements.txt
	@venv
	@echo O ambiente virtual esta pronto.

#Remove-Item -Recurse -Force venv