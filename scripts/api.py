import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI

# --- Configurações do Banco de Dados (copiado de process_data.py) ---
DB_NAME = "megasena_db"
DB_USER = "megasena_user"
DB_PASS = "megasena_password"
DB_HOST = "localhost"
DB_PORT = "5432"

# Cria a aplicação FastAPI
app = FastAPI()

def get_db_connection():
    """Cria e retorna uma nova conexão com o banco de dados."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

@app.get("/api/concursos")
def get_concursos():
    """Endpoint para buscar todos os concursos do banco de dados."""
    conn = None
    try:
        conn = get_db_connection()
        # Usamos RealDictCursor para que o resultado venha como um dicionário (ótimo para JSON)
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM concursos ORDER BY concurso ASC")
            concursos = cur.fetchall()
        return concursos
    except Exception as e:
        # Em caso de erro, retorna uma mensagem de erro (em um app real, isso teria mais tratamento)
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()
