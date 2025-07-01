import os
import sys
import pathlib
import argparse
import json
import random
import io
from datetime import datetime, timezone
import unicodedata
import requests
import tqdm


PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
MIGRATIONS_DIR = PROJECT_ROOT / 'marketplace' / 'migrations'
DB_PATH = PROJECT_ROOT / 'db.sqlite3'
CATEGORIES_DATA_PATH = PROJECT_ROOT / 'scripts' / 'categories.json'
PRODUCT_DATA_PATH = PROJECT_ROOT / 'scripts' / 'product_data.json'
PRODUCT_IMAGE_1_PATH = PROJECT_ROOT / 'scripts' / 'product_img1.jpg'
PRODUCT_IMAGE_2_PATH = PROJECT_ROOT / 'scripts' / 'product_img2.jpg'
PRODUCT_IMAGE_3_PATH = PROJECT_ROOT / 'scripts' / 'product_img3.jpg'
PRODUCT_DUMMY_IMAGE_PATH = PROJECT_ROOT / 'marketplace' / 'static' / 'images' / 'product_no_image.jpg'
USER_NAMES_DATA_PATH = PROJECT_ROOT / 'scripts' / 'users.json'
USER_CITIES_DATA_PATH = PROJECT_ROOT / 'scripts' / 'cities.json'
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
parser.add_argument('-u', '--users', action='store_true', help='Populate DB with sample user data.')
args = parser.parse_args()

# Populate categories
print("Populating categories...")
from marketplace.models import Categoria
with open(CATEGORIES_DATA_PATH, 'r', encoding='utf-8') as fp:
    categories = json.load(fp)
    for category_name in categories:
        category = Categoria(name=category_name)
        category.save()

# Populate sample users
if args.users:
    print("Populating users...")
    from marketplace.models import User

    with open(USER_NAMES_DATA_PATH, 'r', encoding='utf-8') as fp:
        user_data = json.load(fp)

    with open(USER_CITIES_DATA_PATH, 'r', encoding='utf-8') as fp:
        city_data = json.load(fp)

    random.shuffle(user_data["first_names"])
    random.shuffle(user_data["last_names"])

    def clean_str(s):
        ss = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
        ss = ss.lower()
        return ss

    for i in range(len(user_data["first_names"])):
        first_name = user_data["first_names"][i]
        last_name = user_data["last_names"][i]

        # user = User(
            
        # )

        User.objects.create_user(
            username=f'{clean_str(first_name)}_{clean_str(last_name)}',
            email=f'{clean_str(first_name)}@mail.com',
            phone_number=str(random.randint(10000000, 99999999)),
            first_name=first_name,
            last_name=last_name,
            city=random.choice(city_data),
            is_banned=False,

            password='1234'
        )

        # user.save()


# Populate sample product data
if args.products:
    print("Populating products...")
    from django.core.files import File
    from marketplace.models import Product
    from marketplace.models import User
    
    with open(PRODUCT_DATA_PATH, 'r', encoding='utf-8') as fp:
        product_data = json.load(fp)

    category_ids = list(Categoria.objects.values_list('id', flat=True))

    # # Load images
    # img1 = open(PRODUCT_IMAGE_1_PATH, 'rb')
    # img2 = open(PRODUCT_IMAGE_2_PATH, 'rb')
    # img3 = open(PRODUCT_IMAGE_3_PATH, 'rb')

    i = 0
    for data in tqdm.tqdm(product_data):
        photo_files = []
        for photo_url in data['photos']:
            try:
                r_photo = requests.get(photo_url)
                r_photo.raise_for_status()
            except Exception:
                continue

            photo = io.BytesIO(r_photo.content)
            photo_files.append(photo)
            
        n_imgs = len(photo_files)
        random_user = User.objects.order_by("?").first()

        product = Product(
            product_name = data['title'],
            description = data['description'],
            price = random.randint(1, 20)*1000,
            photo1 = File(photo_files[0], name=f'image_{i}_1.jpg') if n_imgs >= 1 else None,
            photo2 = File(photo_files[1], name=f'image_{i}_2.jpg') if n_imgs >= 2 else None,
            photo3 = File(photo_files[2], name=f'image_{i}_3.jpg') if n_imgs >= 3 else None,
            category = Categoria.objects.get(id = random.choice(category_ids)),
            owner = random_user,
            is_sold = False,
            creation_date = datetime.now(timezone.utc),
        )

        product.save()

        i += 1

    # img1.close()
    # img2.close()
    # img3.close()


    print("Assigning dummy image to products without images")
    with open(PRODUCT_DUMMY_IMAGE_PATH, 'rb') as dummy_file:
        dummy_file_data = dummy_file.read()

    products_without_images = Product.objects.filter(photo1='', photo2='', photo3='')
    for product in products_without_images:
        dummy_file_obj = File(io.BytesIO(dummy_file_data), name='dummy.jpg')
        product.photo1 = dummy_file_obj
        product.save()
