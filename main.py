#!/usr/bin/python
# Script to import field name from WP Form on Wordpress Mysql DB to MongoDB

import json
import mysql.connector
from pymongo import MongoClient


config_file = open('.env')
config_data = json.load(config_file)

client = MongoClient(config_data["databases"]["mongodb"]["url"])
mongodb = client.Stage_database


mydb = mysql.connector.connect(
  host=config_data["databases"]["mysql"]["host"],
  user=config_data["databases"]["mysql"]["user"],
  password=config_data["databases"]["mysql"]["password"],
  database=config_data["databases"]["mysql"]["dbname"]
)

# Select all entries from the french form

mycursor = mydb.cursor()

mycursor.execute("SELECT COUNT(wp_tc2c36s7fq_wpforms_entry_fields.id) FROM `wp_tc2c36s7fq_wpforms_entry_fields` WHERE wp_tc2c36s7fq_wpforms_entry_fields.form_id = 25100")

myresult = mycursor.fetchall()


for x in myresult:
  print(x)

