# fullFres
Database med import/eksportmuligheter og GUI for tolkning av sekvensvarianter fra tumorsekvensering

#### Aktivere virtualenv:
> virtualenv is used to manage Python packages for different projects. Using virtualenv allows you to avoid installing Python packages globally which could break system tools or other projects. You can install virtualenv using pip.

```python
# Installert med: python3.9 -m venv env
# Aktiver
source env/bin/activate
# Deaktiver
deactivate
# Installer biblioteker
python3 -m pip install -r requirements.txt
# Installere utenom requirements.txt:
python -m pip install flask
```

#### Kjør flask app:

```python
# Si hvor app befinenrn seg
export FLASK_APP=frontend/frontend
# Sett til development, så den restarter hver gang man gjør en endring
export FLASK_ENV=development
```

