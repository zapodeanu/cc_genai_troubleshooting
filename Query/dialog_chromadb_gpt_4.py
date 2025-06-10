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
# noinspection PyProtectedMember
from langchain._api import LangChainDeprecationWarning
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

warnings.simplefilter("ignore", category=LangChainDeprecationWarning)  # Suppress LangChain warnings

# Load environment variables
load_dotenv('environment.env')

# Database server details
DB_SERVER = os.getenv('DB_SERVER')
DB_PORT = os.getenv('DB_PORT')
DB_COLLECTION = os.getenv('DB_COLLECTION')

# OpenAI Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Model configurations
MODEL_NAME = 'all-MiniLM-L6-v2'
OPENAI_MODEL = 'gpt-4o'

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def main():
    """
    This chatbot uses LangChain to perform similarity searches on a ChromaDB and
    responds with context-aware answers using OpenAI's GPT-4o model.
    """

    # Initialize Chroma DB Server Connection
    chroma_db_server = chromadb.HttpClient(host=DB_SERVER, port=DB_PORT)

    # Define the embedding model for vector search
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    # Connect to Chroma DB Collection
    chroma_db = Chroma(
        client=chroma_db_server,
        collection_name=DB_COLLECTION,
        embedding_function=embeddings
    )

    # Initialize OpenAI LLM
    llm = ChatOpenAI(model_name=OPENAI_MODEL, temperature=1)

    # Add memory to remember past interactions
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Create a conversational chain with memory and ChromaDB as retriever
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=chroma_db.as_retriever(),  # Automatically retrieves relevant context
        memory=memory,
        verbose=False
    )

    print("\nChatbot is ready! Type your query below. Type 'exit' to stop.\n")

    while True:
        # Get user input
        query = input("You: ").strip()

        if query.lower() in ["exit", "quit", "bye"]:
            print("\nChatbot: Goodbye! Have a great day! 👋")
            break

        # Generate response using the memory-aware conversational chain
        response = chain.invoke({"question": query})

        print(f"Chatbot: {response['answer']}\n")


if __name__ == "__main__":
    main()
