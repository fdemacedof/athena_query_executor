# Athena Query Executor

O Athena Query Executor é uma classe Python que fornece uma maneira conveniente de executar consultas no Amazon Athena e recuperar os resultados como um DataFrame do Pandas.

## Pré-requisitos

- Python 3.6 ou superior
- AWS CLI instalado e configurado com credenciais válidas

## Instalação

1. Clone o repositório ou faça o download do arquivo `athena_query_executor.py`.
2. Instale as dependências necessárias executando o seguinte comando:

   ```
   pip install botocore boto3 pandas
   ```

## Uso

1. Importe a classe `AthenaQueryExecutor` no seu script Python:

   ```python
   from athena_query_executor import AthenaQueryExecutor
   ```

2. Crie uma instância da classe `AthenaQueryExecutor`:

   ```python
   executor = AthenaQueryExecutor(output_location='<output_location>', region='<aws_region>')
   ```

   - `output_location` (opcional): O local no bucket S3 onde os resultados da consulta serão armazenados. Se não for fornecido, será solicitado que o usuário informe o local de saída.
   - `region` (opcional): A região da AWS onde o Athena está localizado. Se não for fornecido, será solicitado que o usuário informe a região.

3. Execute uma consulta chamando o método `execute_query`:

   ```python
   query = "SELECT * FROM sua_tabela"
   database = "seu_banco_de_dados"

   result_df = executor.execute_query(query, database)
   ```

   - `query`: A consulta SQL a ser executada.
   - `database`: O nome do banco de dados do Athena onde a consulta será executada.

4. Utilize o DataFrame `result_df` do Pandas para processar e analisar os resultados da consulta.

## Desenvolvimento Futuro

- Melhoria na detecção de datas: A versão atual do `AthenaQueryExecutor` não possui detecção avançada de datas. Em versões futuras, a detecção de tipos de dados para datas será aprimorada.
- Execução de várias consultas de uma vez: Em versões futuras, a opção de executar várias consultas de uma só vez será adicionada.
- Certifique-se de fornecer as informações necessárias, como a localização de saída e a região da AWS, ao criar uma instância da classe `AthenaQueryExecutor`.