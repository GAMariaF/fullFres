# VariantBrowser
Database med import/eksportmuligheter og GUI for tolkning av sekvensvarianter fra tumorsekvensering
OBS: Bare ment for å kjøre på lokalnett eller på en enkelt PC, ikke over internett.

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
- Bygg Image fra VariantBrowser mappa: 
  ```sh
  docker image build -t name -f docker/Dockerfile . 
  ```
  Eller bruk VaraintBrowser/build_docker.sh.
  Må bygges fra overordna mappe fordi hele repositoriet blir kopiert inn i dockerimaget. 
- Sett frontendport i run_VB_docker.sh og kjør for å starte docker
- Paths i backend/config.ini må kanskje endres på (man burde påse at databasen lagres utenfor docker containeren)

## Sett opp dev utgave (ikke i docker)
- Installer nvm som beskrevet lenger ned
- Sett opp python virtual env og installer requirements.txt, mer info lenger ned
- Sett korrekt ip og backendport i run_backend.py og frontend/src/config.js
- Sett frontend port i frontend/start_frontend.sh
- Paths i backend/config.ini må endres på 
  
```sh
# Starte flask 
# I ./VariantBrowser
python run_backend_server.py 
# Sier i fra om du må aktivere virtualenv

# Starte javascript
cd frontend; sh start_frontend.sh 

```

## Bruker og passord
Kjør db/users_db/add_user.py for å legge til brukere.
(Gjør det i docker container ved å gå inn i containeren med: docker exec -it [container.id] bash)

Endre passord med db/users_db/change_pwd.py
Man trenger ikke å kunne det gamle passordet for å gjøre dette, da det er en simpel overskriving.

## Laste inn prøver
- I Genexus: gå til resultat -> prøve -> varianter. Klikk export for å få ett excel ark. I tillegg: Gå på download files og last ned "filtered variants" for å få ei zip fil. 
- Legg filene i path som står i backend/config.ini "db_test_path"  (Burde få nytt navn)
- OBS: pass på at det er filtrerte filer.

## Unapprove og sletting av prøver
En prøve som allerede har vært gjennom kontroll kan sendes tilbake til start ved hjelp av db/unapprove_sample.py -S [sample.id]

En prøve kan bli sletted ved hjelp av db/remove_sample.py -S [sample.id]
OBS: bare "Samples" og "VariantsPerSample" blir slettet, generelle variantdata og evtuelle klassifiseringer forblir. 

## Backup
For å kopiere databasen kan man bruke VariantBrowser/backup_variantdb.sh.
Den kan også koperest på vanlig måte, men viss den er i bruk/i en prosess kan den bli korrupt.
Man kan f.eks. bruke en cronjob for å regelmessig ta backup.

#### Sette opp virtualenv:
> virtualenv is used to manage Python packages for different projects. Using virtualenv allows you to avoid installing Python packages globally which could break system tools or other projects. You can install virtualenv using pip.

```python
# Lag env med: python3.12 -m venv env

# Aktiver
source env/bin/activate

# Deaktiver
deactivate
# Installer biblioteker
python3 -m pip install -r requirements.txt

# Installere utenom requirements.txt:
python -m pip install <pakkenavn>
```

#### DB schema
![DB schema](https://raw.githubusercontent.com/oyvindbusk/fullFres/main/db/DB%20schema.png)
