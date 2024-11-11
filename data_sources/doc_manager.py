import os
from langchain.document_loaders import PyPDFLoader, WebBaseLoader, UnstructuredHTMLLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_ai21 import AI21SemanticTextSplitter


class DocManager():
    def __init__(self):
        """Takes in list of document paths"""
        self.chunk_size = 1000
    
    def filter_short_pages(documents, min_length=30): 
        filtered_documents = [] 
        for doc in documents: 
            if len(doc.page_content) >= min_length: 
                filtered_documents.append(doc) 
        return filtered_documents
    
    def split(self, documents):
        semantic_text_splitter = AI21SemanticTextSplitter(chunk_size=self.chunk_size)
        documents = self.filter_short_pages(documents)
        documents = semantic_text_splitter.split_documents(documents)

    def load_pdf(self, pdf_path):
        pdf_loader = PyPDFLoader(pdf_path)
        pdf = pdf_loader.load()
        return pdf

    def load_web(self, url):
        web_loader = WebBaseLoader(url)
        web_content = web_loader.load()
        return web_content

    def load_docx(self, docx_path):
        docx_loader = Docx2txtLoader(docx_path)
        docx_content = docx_loader.load()
        return docx_content

    def load_html(self, html_path):
        html_loader = UnstructuredHTMLLoader(html_path)
        html_content = html_loader.load()
        return html_content

    def load_txt(self, txt_path):
        txt_loader = UnstructuredHTMLLoader(txt_path)
        txt_content = txt_loader.load()
        return txt_content


    def load_data(self, data_path="data/"):
        loaders = {
            '.pdf': PyPDFLoader,
            '.html': UnstructuredHTMLLoader,
            '.htm': UnstructuredHTMLLoader,
            '.docx': Docx2txtLoader,
            '.txt': UnstructuredHTMLLoader,
        }

        all_documents = []
        
        for root, _, files in os.walk(data_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[-1].lower()

                loader_class = loaders.get(file_extension)
                if loader_class:
                    loader = loader_class(file_path)
                    documents = loader.load()
                    all_documents.extend(documents)
                else:
                    print(f"No loader available for file type: {file_extension}")

        return all_documents

# # Example usage
# data_path = "path_to_your_folder"
# documents = load_data(data_path)
# for doc in documents:
#     print(doc)