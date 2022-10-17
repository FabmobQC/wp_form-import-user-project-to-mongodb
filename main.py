#!/usr/bin/python
# Script to import field name from WP Form on Wordpress Mysql DB to MongoDB

import json
import uuid
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

#mycursor.execute("SELECT COUNT(wp_tc2c36s7fq_wpforms_entry_fields.id) FROM `wp_tc2c36s7fq_wpforms_entry_fields` WHERE wp_tc2c36s7fq_wpforms_entry_fields.form_id = 25100")


def update_user_project(mysql_c,  mongodb_c, form_id, uuid_field_id, project_field_id):

    mysql_c.execute("SELECT * FROM `wp_tc2c36s7fq_wpforms_entries` WHERE form_id={}".format(form_id))
    entries = mycursor.fetchall()

    for entrie in entries:
        user_uuid = ""
        project = ""


        try:
            user_uuid = json.loads(entrie[8])[uuid_field_id]['value']
        except:
            print("Error retrieving user id for entry {}".format(str(entrie)))
        
        try:
            if user_uuid != "":
                project = json.loads(entrie[8])[project_field_id]['value']
                if user_uuid != "" and project != "":
                    mongodb_c.Stage_Profiles.update({"user_id": uuid.UUID(user_uuid)}, {"$set": { "project_name": project}})
        except:
            print("Error retrieving user {} project".format(str(user_uuid)))

        if user_uuid != "" and project != "":
            print("User {} has project {}".format(user_uuid, project))



update_user_project(mycursor, mongodb, "25100", "14", "28")
update_user_project(mycursor, mongodb, "25278", "14", "24")

