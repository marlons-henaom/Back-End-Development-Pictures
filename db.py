from pymongo import MongoClient
import os

mongodb_service = os.environ.get('MONGODB_SERVICE')
mongodb_username = os.environ.get('MONGODB_USERNAME')
mongodb_password = os.environ.get('MONGODB_PASSWORD')
mongodb_port = os.environ.get('MONGODB_PORT')

if mongodb_service == None:
    app.logger.error('Missing MongoDB server in the MONGODB_SERVICE variable')
    # abort(500, 'Missing MongoDB server in the MONGODB_SERVICE variable')
    sys.exit(1)

if mongodb_username and mongodb_password:
    MONGO_URI = "mongodb://{}:{}@{}/?authSource=admin".format(mongodb_username,mongodb_password,mongodb_service)
else:
    MONGO_URI = "mongodb://{}/?authSource=admin".format(mongodb_service)

_client = None

def get_client():
    try:
        global _client
        if _client is None:
            _client = MongoClient(MONGO_URI)
        return _client
    except OperationFailure as e:
        app.logger.error(f"Authentication error: {str(e)}")

def get_database(name="test"):
    client = get_client()
    return client[name]