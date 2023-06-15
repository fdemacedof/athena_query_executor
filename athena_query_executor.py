import botocore.session
import boto3
import time
import pandas as pd

class AthenaQueryExecutor:
    def __init__(self, output_location=None, region=None):
        # Create a botocore session to load the credentials file
        self.botocore_session = botocore.session.Session()

        # Retrieve the credentials from the [default] profile in the AWS credentials file
        self.credentials = self.botocore_session.get_credentials()

        # Check if the credentials are valid
        if self.credentials is None:
            print("No valid AWS credentials found.")
            exit(1)

        # Retrieve the session token, access key, and secret access key
        self.session_token = self.credentials.token
        self.access_key = self.credentials.access_key
        self.secret_key = self.credentials.secret_key

        if output_location is None:
            # Ask the user to enter the output location
            output_location = input("Enter the output location: ")
        self.output_location = output_location

        # Set the AWS region
        if region is None:
            region = input("Enter region:")    
        self.region = region

        # Create a session with the retrieved credentials and region
        self.session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            aws_session_token=self.session_token,
            region_name=self.region
        )

        # Create an Athena client using the session
        self.athena_client = self.session.client('athena')

    def execute_query(self, query, database, n_tokens=1):
        # Start the Athena query execution
        response = self.athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': database
            },
            ResultConfiguration={
                'OutputLocation': self.output_location
            }
        )

        # Get the query execution ID
        query_execution_id = response['QueryExecutionId']

        # Wait for the query to complete
        while True:
            response = self.athena_client.get_query_execution(QueryExecutionId=query_execution_id)
            status = response['QueryExecution']['Status']['State']

            if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break

            time.sleep(1)

        # Check if the query execution was successful
        if status == 'SUCCEEDED':
            # Get the results of the query
            results_response = self.athena_client.get_query_results(QueryExecutionId=query_execution_id)

            # Extract column names from the results
            columns = [col['Label'] for col in results_response['ResultSet']['ResultSetMetadata']['ColumnInfo']]

            # Extract row data from the results
            rows = []
            next_token = None
            tokens_used = 0

            while True:
                if next_token and tokens_used >= n_tokens:
                    break

                if next_token:
                    results_response = self.athena_client.get_query_results(
                        QueryExecutionId=query_execution_id,
                        NextToken=next_token
                    )
                else:
                    results_response = self.athena_client.get_query_results(QueryExecutionId=query_execution_id)

                for row in results_response['ResultSet']['Rows'][1:]:
                    data = row.get('Data', [])
                    values = [col.get('VarCharValue', '') for col in data]
                    rows.append(values)

                if 'NextToken' in results_response:
                    next_token = results_response['NextToken']
                    tokens_used += 1
                else:
                    break

            # Create a Pandas DataFrame from the results
            df = pd.DataFrame(rows, columns=columns)

            # Detect and assign the correct data types to DataFrame columns
            for col in columns:
                col_data = df[col]
                dtype = self.detect_column_type(col_data)
                if dtype == 'datetime':
                    df[col] = pd.to_datetime(col_data)
                else:
                    df[col] = col_data.astype(dtype)

                # Return the DataFrame containing the query results
                return df

        else:
            error_message = response['QueryExecution']['Status']['StateChangeReason']
            print("Query execution failed or was cancelled. Error message: ", error_message)
            return None

    def detect_column_type(self, column_data):
        # Detect the data type of the column
        types = [int, float]

        for dtype in types:
            try:
                column_data.astype(dtype)
                return dtype
            except (ValueError, TypeError):
                continue

        if self.is_timestamp(column_data):
            return 'datetime'
            
        # If no valid type is found, default to object
        return object


    def is_timestamp(self, value):
        try:
            pd.to_datetime(value)
            return True
        except (ValueError, TypeError):
            return False