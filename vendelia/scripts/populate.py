import os
import sys
import pathlib
import argparse
import subprocess
import json


PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
MIGRATIONS_DIR = PROJECT_ROOT / 'marketplace' / 'migrations'
DB_PATH = PROJECT_ROOT / 'db.sqlite3'
CATEGORIES_DATA_PATH = PROJECT_ROOT / 'scripts' / 'categories.json'
DJANGO_SETTINGS_MODULE = 'vendelia.settings'
BASE_DIR = PROJECT_ROOT / 'vendelia'

# Set CWD to BASE_DIR
os.chdir(PROJECT_ROOT / 'vendelia')

# Ensure virtual env is active
if os.environ.get('VIRTUAL_ENV') != str(PROJECT_ROOT.parent / 'env'):
    print('Error: Virtual Environment not active. Exiting.')
    sys.exit(1)

# Set django settings with Vendelia project
import django
sys.path.append(str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', DJANGO_SETTINGS_MODULE)
django.setup()


# Argument parsing
parser = argparse.ArgumentParser(description='Initializes categories into DB and optionally sample product data.')
parser.add_argument('-p', '--products', action='store_true', help='Populate DB with sample product data.')
args = parser.parse_args()

# Populate categories
from marketplace.models import Categoria
with open(CATEGORIES_DATA_PATH, 'r', encoding='utf-8') as fp:
    categories = json.load(fp)
    for category_name in categories:
        category = Categoria(name=category_name)
        category.save()

# Populate sample product data
if args.products:
    print('Sample product data // TODO')
