import boto3
import psycopg2

def read_from_s3():
    # Replace 'your_bucket_name' with the name of your S3 bucket
    bucket_name = 'godigitalproj'
    # Replace 'your_file_key' with the key of the file in your S3 bucket
    file_key = 'sample_data.csv'

    # Create an S3 client
    s3 = boto3.client('s3')

    # Read the file from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    data = response['Body'].read().decode('utf-8')
    
    return data

def push_to_rds(data):
    # Replace the connection parameters with your RDS details
    connection = psycopg2.connect(
        user='admin',
        password='password',
        host='go-digital-1.clwc628ko6a4.us-east-1.rds.amazonaws.com',
        port=3306,
        database='go-digital-1'
    )

    cursor = connection.cursor()
    
    # Check if the table exists
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'Akash')")
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        # Create the table if it doesn't exist
        create_table_query = """
        CREATE TABLE Akash (
            id SERIAL PRIMARY KEY,
            column_name TEXT
        )
        """
        cursor.execute(create_table_query)
        print("Table 'Akash' created successfully")

    # Insert data into the table
    insert_query = "INSERT INTO Akash (column_name) VALUES (%s)"

    try:
        cursor.execute(insert_query, (data,))
        connection.commit()
        print("Data pushed to RDS successfully")
    except Exception as e:
        connection.rollback()
        print("Failed to push data to RDS:", e)
    finally:
        cursor.close()
        connection.close()


def push_to_glue_database(data):
    # Code to push data to Glue Database
    print("data push to glue db")

def main():
    # Read data from S3
    data = read_from_s3()
    
    # Try pushing data to RDS
    try:
        push_to_rds(data)
        print("Data pushed to RDS successfully")
    except Exception as e:
        print("Failed to push data to RDS:", e)
        # If pushing to RDS fails, try pushing to Glue Database
        try:
            push_to_glue_database(data)
            print("Data pushed to Glue Database successfully")
        except Exception as e:
            print("Failed to push data to Glue Database:", e)

if __name__ == "__main__":
    main()
