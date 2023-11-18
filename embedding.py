import os 
from dotenv import load_dotenv
from langchain.llms import OpenAI
# text stuff
from langchain.document_loaders import TextLoader
from langchain.text_splitter import NLTKTextSplitter
from langchain.embeddings import OpenAIEmbeddings
# vector store stuff
from langchain.vectorstores import Chroma
from langchain.agents.agent_toolkits import (create_vectorstore_agent, VectorStoreToolkit, VectorStoreInfo)
# ui stuff
import streamlit as st



#### PRELIMINARY ####

# initialize key
load_dotenv()
OpenAI.api_key = os.environ['OPENAI_API_KEY']

# sets llm **creativity**
llm = OpenAI(temperature=0.5, verbose=True)
embeddings = OpenAIEmbeddings()

# loads cleaned text file
file_path = 'C:\Users\devmp\Desktop\AmazonPrimeGPT\info.json'

loader = TextLoader(file_path)
documents = loader.load()

# splits by sentence and stores in chroma
nltk_text_splitter = NLTKTextSplitter(chunk_size=1000)
docs = nltk_text_splitter.create_documents([text])
vectordb = Chroma.from_documents(documents=docs, embedding=embeddings)

# calling an agent to help out
vectorstore_info = VectorStoreInfo(name='ChorasDB', description='Course Data', vectorstore=vectordb)
toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)
agent = create_vectorstore_agent(llm=llm, toolkit=toolkit, verbose=True)



#### MAIN ####

st.title('🌸 Choras: Your AI Academic Advisor')
st.divider()

prompt = st.text_input('Let me help you find a class:')
st.caption('Ask \"What\'s a 4 credit class about Architecture that I can take in the mornings?\"')

if prompt:
    response = agent.run(prompt)
    st.write(response)

    st.divider()
    with st.expander('Similarity Search'):
        search = vectordb.similarity_search_with_score(prompt)
        st.write(search[0][0].page_content)