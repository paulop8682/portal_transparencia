from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col, to_date, regexp_replace

# Caminho para o banco de dados SQLite
db_path = "/home/sdna/Documents/python_portal_transparencia/portal.db"
jdbc_url = f"jdbc:sqlite:{db_path}"

# Nome da tabela no banco de dados SQLite
#precisei copiar o arquivo jar jdbc para a pasta spark\jars 

# Inicialize a SparkSession
spark = SparkSession.builder \
    .appName("PySpark com SQLite via JDBC") \
    .config("spark.jars.packages", "org.xerial:sqlite-jdbc:3.41.2.1") \
    .getOrCreate()

# Leia os dados da tabela do SQLite usando JDBC
try:
    df = spark.read \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", "DT_PORTAL_BRONZE") \
        .option("driver", "org.sqlite.JDBC") \
        .load()
    
    #Transformacao variaveis
    df = df.withColumn('SALARIO', regexp_replace('SALARIO', '\.', '')) \
        .withColumn('SALARIO', regexp_replace('SALARIO', 'R\$.', '')) \
            .withColumn('SALARIO', regexp_replace('SALARIO', ',', '\.')) 
 
    df = df.withColumn("SALARIO",df.SALARIO.cast('double')) \
        .withColumn("DATA_CONTRATACAO", to_date(df["DATA_CONTRATACAO"], "dd/MM/yyyy"))   

    df.write \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", "DT_PORTAL_PRATA") \
        .option("driver", "org.sqlite.JDBC") \
        .mode("append") \
        .save()        

    # Mostre os dados lidos
    df.show()
except Exception as e:
    print("Erro ao ler os dados com JDBC:", e)
finally:
    # Feche a SparkSession
    spark.stop()
