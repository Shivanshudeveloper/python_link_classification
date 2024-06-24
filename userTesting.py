import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# Retrieve database credentials from environment variables
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# Define the connection string for SQLAlchemy
connection_string = f'mysql+mysqlconnector://{db_username}:{db_password}@{db_host}/{db_name}'

# Connect to the database using mysql.connector
conn = mysql.connector.connect(
    user=db_username,
    password=db_password,
    host=db_host,
    database=db_name
)

# Load user activity data
query = """
SELECT * FROM user_activity
WHERE timestamp BETWEEN '2023-01-01 09:00:00' AND '2023-01-01 18:00:00'
"""
df = pd.read_sql_query(query, conn)

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Define the start and end of the workday
start_time = datetime.strptime('09:00:00', '%H:%M:%S').time()
end_time = datetime.strptime('18:00:00', '%H:%M:%S').time()

# Initialize an empty list to store productivity records
productivity_records = []

# Process data per user
for user_id, user_data in df.groupby('user_uid'):
    user_data = user_data.sort_values(by='timestamp')
    current_hour = user_data.iloc[0]['timestamp'].replace(minute=0, second=0, microsecond=0)
    
    while current_hour.time() < end_time:
        next_hour = current_hour + timedelta(hours=1)
        hour_data = user_data[(user_data['timestamp'] >= current_hour) & (user_data['timestamp'] < next_hour)]
        
        if not hour_data.empty:
            productive_count = sum(hour_data['productivity_status'] == 'productive')
            unproductive_count = sum(hour_data['productivity_status'] == 'unproductive')
            core_productive_count = sum(hour_data['productivity_status'] == 'core productive')
            away_count = sum(hour_data['productivity_status'] == 'away')
            idle_count = sum(hour_data['productivity_status'] == 'idle')
            
            total_count = len(hour_data)
            if total_count > 0:
                productivity_percent = {
                    'core productive': (core_productive_count / total_count) * 100,
                    'productive': (productive_count / total_count) * 100,
                    'unproductive': (unproductive_count / total_count) * 100,
                    'away': (away_count / total_count) * 100,
                    'idle': (idle_count / total_count) * 100,
                }
            else:
                productivity_percent = {
                    'core productive': 0,
                    'productive': 0,
                    'unproductive': 0,
                    'away': 0,
                    'idle': 0,
                }
            
            productivity_records.append({
                'user_id': user_id,
                'hour': current_hour,
                'productivity': productivity_percent,
                'start_time': hour_data.iloc[0]['timestamp'],
                'end_time': hour_data.iloc[-1]['timestamp'],
            })
        
        current_hour = next_hour

# Convert to DataFrame
productivity_df = pd.DataFrame(productivity_records)

# Save to a new table using SQLAlchemy engine
engine = create_engine(connection_string)
productivity_df.to_sql('users_productivity_record', engine, if_exists='append', index=False)
