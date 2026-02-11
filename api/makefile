prepare-venvironment:
	@echo Preparando ambiente virtual e dependencias
	@if exist venv rmdir /s /q venv
	@python -m venv .venv
	@.venv\Scripts\python -m pip install --upgrade pip
	@.venv\Scripts\pip install -r src/requirements.txt
	@echo O ambiente virtual esta pronto.
	@echo Ative o .venv usando .venv\\Scripts\\activate

#Remove-Item -Recurse -Force venv
