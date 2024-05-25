import os, mysql.connector, mysql.connector.pooling
from openai import OpenAI
from werkzeug.security import generate_password_hash
from datetime import datetime

# Customer vars
current_date = datetime.now().strftime('"%B %d"')
user_query: str = ''
userQueryCache: dict = {}
CLIENT_INDEX: str = 'web-application-development'
DATA_CSV: str = 'webappdev.csv'#'demo.csv'
CSV_COLUMN_NAME: str = 'School Material'
DATA_EMBEDDING_CSV: str = 'webappdev_embeddings.csv'

# OpenAI API configuration
openai_api_key: str = os.getenv('OPENAI_API_KEY')
openai_org_key: str = os.getenv('ORG_KEY')
MODERATION_API_ENDPOINT: str = 'https://api.openai.com/v1/moderations'
EMBEDDING_MODEL: str = "text-embedding-3-small" # essential! Generates 1536 dimensions Pinecone must match this!
GPT_MODEL: str =  "gpt-4o" #"gpt-4-1106-preview" #"gpt-3.5-turbo-0125" #"gpt-4-turbo" 
NUM_OF_SIMILARITIES: int = 3
OUT_TOKEN_LIMIT: int = 150
IN_TOKEN_LIMIT: int = 100
TEMP_SET: int = 0

SYSTEM_INSTRUCTIONS: str = f"""
                            This is for a student learning HTML, CSS, JavaScript, and PHP.
                            This student has little knowledge of Web Application Development, so keep that in mind.
                            Be sure to give HTML, CSS, JavaScript, and PHP examples when possible in the proper syntax and format.
                            It is important that you know the current date of today which is {current_date}.
                            We are in the the week that {current_date} is in. 
                            Many questions will be based on the most current assignments.
                            Limit reponses to {OUT_TOKEN_LIMIT} tokens. 
                            IMPORTANT: If your response contains HTML tags for examples, treat it like normal text because the browswer will render it.
                            IMPORTANT: Use ASCII examples for code snippets.
                        """

# System Parameters
instruction_Header: str = 'Follow these instructions and answer with data below\n'
data_Header: str = '\n\nAnswer the question using this data\n'
user_Question_Header: str = '\n\nAnswer this question\n'
system_instruction_trail: str = 'Based on this information only, answer the user\'s question.'

# Store customer credentials for authentication purposes in the Flask application
CUSTOMER_ID = 'cpsc@clemson.edu'
PASSWORD = '3750'

# User email/password in Flask POST matches the chatbot DB
customers: dict = {
    CUSTOMER_ID: generate_password_hash(PASSWORD)
}

# Database configuration
db_password: str = os.getenv('DB_PASS')
db_host: str = '127.0.0.1'
db_user: str = 'root'
db_database: str = 'chatbot'

# Establish database connection pool
dbconfig: dict = {
    "host": db_host,
    "user": db_user,
    "password": db_password,
    "database": db_database
}
cnxpool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "SQLPool",
    pool_size = 32,
    **dbconfig
)

# Pinecone API configuration
pinecone_api_key: str = os.getenv('PINECONE_API_KEY')
client: OpenAI = OpenAI(
    organization = openai_org_key,
    api_key = openai_api_key
)

# Check for required configuration
if not all([openai_api_key, openai_org_key, pinecone_api_key, db_host, db_user, db_password, db_database]):
    raise ValueError("Required API keys or database credentials are not set in environment variables.")
