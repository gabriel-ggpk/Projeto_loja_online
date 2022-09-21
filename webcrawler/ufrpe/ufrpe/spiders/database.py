from pymongo import MongoClient

def get_database():
    

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://gabrielHCS:teste@cluster0.sqgb8.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['feira_online']
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    dbname = get_database()