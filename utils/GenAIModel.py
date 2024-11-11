from langchain_openai import OpenAI
from ..langchain_prompts.prompt_templates import sql_query_prompt_template, data_source_selection_prompt_template, get_answer_prompt_template


class GenAIModel():
    def __init__(self, OpenAI_KEY):
        self.llm = OpenAI(
            model="gpt-3.5-turbo-instruct",
            temperature=0, 
            openai_api_key = OpenAI_KEY
        )

    def select_data_source(self, _user_query:str):
        data_source_selection_prompt_template.format(question=str(_user_query))

    def generate_sql_query(self, _prompt:str):
        formatted_prompt = sql_query_prompt_template.format(question=str(_prompt))
        sql_query = self.llm(formatted_prompt)
        return sql_query.strip()

    def get_answer(self, _prompt:str, _data, _datasource):
        formatted_prompt = get_answer_prompt_template.format(question=str(_prompt), data=str(_data), datasource=str(_datasource))
        answer = self.llm(formatted_prompt)
        return answer
