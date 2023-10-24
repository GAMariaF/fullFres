# fullFres
Database med import/eksportmuligheter og GUI for tolkning av sekvensvarianter fra tumorsekvensering
OBS: Bare ment for å kjøre på lokalnett, ikke over internett.

## Oppsett:
* Sqlite-db via Sqlalchemy
* Python3 
* Flask for backend-server
* Vue som frontend
* Bootstrap som css

## Sett opp tom database
Blir gjort automatisk viss angitt database ikkje eksisterer (??, ikke testet, er nok heller ikke oppdatert med nye felt.)

## Sett opp VariantBrowser som docker container
- Sett IP i frontend/src/config.js
- Endre backend-port i run_backend.py og frontend/src/config.js
- Bygg Image fra fullFres mappa: 
  ```sh
  docker image build -t name -f docker/Dockerfile . 
  ```
  Eller bruk fullFres/build_docker.sh.
  Må bygges fra fullFres fordi heile repositoriet blir kopiert inn i dockerimaget. 
- Sett frontendport i run_VB_docker.sh og kjør for å starte docker
- Paths i backend/config.ini må kanskje endres på (man burde påse at databasen lagres utenfor docker containeren)

## Sett opp dev utgave
- Installer nvm som beskrevet lenger ned
- Sett opp python virtual env og installer requirements.txt, mer info lenger ned
- Sett korrekt ip og backendport i run_backend.py og frontend/src/config.js
- Sett frontend port i frontend/start_frontend.sh
- Paths i backend/config.ini må endres på 
  
```sh
# Starte flask 
# I ./fullFres
python run_backend_server.py 
# Sier i fra om du må aktivere virtualenv

# Starte javascript
cd frontend; sh start_frontend.sh 

# Passord 
#bruker: passord: buso123
```

## Bruker og passord
Kjør db/users_db/add_user.py for å legge til brukere.\n
(Gjør det fra docker ved å gå inn i docker med: docker exec -it {container.id} /bin/bash)

Endre passord med db/users_db/change_pwd.py\n
OBS: man trenger ikke å kunne det gamle passordet for å gjøre dette, det er en simpel overskriving.

## Laste inn prøver
- I Genexus: gå til resultat -> prøve -> varianter. Klikk export for å få ett excel ark. I tillegg: Gå på download files og last ned "filtered variants" for å få ei zip fil. 
- Legg filene i path som står i backend/config.ini "db_test_path"  (Burde få nytt navn)
- OBS: pass på at det er filtrerte filer.

## Unapprove og sletting av prøver
En prøve som allerede har vært gjennom kontroll kan sendes tilbake til start ved hjelp av db/unapprove_sample.py -S {sample.id}

En prøve kan bli sletted ved hjelp av db/remove_sample.py -S {sample.id}
OBS: bare "Samples" og "VariantsPerSample" blir slettet, generelle variantdata og evtuelle klassifiseringer forblir. 

## Backup
For å kopiere databasen kan man bruke fullFres/backup_variantdb.sh.
Den kan også koperest på vanlig måte, men viss den er i bruk/i en prosess kan den bli korrupt.
Man kan f.eks. bruke en cronjob for å regelmessig ta backup.

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

