# Raspagem de Dados do Portal da Transparência da Cidade de Itambacuri-MG

Este projeto tem como objetivo realizar a raspagem e transformação dos dados do Portal da Transparência de Itambacuri-MG para o ano de 2024. O projeto segue uma série de etapas para extrair, transformar e analisar esses dados, utilizando diversas ferramentas e bibliotecas.

## Estrutura do Projeto

1. **Raspagem de Dados (`portal_extracao.py`)**:
    - Este script realiza a raspagem dos dados do Portal da Transparência de Itambacuri-MG.
    - A raspagem é feita para obter dados referentes ao ano de 2024.
    - Os dados raspados são armazenados em um banco de dados SQLite para processamento posterior.

2. **Armazenamento no Banco SQLite (`db_sql.py`)**:
    - O script `db_sql.py` é responsável por criar e gerenciar o banco de dados SQLite.
    - Os dados extraídos são salvos em tabelas específicas dentro do banco de dados SQLite.

3. **Transformação dos Dados (`transformacao.py`)**:
    - Utilizando a biblioteca PySpark, este script realiza a transformação das colunas dos dados armazenados no SQLite.
    - As transformações incluem formatação e estruturação dos dados para análises futuras.
    - Após as transformações, os dados são salvos em uma nova tabela do banco de dados SQLite.

4. **Análise dos Dados (`analise_dados_portal.ipynb`)**:
    - As análises são realizadas em um Jupyter Notebook, onde os dados transformados são explorados e visualizados.
    - O objetivo é identificar padrões, insights e possíveis anomalias nos dados.

## Como Utilizar

### Pré-requisitos

- **Python 3.10+**
- **SQLite**
- **PySpark**
- **Jupyter Notebook**
- Instale as dependências necessárias utilizando o `pip`:
  ```bash
  pip install -r requirements.txt
