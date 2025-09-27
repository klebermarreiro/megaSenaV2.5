import pandas as pd
import numpy as np
import psycopg2
from collections import Counter
from sklearn.cluster import KMeans

# --- Configurações do Banco de Dados ---
DB_NAME = "megasena_db"
DB_USER = "megasena_user"
DB_PASS = "megasena_password"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_all_data():
    """Busca todos os dados de concursos do banco e retorna como um DataFrame pandas."""
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    query = "SELECT * FROM concursos;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    # Garante que as dezenas sejam tratadas como números inteiros
    for i in range(1, 7):
        df[f'dezena{i}'] = pd.to_numeric(df[f'dezena{i}'])
    return df

def analyze_frequencies(df):
    """Analisa e imprime a frequência dos números."""
    print("\n--- Análise de Frequência dos Números ---")
    # Coleta todas as dezenas em uma única lista
    all_numbers = df[['dezena1', 'dezena2', 'dezena3', 'dezena4', 'dezena5', 'dezena6']].values.flatten()
    
    # Conta a ocorrência de cada número
    number_counts = Counter(all_numbers)
    
    print("\nOs 10 números que MAIS saíram na história:")
    for number, count in number_counts.most_common(10):
        print(f"Número {number}: {count} vezes")
        
    print("\nOs 10 números que MENOS saíram na história:")
    for number, count in number_counts.most_common()[-10:]:
        print(f"Número {number}: {count} vezes")
    
    return number_counts

def run_ml_clustering(df):
    """Roda o algoritmo K-Means para encontrar padrões (clusters) de jogos."""
    print("\n--- Análise de Machine Learning (Clusterização) ---")
    # Pega apenas as dezenas para o modelo de ML
    X = df[['dezena1', 'dezena2', 'dezena3', 'dezena4', 'dezena5', 'dezena6']].values
    
    # Vamos criar 8 clusters. Este número é arbitrário e pode ser ajustado.
    n_clusters = 8
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10) # n_init para evitar avisos
    kmeans.fit(X)
    
    print(f"{n_clusters} padrões (clusters) de jogos foram identificados.")
    print("Os centros desses padrões (jogos 'médios' de cada grupo) são:")
    
    # Arredonda e converte os centros dos clusters para inteiros para que pareçam jogos reais
    cluster_centers = np.round(kmeans.cluster_centers_).astype(int)
    for i, center in enumerate(cluster_centers):
        # Ordena os números para melhor visualização
        sorted_center = sorted(center)
        print(f"Padrão {i + 1}: {sorted_center}")
        
    return cluster_centers

def generate_suggestions(number_counts, cluster_centers):
    """Gera 3 sugestões de jogos com base nas análises."""
    print("\n--- Sugestões de Jogos ---")

    # Lógica 1: Jogo com os 6 números mais "quentes" (que mais saem)
    hot_numbers = [num for num, count in number_counts.most_common(6)]
    print(f"Sugestão 1 (Números Quentes): {sorted(hot_numbers)}")

    # Lógica 2: Jogo com os 6 números mais "frios" (que menos saem)
    cold_numbers = [num for num, count in number_counts.most_common()[-6:]]
    print(f"Sugestão 2 (Números Frios):   {sorted(cold_numbers)}")

    # Lógica 3: Jogo inspirado em um dos padrões encontrados pelo Machine Learning
    # Vamos pegar o primeiro centro de cluster como inspiração
    ml_game = sorted(cluster_centers[0])
    print(f"Sugestão 3 (Inspirado em IA): {ml_game}")


if __name__ == "__main__":
    print("Iniciando análise completa dos dados da Mega-Sena...")
    try:
        main_df = get_all_data()
        print(f"{len(main_df)} concursos carregados do banco de dados.")
        
        # Roda as análises
        counts = analyze_frequencies(main_df)
        clusters = run_ml_clustering(main_df)
        
        # Gera as sugestões
        generate_suggestions(counts, clusters)

    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
        print("Verifique se o banco de dados está acessível e se o script 'process_data.py' foi executado com sucesso.")

    print("\nAnálise finalizada.")
