
import os
import pandas as pd
import psycopg2
from psycopg2 import sql

# --- Configurações do Banco de Dados (do docker-compose.yml) ---
DB_NAME = "megasena_db"
DB_USER = "megasena_user"
DB_PASS = "megasena_password"
DB_HOST = "localhost"
DB_PORT = "5432"

# --- Caminho do arquivo Excel ---
# O script espera que o arquivo esteja em ../data/megasena_resultados.xlsx
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, '../data/megasena_resultados.xlsx')

def create_table(conn):
    """Cria a tabela de concursos se ela não existir."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS concursos (
        id SERIAL PRIMARY KEY,
        concurso INTEGER UNIQUE NOT NULL,
        data_sorteio DATE NOT NULL,
        dezena1 INTEGER NOT NULL,
        dezena2 INTEGER NOT NULL,
        dezena3 INTEGER NOT NULL,
        dezena4 INTEGER NOT NULL,
        dezena5 INTEGER NOT NULL,
        dezena6 INTEGER NOT NULL
    );
    """
    with conn.cursor() as cur:
        cur.execute(create_table_query)
        conn.commit()
    print("Tabela 'concursos' verificada/criada com sucesso.")

def insert_data(conn, df):
    """Insere os dados do DataFrame no banco de dados, evitando duplicatas."""
    inserted_count = 0
    skipped_count = 0
    
    with conn.cursor() as cur:
        for index, row in df.iterrows():
            # Verifica se o concurso já existe
            cur.execute("SELECT id FROM concursos WHERE concurso = %s", (row['concurso'],))
            if cur.fetchone():
                skipped_count += 1
                continue

            # Insere o novo concurso
            insert_query = sql.SQL("""
                INSERT INTO concursos (concurso, data_sorteio, dezena1, dezena2, dezena3, dezena4, dezena5, dezena6)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """)
            cur.execute(insert_query, (
                row['concurso'],
                row['data_sorteio'],
                row['dezena1'],
                row['dezena2'],
                row['dezena3'],
                row['dezena4'],
                row['dezena5'],
                row['dezena6']
            ))
            inserted_count += 1
    
    conn.commit()
    print(f"{inserted_count} novos concursos inseridos.")
    print(f"{skipped_count} concursos já existentes foram ignorados.")

def main():
    """Função principal para orquestrar a leitura e inserção dos dados."""
    print("Iniciando processo de importação de dados...")

    # Verifica se o arquivo de dados existe
    if not os.path.exists(DATA_FILE):
        print(f"ERRO: Arquivo de dados não encontrado em {DATA_FILE}")
        print("Por favor, baixe o arquivo e coloque-o na pasta 'data' com o nome 'megasena_resultados.xlsx'")
        return

    # Lê o arquivo Excel
    try:
        # Com o debug, descobrimos que precisamos pular 6 linhas para chegar no cabeçalho real
        df = pd.read_excel(DATA_FILE, skiprows=6)
        print("Arquivo Excel lido com sucesso.")
    except Exception as e:
        print(f"ERRO ao ler o arquivo Excel: {e}")
        return

    # --- Limpeza e Preparação dos Dados ---
    # Renomeia as colunas para um formato padrão
    # (Isso pode precisar de ajuste dependendo do arquivo real)
    column_mapping = {
        'Concurso': 'concurso',
        'Data': 'data_sorteio',
        'bola 1': 'dezena1',
        'bola 2': 'dezena2',
        'bola 3': 'dezena3',
        'bola 4': 'dezena4',
        'bola 5': 'dezena5',
        'bola 6': 'dezena6'
    }
    df = df.rename(columns=column_mapping)

    # Garante que as colunas esperadas existem
    expected_columns = list(column_mapping.values())
    if not all(col in df.columns for col in expected_columns):
        print("ERRO: As colunas esperadas não foram encontradas no arquivo Excel.")
        print(f"Esperado: {expected_columns}")
        print(f"Encontrado: {list(df.columns)}")
        return

    # Converte a coluna de data e extrai apenas a data
        df['data_sorteio'] = pd.to_datetime(df['data_sorteio'], dayfirst=True).dt.date

    # Conecta ao banco de dados
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Conexão com o PostgreSQL estabelecida com sucesso.")
    except psycopg2.OperationalError as e:
        print(f"ERRO de conexão com o banco de dados: {e}")
        print("Verifique se o contêiner do Docker está rodando ('docker-compose up -d').")
        return

    # Roda as funções
    create_table(conn)
    insert_data(conn, df)

    # Fecha a conexão
    conn.close()
    print("Processo finalizado.")

if __name__ == "__main__":
    main()
