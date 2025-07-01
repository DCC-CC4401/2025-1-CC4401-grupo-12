import os
import sys
import pathlib
import argparse
import subprocess
import json

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
MIGRATIONS_DIR = PROJECT_ROOT / 'marketplace' / 'migrations'
DB_PATH = PROJECT_ROOT / 'db.sqlite3'
RESET_DATA_PATH = PROJECT_ROOT / 'scripts' / 'reset.json'
DJANGO_SETTINGS_MODULE = 'vendelia.settings'
BASE_DIR = PROJECT_ROOT / 'vendelia'

# Set CWD to BASE_DIR
os.chdir(PROJECT_ROOT / 'vendelia')

# Ensure virtual env is active
if os.environ.get('VIRTUAL_ENV') != str(PROJECT_ROOT.parent / 'env'):
    print('Error: Virtual Environment not active. Exiting.')
    sys.exit(1)

# Argument parsing
parser = argparse.ArgumentParser(
    description='Resets Migrations/DB and optionally creates debug superuser.')
parser.add_argument('-a', '--admin', action='store_true',
                    help='Create debug superuser.')
args = parser.parse_args()

# Delete migration files
print('Deleting migration files')
for path in MIGRATIONS_DIR.rglob('*.py'):
    if path.name != '__init__.py':
        path.unlink()

for path in MIGRATIONS_DIR.rglob('*.pyc'):
    path.unlink()

# Delete DB
if DB_PATH.exists():
    print('Deleting DB: db.sqlite3')
    DB_PATH.unlink()

# Run migrations
print('Running migrations')
subprocess.run([sys.executable, 'manage.py', 'makemigrations'],
               cwd=PROJECT_ROOT, check=True)
subprocess.run([sys.executable, 'manage.py', 'migrate'],
               cwd=PROJECT_ROOT, check=True)

# Create debug superuser
if args.admin:
    print('Creating debug superuser')

    # Set django settings with Vendelia project
    import django

    sys.path.append(str(PROJECT_ROOT))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', DJANGO_SETTINGS_MODULE)
    django.setup()

    from django.contrib.auth import get_user_model

    # Check for existing credentials, otherwise prompts the user to enter new ones.
    if RESET_DATA_PATH.exists():
        with open(RESET_DATA_PATH, 'r', encoding='utf-8') as fp:
            reset_data = json.load(fp)
            admin_username = reset_data['username']
            admin_email = reset_data['email']
            admin_password = reset_data['password']
            admin_phone_number = reset_data["phone_number"]
            admin_first_name = reset_data["first_name"]
            admin_last_name = reset_data["last_name"]
            admin_city = reset_data["city"]
    else:
        print('Credentials file not found, please enter new superuser credentials.')
        admin_username = input('Username: ')
        admin_email = input("E-mail: ")
        admin_password = input('Password: ')
        admin_phone_number = input("Phone number: ")
        admin_first_name = input("First name: ")
        admin_last_name = input("Last name: ")
        admin_city = input("City: ")
        

        reset_data = {
            'username': admin_username, 
            'email': admin_email,
            'password': admin_password,
            'phone_number': admin_phone_number,
            'first_name': admin_first_name,
            'last_name': admin_last_name,
            'city': admin_city
            }
        
        with open(RESET_DATA_PATH, 'w', encoding='utf-8') as fp:
            json.dump(reset_data, fp)

    # Saves the new superuser
    User = get_user_model()
    User.objects.create_superuser(
        username=admin_username,
        email=admin_email,
        password=admin_password,
        phone_number=admin_phone_number,
        first_name=admin_first_name,
        last_name=admin_last_name,
        city=admin_city,
        is_banned=False
    )

print('Operation completed.')
