# Testes de Mutação – Projeto Biblioteca

- **Ferramenta:** `mutmut`
- **Módulos mutados (3+):**
  - `src/services` 
  - `src/models` 
  - `src/repositories/repository.py`
- **Cobertura usada para acelerar:** sim (`--use-coverage`)
- **Runner de testes:** `pytest -q`
- **Ambiente:** Ubuntu/WSL + Python 3.12 (venv)

## Como rodar

# entre na pasta do projeto
cd ~/projeto-teste-software

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "mutmut==2.4.4"
python -m pip install -U pip wheel setuptools
pip install -r config/requirements.txt
pip install pytest pytest-cov
$env:MUTMUT_TRAMPOLINE_DISABLED = "1"
pip install 'pydantic[email]'
pytest -q --cov=src --cov-branch
mutmut run `
  --paths-to-mutate "src/services,src/repositories/repository.py,src/models" `
  --tests-dir "tests/unit" `
  --runner "pytest -q tests/unit --maxfail=1" `
  --use-coverage
mutmut results
mutmut junitxml > ../evidencias/mutmut_junit.xml
```