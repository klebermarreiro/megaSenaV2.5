# MegaSena v2.5 - Análise de Dados e IA

Este projeto utiliza dados históricos dos sorteios da Mega-Sena para realizar análises estatísticas e aplicar um modelo simples de Machine Learning para identificar padrões e gerar sugestões de jogos.

**Aviso Importante:** Este projeto é uma ferramenta de estudo e análise de dados históricos. Ele **não garante e não tem a capacidade de prever** resultados futuros. A Mega-Sena é um jogo de azar e os resultados são estatisticamente independentes.

---

## Tecnologias Utilizadas

*   **Linguagem Principal:** Python 3
*   **Banco de Dados:** PostgreSQL (rodando em um contêiner Docker)
*   **API:** FastAPI
*   **Servidor da API:** Uvicorn
*   **Análise de Dados:** Pandas, NumPy
*   **Machine Learning:** Scikit-learn (usando o algoritmo K-Means)
*   **Conector do Banco de Dados:** psycopg2
*   **Visualização de Dados:** Power BI (conectado à API)
*   **Controle de Versão:** Git & GitHub

---

## Estrutura do Projeto

*   `docker-compose.yml`: Arquivo de configuração para iniciar o banco de dados PostgreSQL com Docker de forma simples.
*   `scripts/`: Pasta que contém todos os nossos scripts Python.
    *   `requirements.txt`: Lista de todas as bibliotecas Python necessárias.
    *   `process_data.py`: Script para ler o arquivo Excel com os resultados, limpar os dados e inseri-los no banco de dados.
    *   `api.py`: Expõe os dados do banco de dados através de uma API web com FastAPI.
    *   `analysis.py`: Lê os dados do banco, realiza a análise de frequência, aplica o modelo de Machine Learning e gera as sugestões de jogos.
*   `data/`: Pasta onde o arquivo `megasena_resultados.xlsx` deve ser colocado.

---

## Como Usar

Siga os passos abaixo para configurar e executar o projeto do zero.

### Pré-requisitos

*   [Git](https://git-scm.com/)
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/)
*   [Python 3](https://www.python.org/downloads/)

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/klebermarreiro/megaSenaV2.5.git
cd megaSenaV2.5
```

### Passo 2: Iniciar o Banco de Dados

Certifique-se de que o Docker Desktop está em execução. Então, execute o comando:

```bash
docker-compose up -d
```

### Passo 3: Instalar as Dependências Python

```bash
pip install -r scripts/requirements.txt
```

### Passo 4: Popular o Banco de Dados

1.  Baixe o arquivo de resultados em Excel do site [As Loterias](https://asloterias.com.br/download-todos-resultados-mega-sena).
2.  Clique em **"Download Todos resultados da Mega Sena em Excel por ordem de sorteio"**.
3.  Salve ou mova o arquivo baixado para a pasta `data/` do projeto.
4.  Renomeie o arquivo para `megasena_resultados.xlsx`.
5.  Execute o script de processamento:

```bash
python scripts/process_data.py
```

### Passo 5: Executar a Análise e Gerar Sugestões

Para ver a análise de frequência e as sugestões de jogos, execute:

```bash
python scripts/analysis.py
```

### Passo 6: Iniciar a API

Para que o Power BI possa acessar os dados, a API precisa estar em execução. Deixe este terminal aberto.

```bash
uvicorn scripts.api:app --reload
```

A API estará disponível em `http://localhost:8000`.

### Passo 7: Conectar com o Power BI

1.  Abra o Power BI Desktop.
2.  Clique em **Obter dados > Web**.
3.  Insira a URL: `http://localhost:8000/api/concursos`.
4.  Clique em **OK** e depois em **Carregar**.
5.  Pronto! Agora você pode criar seus gráficos e dashboards com todos os dados dos sorteios.
