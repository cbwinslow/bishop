import os
import psycopg2
import weaviate
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import Weaviate

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    conn = psycopg2.connect(
        host=os.environ.get("PG_HOST", "localhost"),
        database=os.environ.get("PG_DATABASE", "agent_zero"),
        user=os.environ.get("PG_USER", "user"),
        password=os.environ.get("PG_PASSWORD", "password")
    )
    return conn

def init_db():
    """Initializes the database schema."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create tables for agent states, logs, etc.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_states (
            agent_id TEXT PRIMARY KEY,
            state TEXT NOT NULL,
            timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            log_id SERIAL PRIMARY KEY,
            agent_id TEXT NOT NULL,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_id) REFERENCES agent_states (agent_id)
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()

def get_weaviate_client():
    """Initializes and returns a Weaviate client."""
    client = weaviate.connect_to_local()
    return client

def get_vector_store():
    """Initializes and returns a Weaviate vector store."""
    client = get_weaviate_client()
    embeddings = OllamaEmbeddings(model="gemma:2b")
    vector_store = Weaviate(client, "AgentZero", "content", embedding=embeddings)
    return vector_store
