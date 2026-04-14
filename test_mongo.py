import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

print("Starting W3Schools PyMongo Test...")
try:
    # This is the exact method taught by W3Schools
    myclient = pymongo.MongoClient("mongodb+srv://louvel:%40LouvelRouz15@nutricalc.0xus7pc.mongodb.net/", serverSelectionTimeoutMS=10000)
    
    # Attempting to fetch server info to prove the connection works
    print("Waiting for server response...")
    myclient.admin.command('ping')
    print("\nSUCCESS! The W3Schools connection string works perfectly!")
    
except Exception as e:
    print(f"\nFAILED! PythonAnywhere Firewall Blocked It.")
    print(f"Exact Error: {e}")
