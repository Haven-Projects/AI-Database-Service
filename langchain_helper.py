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

def setup_llm() -> ChatGoogleGenerativeAI:
    """Initialize and return the LLM."""
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.1,
        google_api_key=os.environ.get("API_KEY"),
    )

def setup_db() -> SQLDatabase:
    """Initialize and return the SQLDatabase."""
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASS")
    db_host = os.environ.get("DB_HOST")
    db_name = os.environ.get("DB_NAME")
    return SQLDatabase.from_uri(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
        sample_rows_in_table_info=3
    )

def setup_embeddings() -> HuggingFaceEmbeddings:
    """Initialize and return the embeddings."""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def setup_prompt(example_selector, example_prompt, mysql_prompt, custom_suffix):
    """Create and return the FewShotPromptTemplate."""
    return FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=mysql_prompt,
        suffix=custom_suffix,
        input_variables=["input", "table_info"],
    )

def create_chain(llm, db, few_shots, embeddings, prompt):
    """Create and return the SQLDatabaseChain."""
    to_vectorize = [" ".join(str(value) for value in example.values()) for example in few_shots]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=2)
    return SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=prompt)

def get_few_shot_db_chain():

    ''' This is the intial approach
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
    #print(db.table_info)
    
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
    - Do NOT execute INSERT, UPDATE, DELETE, or any other non-SELECT queries.
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
    If the question is not answerable with the given tables, return "Sorry, can't help with that.".
    If the question asks for an update or modification or deletion or drop of a tableto the database, return "Sorry, can't help with that." as well.
    If question ask anything other than SELECT query, return "Sorry, can't help with that.".
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
    '''
    llm = setup_llm()
    db = setup_db()
    embeddings = setup_embeddings()
    # Prompt setup
    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )
    mysql_prompt = """
    You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use CURDATE() function to get the current date, if the question involves "today".

    CRITICAL INSTRUCTIONS:
    - Do NOT execute INSERT, UPDATE, DELETE, or any other non-SELECT queries.
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
    If the question is not answerable with the given tables, return "Sorry, can't help with that.".
    If the question asks for an update or modification or deletion or drop of a tableto the database, return "Sorry, can't help with that." as well.
    If question ask anything other than SELECT query, return "Sorry, can't help with that.".
    Question: {input}"""

    
    # Vectorstore and selector
    to_vectorize = [" ".join(str(value) for value in example.values()) for example in few_shots]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=2)
    prompt = setup_prompt(example_selector, example_prompt, mysql_prompt, custom_suffix)
    return SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=prompt)

def safe_chain_call(chain, question):
    """
    Runs the chain and intercepts non-SELECT or refusal SQL before execution.
    Returns the refusal message directly if detected.
    """
    try:
        result = chain.invoke({"query": question})
        sql_query = ""
        if "intermediate_steps" in result and result["intermediate_steps"]:
            sql_query = result["intermediate_steps"][0].get("sql_cmd", "")
        # If the SQL is not a SELECT or is a refusal message, return the message
        if not sql_query.strip().lower().startswith("select"):
            return sql_query # or "Sorry, can't help with that."
        # If the result contains a refusal message, return only the answer part
        answer = result.get("result", "")
        if answer.strip().lower().startswith("sorry, can't help"):
            return answer
        return answer or result
    except Exception as e:
        return "Sorry, can't help with that."

if __name__ == "__main__":
    chain = get_few_shot_db_chain()
    question = "How many sales have occured in last 2 weeks?" 
    print(safe_chain_call(chain, question))