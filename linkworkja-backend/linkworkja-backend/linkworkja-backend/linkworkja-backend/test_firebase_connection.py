#!/usr/bin/env python3
"""
Test script to verify Firebase connection
Run this after setting up your Firebase credentials
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_firebase_connection():
    """Test if Firebase is properly connected"""
    try:
        from app.services.firebase_service import firebase_service
        
        print("Testing Firebase connection...")
        print(f"Development mode: {firebase_service._dev_mode}")
        
        if firebase_service._dev_mode:
            print("WARNING: Still in development mode!")
            print("Make sure you have:")
            print("1. Created a Firebase project")
            print("2. Downloaded the service account JSON file")
            print("3. Renamed it to 'dev-firebase-credentials.json'")
            print("4. Placed it in the project root directory")
            return False
        else:
            print("SUCCESS: Connected to Firebase!")
            
            # Test basic operations
            print("Testing basic operations...")
            
            # Test creating a test document
            test_data = {
                "test": True,
                "timestamp": "2024-01-01T00:00:00Z"
            }
            
            # This will create a test document in Firestore
            doc_ref = firebase_service.db.collection('test').document('connection_test')
            doc_ref.set(test_data)
            print("SUCCESS: Can write to Firestore")
            
            # Test reading
            doc = doc_ref.get()
            if doc.exists:
                print("SUCCESS: Can read from Firestore")
                print(f"Test data: {doc.to_dict()}")
            else:
                print("ERROR: Cannot read from Firestore")
                return False
            
            # Clean up test document
            doc_ref.delete()
            print("SUCCESS: Can delete from Firestore")
            
            print("\nFirebase connection is working perfectly!")
            return True
            
    except Exception as e:
        print(f"ERROR: Firebase connection failed: {e}")
        return False

if __name__ == "__main__":
    if test_firebase_connection():
        print("\nFirebase is ready for production use!")
        sys.exit(0)
    else:
        print("\nFirebase setup incomplete. Please follow the setup guide.")
        sys.exit(1)
