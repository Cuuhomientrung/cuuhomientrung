import csv
import os
from django.db import migrations
from app.models import Tinh, Huyen, Xa
from django.db import models
from django.conf import settings


DATA_DIR = os.path.join(settings.BASE_DIR, 'app', 'data_files')
TTH_ID_FROM_DB = 1
TTH_ID_FROM_FILE = '67'
EXISTING_DISTRICT = 'Quảng Điền'
EXISTING_DISTRICT_ID = 1231
EXISTING_DISTRICT_ID_IN_FILE = '2371'

def import_missing_communes_for_existing_district(apps, schema_editor):
    print('{}/xa.csv'.format(DATA_DIR))
    with open('{}/xa.csv'.format(DATA_DIR)) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row[7] == EXISTING_DISTRICT_ID_IN_FILE:
                _, _ = Xa.objects.get_or_create(
                    name = row[0],
                    huyen_id = EXISTING_DISTRICT_ID,
                    )

def import_missing_districts_and_communes(apps, schema_editor):
    district_list = []
    district_ids = []
    commune_dict = {}
    
    # Get data of districts within Thua Thien Hue 
    with open('{}/huyen.csv'.format(DATA_DIR)) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row[7] == TTH_ID_FROM_FILE and row[6] != EXISTING_DISTRICT_ID_IN_FILE:
                district_list.append(row)
                district_ids.append(row[6])
    
    # Get data of communes within districts of Thua Thien Hue
    with open('{}/xa.csv'.format(DATA_DIR)) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row[7] in district_ids:
                current_dict = commune_dict.get(row[7], [])
                current_dict.append(row)
                commune_dict[row[7]] = current_dict
    
    # Import missing districts and communes 
    for district in district_list:
        huyen, created = Huyen.objects.get_or_create(
            name = district[0],
            tinh_id = TTH_ID_FROM_DB,
            )
        if created == True:
            for commune in commune_dict[district[6]]:
                _, _ = Xa.objects.get_or_create(
                    name = commune[0],
                    huyen_id = huyen.id,
                    )
    

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0074_auto_20201106_2122'),
    ]

    operations = [
        migrations.RunPython(import_missing_communes_for_existing_district),
        migrations.RunPython(import_missing_districts_and_communes),
    ]   

