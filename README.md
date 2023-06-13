# AthenaQueryExecutor

AthenaQueryExecutor é uma classe em Python que permite executar consultas no Amazon Athena e recuperar os resultados como um Pandas DataFrame. Essa classe utiliza a biblioteca Boto3 para interagir com o serviço Athena.

## Recursos

- Executa consultas no Amazon Athena.
- Recupera os resultados da consulta como um Pandas DataFrame.
- Trata erros na execução da consulta e fornece mensagens de erro apropriadas.

## Pré-requisitos

Antes de usar a classe AthenaQueryExecutor, verifique se você possui os seguintes pré-requisitos:

- Credenciais de conta da AWS com as permissões necessárias para acessar o Athena.
- Python 3.x instalado em seu sistema.
- Bibliotecas Python necessárias: botocore, boto3, time, pandas.

## Uso

Siga as etapas abaixo para usar a classe AthenaQueryExecutor:

1. Importe as bibliotecas necessárias:
```python
import botocore.session
import boto3
import time
import pandas as pd
```

2. Crie uma instância da classe AthenaQueryExecutor:
```python
query_executor = AthenaQueryExecutor()
```

3. Execute uma consulta:
```python
query = "SELECT * FROM sua_tabela"
database = "seu_banco_de_dados"
df = query_executor.execute_query(query, database)
```
- Substitua "sua_tabela" pelo nome da tabela que você deseja consultar.
- Substitua "seu_banco_de_dados" pelo nome do banco de dados Athena que contém a tabela.

4. Acesse os resultados da consulta:
```python
print(df.head())
```
- Isso imprimirá as primeiras linhas do DataFrame contendo os resultados da consulta.

## Personalização

Você pode personalizar o comportamento da classe AthenaQueryExecutor modificando os seguintes atributos:

- `region`: Defina a região da AWS desejada para suas consultas Athena.
- `OutputLocation`: Defina o bucket do S3 e o caminho onde os resultados da consulta devem ser armazenados.

```python
self.region = 'us-east-1'
self.athena_client = self.session.client('athena')
self.athena_client.start_query_execution(
    QueryString=query,
    QueryExecutionContext={'Database': database},
    ResultConfiguration={'OutputLocation': 's3://seu-bucket/seu-caminho'}
)
```
- Substitua "us-east-1" pelo código da região da AWS desejada.
- Substitua "seu-bucket/seu-caminho" pelo bucket do S3 e caminho onde você deseja armazenar os resultados da consulta.

## Tratamento de Erros

A classe AthenaQueryExecutor fornece tratamento de erros para falhas na execução da consulta. Se uma consulta falhar ou for cancelada, uma mensagem de erro apropriada será exibida.

```python
if status == 'SUCCEEDED':
    # Processar os resultados da consulta
else:
    error_message = response['QueryExecution']['Status']['StateChangeReason']
    print("A execução da consulta falhou ou foi cancelada. Mensagem de erro: ", error_message)
```

## Desenvolvimentos Futuros

<<<<<<< HEAD
- A atribuição dos tipos de coluna não está funcionando corretamente, especialmente com datas. Esse é um problema conhecido e será corrigido em desenvolvimentos futuros.
- O parâmetro "database" não é ideal, pois podemos (
=======
The AthenaQueryExecutor class simplifies the process of executing queries on Amazon Athena and retrieving the results as a Pandas DataFrame. You can easily integrate this class into your data analysis workflows and leverage the power of Athena for querying large datasets stored in Amazon S3.
>>>>>>> 083094b1e7d197831f3977d5df1316b03b411b69
