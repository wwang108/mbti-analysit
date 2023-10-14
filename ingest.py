from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import DeepLake

import os

#OPENAI key

# Write a vector store
documents = TextLoader("documents/").load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
db = DeepLake(
    dataset_path="./my_deeplake/", embedding=embeddings, overwrite=True
)
db.add_documents(docs)



