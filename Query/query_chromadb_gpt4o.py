#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2025 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Gabriel Zapodeanu TME, ENB"
__email__ = "gzapodea@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2025 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import os
import warnings
import chromadb

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
# noinspection PyProtectedMember
from langchain._api import LangChainDeprecationWarning

warnings.simplefilter("ignore", category=LangChainDeprecationWarning)  # to disable LangChain warnings
os.chdir('../')

load_dotenv('environment.env')

# database server details
DB_SERVER = os.getenv('DB_SERVER')
DB_PORT = int(os.getenv('DB_PORT'))
DB_COLLECTION = os.getenv('DB_COLLECTION')

# OpenAI key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

MODEL_NAME = 'all-MiniLM-L6-v2'
OPENAI_MODEL = 'gpt-4o'

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def main():
    """
    A conversational app for network troubleshooting, powered by LangChain, that retrieves similarity matches
    from ChromaDB and generates responses using OpenAI's GPT-4o.
    """

    # Chroma DB server details and connection
    chroma_db_server = chromadb.HttpClient(host=DB_SERVER, port=DB_PORT)

    # define the embeddings model
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    # Chroma DB connection to server and collection
    chroma_db = Chroma(
        client=chroma_db_server,
        collection_name=DB_COLLECTION,
        embedding_function=embeddings
    )

    # define retriever from Chroma DB and number of proximity matches
    retriever = chroma_db.as_retriever(search_kwargs={"k": 8})

    # define the LLM used - OpenAI, model 'gpt-4o'
    llm = ChatOpenAI(model_name=OPENAI_MODEL, temperature=1)

    # define the conversational messages/memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    # define the conversational retrieval chain
    conversational_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        verbose=False
    )

    print('\nHi, I am your IssuePilot! Enter your query or space to end.\n')

    while True:
        # Prompt user for input
        query = input("Your input: ").strip()

        if query == '' or query == ' ':
            print('\nEnding IssuePilot. Goodbye!\n')
            break

        # Generate response using Conversational Retrieval Chain
        response = conversational_chain.invoke({"question": query})

        print('IssuePilot: ' + response['answer'] + '\n')

    return


if __name__ == "__main__":
    main()
