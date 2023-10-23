# fullFres
Database med import/eksportmuligheter og GUI for tolkning av sekvensvarianter fra tumorsekvensering

## Oppsett:
* Sqlite-db via Sqlalchemy
* Python3 
* Flask for backend-server
* Vue som frontend
* Bootstrap som css

## Sett opp tom database
Blir gjort automatisk viss angitt database ikkje eksisterer (??)

## Sett opp VariantBrowser ved hjelp av docker image
- Sett IP i frontend/src/config.js
- Endre backend-port i run_backend.py og frontend/src/config.js
- Bygg Image fra fullFres mappa: docker image build -t name -f docker/Dockerfile . 
- Sett frontendport i run_VB_docker.sh og kjør for å starte docker
- Paths i backend/config.ini må kanskje endres på

## Sett opp dev utgave
- Installer nvm som beskrevet nedenfor
- Sett opp python virtual env og installer requirements.txt, mer infor nedenfor
- Sett korrekt ip og backendport i run_backend.py og frontend/src/config.js
- Sett frontend port i frontend/start_frontend.sh
- Paths i backend/config.ini må endres på
  
```sh
# Starte flask 
# Fra /illumina/analysis/dev/2022/fullFres
python run_backend_server.py # Sier i fra om du må aktivere virtualenv
# Starte javascript
cd frontend; sh start_frontend.sh 

# Passord 
#bruker: passord: buso123
```

## Bruker og passord
Kjør db/users_db/add_user.py for å legge til brukere.
(Gjør det fra docker ved å gå inn i docker med: docker exec -it {container.id} /bin/bash)

Endre passord med db/users_db/change_pwd.py
OBS: man trenger ikke å kunne det gamle passordet for å gjøre dette, det er en simpel overskriving.

## Unapprove og sletting av prøver
En prøve som allerede har vært gjennom kontroll kan sendes tilbake til start ved hjelp av db/unapprove_sample.py {sample}

En prøve kan bli sletted ved hjelp av db/remove_sample.py {sample}
OBS: bare "Samples" og "VariantsPerSample" blir slettet, generell variantdata og evtuelle klassifiseringer forblir. 

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
### Starte for test:
#### Kjør flask app (backend API):


#### TODO:
- [x] Bestemme tabell-bibliotek
- [x] Lage db schema
- [x] Lage funksjon for å generere DB
- [x] Lage dockerfiles
- [x] Lage rapport-funksjon
- [ ] Lage test-mappe og scripts for å teste

#### Info om diverse installeringer etc
```sh
# Installer node:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
source ~/.bash_profile
nvm install v16.14.2


# Create Vue App:
# vue create frontend # preset = vue2

# Pakker som er installert etterpå (i frontend-folder):
npm install bootstrap bootstrap-vue vue-router@3.4.9 axios vue-axios --save
npm install --save vue-perfect-scrollbar

# Starts the development server.
npm run serve
# Jeg måtte nedgradere nodeversion for å få det til
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

#### DB schema
![DB schema](https://raw.githubusercontent.com/oyvindbusk/fullFres/main/db/DB%20schema.png)

#### Info om Vue auth
Jeg lager en relativt enkel login-løsning uten Oauth, og satser heller på en lokal mock backend ala: https://jasonwatmore.com/post/2018/07/14/vue-vuex-user-registration-and-login-tutorial-example

