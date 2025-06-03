
# All import statements from the notebook
from few_shots import few_shots
# Google Generative AI imports
#from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# Standard library
import os

# Custom module
#from secret_key import API_KEY

# LangChain core imports
from langchain.utilities import SQLDatabase
from langchain.prompts import PromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts import SemanticSimilarityExampleSelector

# LangChain experimental
from langchain_experimental.sql import SQLDatabaseChain

# LangChain chains and prompts
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt

# Embeddings and Vector stores
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

from dotenv import load_dotenv
load_dotenv()


def get_free_shot_db_chain():
    # intialize the Google Generative AI model
    llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.1,
    google_api_key= os.environ.get("API_KEY"),
    )
   

    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASS")
    db_host = os.environ.get("DB_HOST")
    db_name = os.environ.get("DB_NAME")

    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}", sample_rows_in_table_info=3)

    
    # intializing the embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Few-shot examples for the prompt
    to_vectorize = [" ".join(str(value) for value in example.values()) for example in few_shots]
    
    # Creating vector store from the few-shot examples
    vectorstore = Chroma.from_texts(
    to_vectorize,
    embeddings,
    metadatas=few_shots
    )
    
    # Example selector for the few-shot prompt
    example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=2
    )
    
    # Creating the SQLDatabaseChain with the LLM, database, and example selector
    example_prompt = PromptTemplate(
    input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
    template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )
    
    # using custome prompt to avoid markdown formatting
    mysql_prompt = """
    You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use CURDATE() function to get the current date, if the question involves "today".

    CRITICAL INSTRUCTIONS:
    - Do NOT use markdown formatting
    - Do NOT use backticks (```)
    - Do NOT use code blocks
    - Return ONLY plain SQL
    - Never wrap SQL in ```sql``` tags
    """
    
    custom_suffix = """
    Only use the following tables:
    {table_info}

    REMEMBER: Return ONLY plain SQL without any formatting, backticks, or code blocks.

    Question: {input}"""

    few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=mysql_prompt,
    suffix=custom_suffix,
    input_variables=["input", "table_info"], #These variables are used in the prefix and suffix
    )
    
    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)   
    return chain

if __name__ == "__main__":
    chain = get_free_shot_db_chain()
    print(chain("What items are in the inventory?"))