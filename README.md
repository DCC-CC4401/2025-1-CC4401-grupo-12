# Vendelia

CC4001 | Software Engineering Project

## Installation

1. Clone and enter repository.

```
git clone https://github.com/DCC-CC4401/2025-1-CC4401-grupo-12
cd 2025-1-CC4401-grupo-12
```

2. Set up virtual environment using **Python 3.10.17**.

- For Windows:
```
py -3.10 -m venv env
.\env\bin\activate
python -m pip install -r requirements.txt
```

- For Linux:
```
python3.10 -m venv env
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
