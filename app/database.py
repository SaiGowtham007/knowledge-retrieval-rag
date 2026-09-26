import psycopg

def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="knowledge_rag",
        user="rag_user",
        password="rag_password"
    )   