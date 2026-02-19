
import requests
import json
import random

API_URL = "http://localhost:8000"

def test_prediction():
    print(f"Testing Prediction API at {API_URL}...")
    
    payload = {
        "patient_name": f"Test User {random.randint(1000,9999)}",
        "age": 45,
        "fev1": 3.5,
        "pef": 450,
        "spo2": 98,
        "zip_code": "100018", # Use a valid looking zip
        "gender": "Male",
        "smoking": "Non-smoker",
        "wheezing": False,
        "shortness_of_breath": False,
        "height": 175,
        "weight": 70,
        "medication_use": False
    }

    try:
        # 1. Make Prediction
        print("Sending POST /predict request...")
        response = requests.post(f"{API_URL}/predict", json=payload)
        
        if response.status_code != 200:
            print(f"FAILED: Status {response.status_code}")
            print(response.text)
            return False
            
        data = response.json()
        risk = data.get("prediction", {}).get("risk_score")
        print(f"Prediction Success! Risk Score: {risk}")

        # 2. Verify History (Storage)
        print("Checking GET /history to verify storage...")
        hist_response = requests.get(f"{API_URL}/history")
        
        if hist_response.status_code != 200:
            print(f"FAILED to fetcch history: {hist_response.status_code}")
            return False
            
        history = hist_response.json()
        print(f"History contains {len(history)} records.")
        
        # Check if our new patient is there
        found = False
        for record in history:
            if record.get("patient_name") == payload["patient_name"]:
                found = True
                print(f"SUCCESS: Found recent prediction for {payload['patient_name']} in history db!")
                break
        
        if not found:
            print("WARNING: Did not find the new prediction in history immediately. (Might be latency or failure)")
            return False

        return True

    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    test_prediction()
