prepare-venvironment:
	@echo "Preparando ambiente virtual e dependências para Windows"
	@if exist venv rmdir /s /q venv
	@python -m venv .venv
	@.venv\Scripts\python -m pip install --upgrade pip
	@.venv\Scripts\pip install -r requirements/requirements.txt
	@echo "O ambiente virtual esta pronto."
	@echo "Ative o .venv usando .venv\Scripts\activate"

prepare-macos:
	@echo "Preparando ambiente virtual e dependências para MacOs"
	rm -rf venv
	~/.pyenv/versions/3.11.9/bin/python -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/pip install -r requirements/requirements.txt
	@echo "O ambiente virtual esta pronto."
	@echo "Ative usando: source .venv/bin/activate"