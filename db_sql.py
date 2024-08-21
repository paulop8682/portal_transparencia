import sqlite3

# Conectando ao banco de dados
conn = sqlite3.connect('portal.db')
cursor = conn.cursor()

# Criando a tabela se ela não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS DT_PORTAL_BRONZE (
        id INTEGER PRIMARY KEY,
        NOME TEXT,
        CARGO TEXT,
        SALARIO TEXT,
        TIPO_VINCULO TEXT,
        DATA_CONTRATACAO TEXT,
        DATA_DEMISSAO TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS DT_PORTAL_PRATA (
        id INTEGER PRIMARY KEY,
        NOME TEXT,
        CARGO TEXT,
        SALARIO DOUBLE,
        TIPO_VINCULO TEXT,
        DATA_CONTRATACAO DATE,
        DATA_DEMISSAO TEXT
    )
''')


# Salvando as mudanças
conn.commit()
conn.close()