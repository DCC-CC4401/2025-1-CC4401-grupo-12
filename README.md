# Vendelia

CC4001 | Software Engineering Project

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

# Add executable permissions to Reset dev tool
chmod +x vendelia/scripts/reset.sh
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

### Dev tools
Inside the `vendelia/scripts` folder reside some scripts than help ease some common routines while working on the application, there are both (equivalent) Bash and Bat scripts, use the version you need accordingly.

1. Reset: This deletes the migrations and DB, also can be used to create a test super user.

    * `scripts/reset.sh`: Runs the delete operations.
    * `scripts/reset.sh -a`: In addition to deletion, create a test superuser with `username: admin` and `password: admin`.