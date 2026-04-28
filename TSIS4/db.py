import psycopg2

# Update these with your actual PostgreSQL credentials
DB_CONFIG = {
    "database": "leaderboard",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
}

def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.set_client_encoding('UTF8') # Explicitly set encoding
    return conn