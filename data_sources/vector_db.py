from pinecone import Pinecone, ServerlessSpec
from langchain.vectorstores import Pinecone
import time
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.chains import RetrievalQA
# from langchain.llms import OpenAI
# import json


class Vector_DB():
    def __init__(self, PINECONE_API_KEY):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)    

    def emb(self, data):
        self.embeddings = self.pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[d['text'] for d in data],
            parameters={"input_type": "passage", "truncate": "END"}
        )
        return self.embeddings

    def create_index(self, index_name):        
        if not self.pc.has_index(index_name):
            self.pc.create_index(
                name=index_name,
                dimension=1024,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud='aws', 
                    region='us-east-1'
                ) 
            ) 
        print("creating index...")
        while not self.pc.describe_index(index_name).status['ready']:
            time.sleep(1)

    def upload_embeddings(self, index_name, vector_namespace, data, embeddings):
        index = self.pc.Index(index_name)
        records = []
        for d, e in zip(data, embeddings):
            records.append({
                "id": d['id'],
                "values": e['values'],
                "metadata": {'text': d['text']}
            })

        index.upsert(
            vectors=records,
            namespace=vector_namespace
        )
        time.sleep(10)
        return index.describe_index_stats()

    def search(self, index_name, query):
        query_embedding = self.pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[query],
            parameters={
                "input_type": "query"
            }
        )

        index = self.pc.Index(index_name)
        results = index.query(
            namespace="example-namespace",
            vector=query_embedding[0].values,
            top_k=3,
            include_values=False,
            include_metadata=True
        )

        print(results)
        return results
