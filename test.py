from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import os

# Setup Flask
app = Flask(__name__)

# Load environment variables
DB_USER = os.getenv("DB_USERNAME")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Database connection
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Define the productivity map as mentioned before
productivity_map = {
    # As previously defined...
}

# Utility functions
def fetch_device_activities(device_uid):
    session = Session()
    try:
        results = session.execute(
            "SELECT * FROM user_activity WHERE user_uid = :user_uid ORDER BY timestamp",
            {"user_uid": device_uid}
        )
        activities = [dict(result) for result in results]
        return activities
    finally:
        session.close()

def calculate_productivity(activities):
    # Process and calculate productivity per your specification
    pass

@app.route('/productivity_report', methods=['GET'])
def generate_productivity_report():
    session = Session()
    try:
        devices = session.execute("SELECT * FROM devices").fetchall()
        report = []

        for device in devices:
            activities = fetch_device_activities(device['device_uid'])
            productivity_data = calculate_productivity(activities)
            report.append({
                "name": device['user_name'],
                "workingHour": "calculation_needed",
                "productivityRecord": productivity_data
            })

        return jsonify(report)

    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True)
