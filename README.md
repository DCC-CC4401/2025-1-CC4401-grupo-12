# Vendelia

CC4001 | Software Engineering Project

_**Vendelia** is a web-based marketplace designed to connect everyday people who want to buy and sell items locally — without companies, intermediaries, or international shipping. It provides a simple yet robust platform that makes it easy for sellers and buyers to connect directly._


_**Vendelia** es un mercado web diseñado para conectar a personas comunes que quieren comprar y vender artículos de forma local, sin empresas, intermediarios ni envíos internacionales. Ofrece una plataforma simple pero sólida que facilita el contacto directo entre vendedores y compradores._





## Installation

1. Clone and enter repository.

```
git clone https://github.com/DCC-CC4401/2025-1-CC4401-grupo-12
cd 2025-1-CC4401-grupo-12
```

2. Set up virtual environment using [**Python 3.10.11**](https://www.python.org/downloads/release/python-31011/).

- For Windows:
```
py -3.10 -m venv env
.\env\Scripts\activate
python -m pip install -r requirements.txt
```

- For Linux:
```
python3.10 -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
```

- For MacOs:

To switch between Python's versions, we have to set up pyenv. Instructions on: [**Install Python with pyenv**](https://mac.install.guide/python/install-pyenv ).

```
pyenv global 3.10
python -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
```

3. Make migrations.
```
cd vendelia
python manage.py makemigrations
python manage.py migrate
```

4. Test server.
```
python manage.py runserver
```

### Development tools
Inside the `vendelia/scripts` folder reside some scripts than help ease some common routines while working on the application, you can use the following syntax to get help from any script: `python script_file.py --help`.

1. Reset `reset.py`: Deletes the migrations and DB, also can be used to create a test super user.
2. Populate `populate.py`: Populate the DB with default categories, optionally can create sample user/product data for testing.
