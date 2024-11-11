from langchain_community.utilities import SQLDatabase
import json

class SQL_DB():

    def __init__(self, DATABASE_NAME, DATABASE_PASSWORD, config_path="../configs/database_config.json"):
        with open(config_path) as db_config:
            db_config = json.load(db_config)
            db_credentials = db_config["DATABASE_URI"].format(DATABASE_NAME, DATABASE_PASSWORD, DATABASE_NAME)
        self.db = SQLDatabase.from_uri(db_credentials)

    def query_db(self, query):
        try:
            results = self.db.run(query)
            return results
        except Exception as e:
            print("Error:", e)
            return None
