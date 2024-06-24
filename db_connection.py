# import sqlalchemy
# import psycopg2
# from dotenv import load_dotenv
# load_dotenv()
# import os
# # Define your database connection details
# db_url = os.getenv('POSTGRES_URI')

# # Create a SQLAlchemy engine
# engine = sqlalchemy.create_engine(db_url)

# # Establish a connection using psycopg2 for executing raw SQL queries
# connection = psycopg2.connect(db_url)

# def get_user_title_by_id(userId):
#     # Define an SQL query to select the user_title based on userId
#     select_query = f"SELECT user_title FROM system_info WHERE user_process_id = '{userId}'"

#     try:
#         # Execute the query
#         with connection, connection.cursor() as cursor:
#             cursor.execute(select_query)

#             # Fetch and print the user_title
#             user_title = cursor.fetchone()
#             if user_title:
#                 print(f"user_title for userId {userId}: {user_title[0]}")
#             else:
#                 print(f"No user_title found for userId {userId}")

#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     # Provide the userId when running the script
#     user_id = input("Enter the userId: ")
#     get_user_title_by_id(user_id)
    
#     # Close the database connection
#     connection.close()

import sqlalchemy
import psycopg2
from dotenv import load_dotenv
load_dotenv()
import os
# import MySQLdb

# connection = MySQLdb.connect(
#   host= os.getenv("DB_HOST"),
#   user=os.getenv("DB_USERNAME"),
#   passwd= os.getenv("DB_PASSWORD"),
#   db= os.getenv("DB_NAME"),
#   autocommit = True,
#   ssl_mode = "VERIFY_IDENTITY",
#   ssl      = {
#     "ca": "/etc/ssl/cert.pem"
#   }
# )
import mysql.connector

connection= mysql.connector.connect(
  host=os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  password=os.getenv("DB_PASSWORD")
)

# print(connection)

# Define your database connection details
# db_url = os.getenv('POSTGRES_URI')

# Create a SQLAlchemy engine
# print(db_url)
# engine = sqlalchemy.create_engine(db_url)

# Establish a connection using psycopg2 for executing raw SQL queries
# connection = psycopg2.connect(db_url)

def get_all_data():
    # Define an SQL query to select all data from the system_info table
    select_query = "SELECT * FROM system_info"

    try:
        # Execute the query
        with connection, connection.cursor() as cursor:
            cursor.execute(select_query)

            # Fetch and print all rows
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No data found in the system_info table")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_all_data()

    # Close the database connection
    connection.close()

