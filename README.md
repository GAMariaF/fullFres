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

### Info
* Genexus VCF inneholder noen linjer med semikolon i protein feks sånn: p.[Gln61His;Glu62Lys]. Det skaper krøll i parsing. Ha noe konvertering i script som kopierer vcf fra server?


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
python -m pip install <pakkenavn>
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


#### Info om diverse installeringer etc
```sh
# Installer node:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
source ~/.bash_profile
nvm install v17.7.1

# Create App:
npx create-react-app frontend
```

#### Pakker som sikkert dockerimage må ha for at dette skal funke:
* libffi_devel


#### Installerte python slik:
```python
wget https://www.python.org/ftp/python/3.9.11/Python-3.9.11.tgz
tar xvf Python-3.9.11.tgz
cd Python-3.9*/
./configure --enable-optimizations
sudo make altinstall
```