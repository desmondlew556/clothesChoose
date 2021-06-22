import os, sys, django
print(os.path.dirname(os.path.abspath(__file__))[:-19])
sys.path.append(os.path.dirname(os.path.abspath(__file__))[:-19])
from collections import defaultdict

from os import path, environ
from sys import path as sys_path
from django import setup

#sys_path.append(<path to django setting.py>)
environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothesChoose.settings')
setup()
#import required models
from django_backend.models import Characteristics,GarmentMen,GarmentWomen,GarmentOthers



#JSON IO packages
import json
from json.decoder import JSONDecodeError
from django.db.models.fields.json import JSONField

#database connection
import mysql.connector

def rename_photos(source_folder,destination_folder):
    for count,filename in enumerate(os.listdir("images/"+source_folder)):
        sourceFile=os.path.abspath(os.getcwd())+"/images/"+source_folder+"/"+filename
        destFile=os.path.abspath(os.getcwd())+"/images/"+destination_folder+"/"+filename[12:]
        os.rename(sourceFile,destFile)

def add_apparel_photos():
    #connect to database

    #naming for type of clothing
    top_name = 'tops'
    bottom_name = 'bottoms'
    one_piece_name = 'one-piece'
    #mapping of folder names to characteristic names
    characteristics_dict = {
        #tops ('':top_name,)
        #normal shirt
        'sweatshirt':top_name,
        'T-shirt':top_name,
        'shirt':top_name,
        'polo shirt':top_name,
        'blouse':top_name,
        #outer-wear
        'jacket':top_name,
        'windbreaker':top_name,
        'blazer':top_name,
        'cardigan':top_name,
        'overshirt':top_name,
        'sweater':top_name,
        'coat':top_name,
        #bottoms ('':bottom_name,)
        'trouser':bottom_name,
        'jeans':bottom_name,
        'shorts':bottom_name,
        'legging':bottom_name,
        'joggers':bottom_name,
        'skirt':bottom_name,
        #one-piece ('':one_piece_name,)
        'bath robe':one_piece_name,
        'bodysuit':one_piece_name,
        'dress':one_piece_name,
        'co-ordinates':one_piece_name,
        'rompers':one_piece_name,
        'jumpsuit':one_piece_name
    }
    #photos origin directory
    saved_photos_path = "images/new_apparel_photos"
    #destination directory
    destination_photo_folder = "../../../react-frontend/src/static/clothesChoose/images/apparel"
    separator = "/"
    #list of tuples to add
    default_key_value = "Not present"
    garment_entries = defaultdict(lambda:default_key_value)
    #store list of garment characterisitcs in a list and a dictionary for inserting garment entry into database
    characteristics_list = []
    garment_characteristics = defaultdict(lambda:default_key_value)
    try:
        #go through all photos according to file structure in the origin directory
        for category in os.listdir(saved_photos_path):
            #ignore hidden files (e.g. .DStore that are not directories)
            if(is_hidden(category)==True):
                continue
            #check if characteristics is already created
            if(garment_entries[category]==default_key_value):
                print(category+" does not exist.. Adding key")
                garment_entries[category]=[]
            category_path_extension = separator+category
            current_path = saved_photos_path+category_path_extension
            destination_category_folder = os.getcwd()+destination_photo_folder+separator+category
            #Create directory for clothing category if it does not exist in the destination directory
            if(not os.path.exists(destination_category_folder)):
                print("creating directory",folder)
                os.mkdir(destination_category_folder)
            else:
                print("already exists")
            for folder in os.listdir(current_path):
                #ignore hidden files (e.g. .DStore that are not directories)
                if(is_hidden(folder)==True):
                    continue
                #if characteristics mapping is not present, log the occurrence
                try:
                    characteristics_list.append(characteristics_dict[folder])
                    characteristics_list.append(folder)
                except:
                    #IO operation
                    error_logging_file = "error_logging.json"
                    with open(error_logging_file,"r") as file:
                        try:
                            error_log = json.load(file)
                        except JSONDecodeError:
                            error_log = []
                        error_log.append(current_path+separator+folder)
                        with open(error_logging_file,"w") as file_write:
                            json_obj = json.dumps(error_log,indent = 2)
                            file_write.write(json_obj)
                    #Do not proceed if there is an error with categorizing the photo
                    continue
                destination_folder = os.getcwd()+destination_photo_folder+separator+category+separator+folder
                #Create directory for clothing category if it does not exist in the destination directory
                if(not os.path.exists(destination_folder)):
                    print("creating directory",folder)
                    os.mkdir(destination_folder)
                else:
                    print("already exists")
                folder_path_extension = category_path_extension+separator+folder
                current_folder_path = current_path+separator+folder
                for file in os.listdir(current_folder_path):
                    file_path_extension = folder_path_extension+separator+file
                    origin_file_path = os.path.abspath(os.getcwd())+separator+current_folder_path+separator+file
                    destination_file_path = os.getcwd()+destination_photo_folder+file_path_extension
                    #shift photos that are read to destination directory
                    os.rename(origin_file_path,destination_file_path)
                    #save garment entry and characteristics for mass insertion after loops.
                    garment_entries[category].append(destination_file_path)
                    garment_characteristics[destination_file_path] = [characteristics_dict[folder],folder]
                    print(origin_file_path)
                    print(destination_file_path)
                    print("\n\n")
        #find and add characteristics object that have not been created
        characteristics_set = set(characteristics_list)
        unique_characteristics_list = list(characteristics_set)
        for characteristic in unique_characteristics_list:
            if(not Characteristics.objects.filter(characteristic_name=characteristic).exists()):
                Characteristics.objects.create(characteristic_name=characteristic)
        #add garment photo entries into corresponding databases
        for category, garments_photo_links in garment_entries.items():
            if category.lower() == "men":
                for photo_link in garments_photo_links:
                    entry = GarmentMen.objects.create(image_path = photo_link)
                    for characteristic in garment_characteristics[photo_link]:
                        entry.characteristics.add(Characteristics.objects.get(characteristic_name=characteristic))
            elif category.lower() == "women":
                for photo_link in garments_photo_links:
                    entry = GarmentWomen.objects.create(image_path = photo_link)
                    for characteristic in garment_characteristics[photo_link]:
                        entry.characteristics.add(Characteristics.objects.get(characteristic_name=characteristic))
            else:
                for photo_link in garments_photo_links:
                    if(category.lower() == "unisex"):
                        garment_type = "U"
                    else:
                        garment_type = None
                    entry = GarmentOthers.objects.create(image_path = photo_link,garment_type=garment_type)
                    for characteristic in garment_characteristics[photo_link]:
                        entry.characteristics.add(Characteristics.objects.get(characteristic_name=characteristic))
    except NotADirectoryError:
        pass
    except FileNotFoundError:
        pass


def is_hidden(filepath):
    if filepath.startswith("."):
        return True
    else:
        return False

def connect_to_database():

    mydb = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="mydatabase"
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    val = [
    ('Peter', 'Lowstreet 4'),
    ('Amy', 'Apple st 652'),
    ('Hannah', 'Mountain 21'),
    ('Michael', 'Valley 345'),
    ('Sandy', 'Ocean blvd 2'),
    ('Betty', 'Green Grass 1'),
    ('Richard', 'Sky st 331'),
    ('Susan', 'One way 98'),
    ('Vicky', 'Yellow Garden 2'),
    ('Ben', 'Park Lane 38'),
    ('William', 'Central st 954'),
    ('Chuck', 'Main Road 989'),
    ('Viola', 'Sideway 1633')
    ]

    mycursor.executemany(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "was inserted.")

if __name__ == '__main__':
    destination_folder = 'women'
    source_folder = "newclothes"
    add_apparel_photos()