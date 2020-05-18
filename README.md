# Disaster Response App

1. The code in this repository computes a machine learning model for multi-output classification predicting the context of text messages during a disaster.

    a. `source/ETL Pipeline Preparation.ipynb` extracts, transforms and loads the data the model is trained on.
    
    b. `source/ML Pipeline Preparation.ipynb` trains the model.

2. The code further creates a webapp that can be used to classify new incoming messages and predicts which categories the messages might belong to. For files to create the web page where messages can be classified, see the "app" folder. Run the following commands in the project's root directory to set up database and model.

    a. To run ETL pipeline that cleans data and stores in database
    
        `python app/data/process_etl.py app/data/disaster_messages.csv app/data/disaster_categories.csv app/data/DisasterResponse.db`
    b. To run ML pipeline that trains classifier and saves
    
        `python app/models/process_ml.py app/data/DisasterResponse.db app/models/classifier.pkl`

    c. Run the following command in the app's directory to run your web app: `python app/run.py`

    d. Go to http://0.0.0.0:3001/
