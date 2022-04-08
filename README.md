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

flask-cors

# Installere utenom requirements.txt:
python -m pip install <pakkenavn>
```

#### Kjør flask app (backend API):
```python
python run_backend_server.py
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
nvm install v16.14.2

# Create Vue App:
vue create frontend # preset = vue2

# Pakker som er installert etterpå:
npm install bootstrap bootstrap-vue vue-router@3.4.9 axios vue-axios --save


# Starts the development server.
npm run serve
# Jeg måtte nedgradere nodeversion for å få det til
```


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

#### SQLAlchemy
```python
import sqlite3
import sqlalchemy
```

#### Info om Vue auth
Jeg lager en relativt enkel login-løsning uten Oauth, og satser heller på en lokal mock backend ala: https://jasonwatmore.com/post/2018/07/14/vue-vuex-user-registration-and-login-tutorial-example
