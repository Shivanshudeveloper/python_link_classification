from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import joblib
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Constants
labels = {
    0: 'Adult',
    1: 'Business/Corporate',
    2: 'Computers and Technology',
    3: 'E-Commerce',
    4: 'Education',
    5: 'Food',
    6: 'Forums',
    7: 'Games',
    8: 'Health and Fitness',
    9: 'Law and Government',
    10: 'News',
    11: 'Photography',
    12: 'Social Networking and Messaging',
    13: 'Sports',
    14: 'Streaming Services',
    15: 'Travel'
}

# Mapping categories to productivity status
productivity_map = {
    'Adult': 'Unproductive',
    'Business/Corporate': 'Productive',
    'Computers and Technology': 'Productive',
    'E-Commerce': 'Productive',
    'Education': 'Productive',
    'Food': 'Neutral',
    'Forums': 'Neutral',
    'Games': 'Unproductive',
    'Health and Fitness': 'Productive',
    'Law and Government': 'Productive',
    'News': 'Neutral',
    'Photography': 'Neutral',
    'Social Networking and Messaging': 'Unproductive',
    'Sports': 'Unproductive',
    'Streaming Services': 'Unproductive',
    'Travel': 'Neutral',
    'Development': 'Productive',
    'Entertainment & Leisure': 'Unproductive',
    'Meeting & Webinar Platforms': 'Productive',
    'Chat & Instant Messaging': 'Neutral',
    'Email Platforms': 'Neutral',
    'Task & Project Management': 'Productive',
    'Document Collaboration & Sharing': 'Productive',
    'IDEs & Code Editors': 'Productive',
    'Database Management': 'Productive',
    'Version Control Platforms': 'Productive',
    'CI/CD Tools': 'Productive',
    'Adobe Creative Cloud': 'Productive',
    'Figma': 'Productive',
    'Canva': 'Productive',
    'Research Publications & Journals': 'Productive',
    'Online Courses & Platforms': 'Productive',
    'Knowledge-sharing & Forums': 'Productive',
    'National News': 'Neutral',
    'International News': 'Neutral',
    'Industry-specific Publications': 'Neutral',
    'Professional Networking': 'Productive',
    'General Social Media': 'Unproductive',
    'Movies & Series Streaming': 'Unproductive',
    'Gaming & Related Platforms': 'Unproductive',
    'Lifestyle & Blogs': 'Unproductive',
    'Calculators & Converters': 'Neutral',
    'Translation & Language Tools': 'Neutral',
    'Cloud Storage': 'Productive',
    'Amazon': 'Unproductive',
    'eBay': 'Unproductive',
    'Flipkart': 'Unproductive',
    'Etsy': 'Unproductive',
    'Myntra': 'Unproductive',
    'Sports News & Updates': 'Unproductive',
    'Live Streaming & Highlights': 'Unproductive',
    'Explicit Content Sites': 'Unproductive',
    'Dating & Relationship Platforms': 'Unproductive',
    'Gambling & Betting': 'Unproductive',
    'Educational & Informative': 'Productive',
    'Professional & Industry-Specific': 'Productive',
    'Entertainment': 'Unproductive',
    'Lifestyle, Arts & Creativity': 'Neutral',
    'Gaming': 'Unproductive',
    'Sports & Fitness': 'Productive',
    'Tech & Gadgets': 'Productive',
    'Children & Family': 'Neutral',
    'Culture & Society': 'Neutral',
    'Miscellaneous': 'Neutral',
    "Communication Tools": "Productive",
    "Research & Learning": "Productive"
}

# Load machine learning models
label_encoder = joblib.load('label_encoder.joblib')
vectorizer = joblib.load('tfif_vectorizer.joblib')
model = joblib.load('website_classifier_model.joblib')

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
engine = create_engine(f'mysql+mysqlconnector://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}')
Session = sessionmaker(bind=engine)

def get_all_device_ids():
    session = Session()
    try:
        result = session.execute(text("SELECT device_uid, user_name FROM devices")).fetchall()
        devices = [{'device_uid': row[0], 'user_name': row[1]} for row in result]
        return devices
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

def get_user_activities(device_uid, date):
    session = Session()
    try:
        result = session.execute(text(
            "SELECT page_title, timestamp FROM user_activity WHERE DATE(timestamp) = :date AND user_uid = :device_uid ORDER BY timestamp"
        ), {"date": date, "device_uid": device_uid}).fetchall()
        activities = [(row[0], row[1]) for row in result]
        return activities
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

def predict_category(page_title):
    transformed = vectorizer.transform([page_title])
    prediction = model.predict(transformed)
    category = label_encoder.inverse_transform(prediction)[0]
    return category

def calculate_productivity_internal(activities):
    productivity_counts = {'Productive': 0, 'Neutral': 0, 'Unproductive': 0, 'Away': 0}
    total_time = timedelta(hours=1)

    hourly_activities = {}
    for page_title, timestamp in activities:
        hour_key = timestamp.replace(minute=0, second=0, microsecond=0)
        if hour_key not in hourly_activities:
            hourly_activities[hour_key] = []
        hourly_activities[hour_key].append((page_title, timestamp))

    hourly_productivity = {}
    for hour, activities in hourly_activities.items():
        activities.sort(key=lambda x: x[1])
        first_activity = activities[0][1]
        last_activity = activities[-1][1]

        active_time = last_activity - first_activity
        away_time = total_time - active_time
        hourly_counts = {'Productive': 0, 'Neutral': 0, 'Unproductive': 0}

        for page_title, _ in activities:
            category = predict_category(page_title)
            status = productivity_map.get(category, 'Neutral')  # Default to 'Neutral' if the category is unknown
            hourly_counts[status] += 1

        total_activities = sum(hourly_counts.values())
        productive_percentage = (hourly_counts['Productive'] / total_activities) * 100 if total_activities else 0
        unproductive_percentage = (hourly_counts['Unproductive'] / total_activities) * 100 if total_activities else 0
        neutral_percentage = (hourly_counts['Neutral'] / total_activities) * 100 if total_activities else 0
        away_percentage = (away_time / total_time) * 100

        # Convert datetime key to string for JSON serialization
        hourly_productivity[hour.strftime('%Y-%m-%d %H:%M:%S')] = {
            'productive_percentage': round(productive_percentage, 2),
            'unproductive_percentage': round(unproductive_percentage, 2),
            'neutral_percentage': round(neutral_percentage, 2),
            'away_percentage': round(away_percentage, 2)
        }

    return hourly_productivity

def calculate_working_hours(activities):
    if not activities:
        return "0h 0m"
    first_activity = activities[0][1]
    last_activity = activities[-1][1]
    working_duration = last_activity - first_activity
    hours, remainder = divmod(working_duration.total_seconds(), 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m"

@app.route('/calculate_hourly_productivity', methods=['GET'])
def calculate_hourly_productivity():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    devices = get_all_device_ids()
    all_productivity_data = []

    for device in devices:
        device_id = device['device_uid']
        user_name = device['user_name']
        activities = get_user_activities(device_id, date)
        productivity_data = calculate_productivity_internal(activities)
        working_hours = calculate_working_hours(activities)

        all_productivity_data.append({
            'date': date,
            'device_id': device_id,
            'productivity_data': productivity_data,
            'user_name': user_name,
            'working_hours': working_hours
        })

    return jsonify(all_productivity_data)

if __name__ == '__main__':
    app.run(debug=True)
