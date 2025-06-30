import os
import sys
import pathlib
import argparse
import json
import random
import io


PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
MIGRATIONS_DIR = PROJECT_ROOT / 'marketplace' / 'migrations'
DB_PATH = PROJECT_ROOT / 'db.sqlite3'
CATEGORIES_DATA_PATH = PROJECT_ROOT / 'scripts' / 'categories.json'
PRODUCT_DATA_PATH = PROJECT_ROOT / 'scripts' / 'product_data.json'
PRODUCT_IMAGE_1_PATH = PROJECT_ROOT / 'scripts' / 'product_img1.jpg'
PRODUCT_IMAGE_2_PATH = PROJECT_ROOT / 'scripts' / 'product_img2.jpg'
PRODUCT_IMAGE_3_PATH = PROJECT_ROOT / 'scripts' / 'product_img3.jpg'
PRODUCT_DUMMY_IMAGE_PATH = PROJECT_ROOT / 'marketplace' / 'static' / 'images' / 'product_no_image.jpg'
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
print("Populating categories...")
from marketplace.models import Categoria
with open(CATEGORIES_DATA_PATH, 'r', encoding='utf-8') as fp:
    categories = json.load(fp)
    for category_name in categories:
        category = Categoria(name=category_name)
        category.save()

# Populate sample product data
if args.products:
    print("Populating products...")
    from django.core.files import File
    from marketplace.models import Product
    from marketplace.models import User
    
    with open(PRODUCT_DATA_PATH, 'r', encoding='utf-8') as fp:
        product_data = json.load(fp)

    category_ids = list(Categoria.objects.values_list('id', flat=True))

    # Load images
    img1 = open(PRODUCT_IMAGE_1_PATH, 'rb')
    img2 = open(PRODUCT_IMAGE_2_PATH, 'rb')
    img3 = open(PRODUCT_IMAGE_3_PATH, 'rb')

    i = 0
    for data in product_data:
        admin_user = User.objects.get(username='admin')
        n_imgs = random.randint(0, 3)

        product = Product(
            product_name = data['title'],
            description = data['description'],
            price = random.randint(1, 20)*1000,
            photo1 = File(img1, name=f'image_{i}_1.jpg') if n_imgs >= 1 else None,
            photo2 = File(img2, name=f'image_{i}_2.jpg') if n_imgs >= 2 else None,
            photo3 = File(img3, name=f'image_{i}_3.jpg') if n_imgs >= 3 else None,
            category = Categoria.objects.get(id = random.choice(category_ids)),
            owner = admin_user,
            is_sold = False
        )

        product.save()

        i += 1

    img1.close()
    img2.close()
    img3.close()


    print("Assigning dummy image to products without images")
    with open(PRODUCT_DUMMY_IMAGE_PATH, 'rb') as dummy_file:
        dummy_file_data = dummy_file.read()

    products_without_images = Product.objects.filter(photo1='', photo2='', photo3='')
    for product in products_without_images:
        dummy_file_obj = File(io.BytesIO(dummy_file_data), name='dummy.jpg')
        product.photo1 = dummy_file_obj
        product.save()
