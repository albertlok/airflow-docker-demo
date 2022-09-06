# Import libraries:
from datetime import timedelta #Required to calculate duration
import airflow #Required to instantiate a DAG
import pandas as pd
import numpy as np
import os

from airflow import DAG
from airflow.operators.python import PythonOperator #Python operator will be used in our task to run any Python code

dag_path = os.getcwd()

#Callable functions:
def data_cleaning():
    hotel_data = pd.read_csv("raw_data/hotel_bookings.csv") # Importing raw data
    hotel_data.head() # Display first 10 rows of data
    hotel_data.info() # Print info about dataframe
    hotel_data.describe() # Return description of data in dataframe
    
    # Checking null columns
    hotel_data.isnull().sum()
    
    # Replace missing values
    nan_replacements = {'children': 0, 'country':'Unknown', 'agent':'Organic Booking', 'company':'Personal Booking'}
    cleaned_data = hotel_data.fillna(nan_replacements)
    
    hotel_data.info()
    
    # Store cleaned data
    cleaned_data.to_csv('processed_data/processed_hotel_data.csv', index=False)
    
def cleaned_data_message():
    print('Data successfully cleaned')

# These arguments will be passed to each operator
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(7) # Date which the DAG should start running
}

# Object to instantiate pipeline dynamically:
data_cleaning_dag = DAG(
    'data_cleaning_dag', # Name of the DAG displayed in airflow UI
    default_args = default_args,
    schedule_interval = timedelta(days=30), # Interval at which the DAG should run
    catchup = False
)

# Tasks:
clean_data = PythonOperator(
    task_id = 'data_cleaning',
    python_callable = data_cleaning,
    dag = data_cleaning_dag
)
          
message = PythonOperator(
    task_id = 'cleaned_data_message',
    python_callable = cleaned_data_message,
    dag = data_cleaning_dag
)
          
# Set dependencies:
clean_data >> message