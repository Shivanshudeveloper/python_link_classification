Introduction:

    This Python project is designed to classify websites into different categories and perform word matching between user-provided text and predefined words. It is a Flask-based web application that offers various functionalities including website classification using a Decision Tree classifier, word matching against a CSV file, and storing results in a PostgreSQL database. Below, we provide an overview of the project structure and usage instructions.

Prerequisites:

    Before running the project, make sure you have the following prerequisites installed:

        Python 3.x
        Flask
        pandas
        scikit-learn
        pymongo
        sqlalchemy
        dotenv

    You can install these packages using pip if they are not already installed.

Project Structure:

    app.py: The main Flask application file that contains the web server and routes.
    
    website_classification.csv: A CSV file containing predefined words for website categories.
    
    model2.pkl: A pre-trained Decision Tree classifier model (for website classification).
    
    screenshots/: A directory for storing uploaded images (create this directory manually).

Configuration:

    The project uses environment variables to configure various settings. Create a .env file in the project root directory and add the following configuration settings:

        makefile
        Copy code
        MONGO_URI=your_mongodb_uri
        POSTGRES_URI=your_postgresql_uri
        Replace your_mongodb_uri and your_postgresql_uri with the respective URIs for your MongoDB and PostgreSQL databases.

Running the Application:

    To run the application, execute the following command in your terminal:

        python app.py
    
    The Flask web server will start, and you can access the application by navigating to http://localhost:8080 in your web browser.

Web Routes:

    /: The home route that displays a welcome message.
    /mlwork (POST): Accepts JSON data for word matching and website category prediction.

Word Matching and Category Prediction

    The /mlwork route accepts JSON data with the following format:

        {
        "userData": ["list", "of", "words"],
        "userId": "unique_user_id"
        }

    The provided list of words is matched against predefined words in the website_classification.csv file.
    Cosine similarity is used to calculate the similarity between words.
    
    Results are stored in a PostgreSQL database (img_match table) with the average probability and the highest probability word.
    
    Website category prediction is performed using a pre-trained Decision Tree classifier (model2.pkl) based on the user's title. Predicted categories are stored in the data_match table.