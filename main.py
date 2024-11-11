import os
from dotenv import dotenv_values
from data_sources.sql_db import SQL_DB
from data_sources.vector_db import Vector_DB
from langchain_prompts.prompt_templates import data_source_selection_prompt_template
from utils.GenAIModel import GenAIModel
# from utils.response_formatter import format_response

env = dotenv_values(".env")

os.environ["AI21_API_KEY"] = env["AI21_API_KEY"]
genai_model = GenAIModel(env["OPENAI_API_KEY"])
sql_db = SQL_DB(env["DATABASE_NAME"], env["DATABASE_PASSWORD"], config_path="configs/database_config.json")
vec_db = Vector_DB(env["PINECONE_API_KEY"])


def get_answer(user_query):
    # ask what all databases to request
    sql_query = genai_model.generate_sql_query(user_query)

    data = sql_db.query_db(sql_query)
    response = GenAIModel.
    # formatted_response = format_response(data)
    return response

query = "What are the recent transactions for customer C001?"
answer = get_answer(query)
print(answer)
