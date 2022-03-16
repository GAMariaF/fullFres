# fullFres
Database med import/eksportmuligheter og GUI for tolkning av sekvensvarianter fra tumorsekvensering

## Oppsett:
* Sqlite-db via Sqlalchemy
* Python3 
* Flask for backend-server
* React som frontend
* Bootstrap som css
* Tabell-bibliotek?
* authentication?


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

#### Kjør flask app (backend API):
```python
python run_backend_server.py
```

#### Kjør frontend server:
```sh
npm start
#Starts the development server.

npm run build
#Bundles the app into static files for production.

npm test
#Starts the test runner.

npm run eject
#Removes this tool and copies build dependencies, configuration files
#and scripts into the app directory. If you do this, you can’t go back!

# We suggest that you begin by typing:

cd frontend
npm start
```



#### TODO:
- [ ] Bestemme tabell-bibliotek
- [ ] Lage db schema
- [ ] Lage funksjon for å generere DB
- [ ] Lage test-mappe og script
- [ ] Lage dockerfiles
- [ ] Lage docker-compose oppsett
- [ ] 
- [ ] 
- [ ] 
- [ ] 


#### Info om diverse installeringer etc
```sh
# Installer node:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
source ~/.bash_profile
nvm install v17.7.1

# Create App:
npx create-react-app frontend
```