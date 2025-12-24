import requests
import time
from endpoints import ENDPOINTS 

def test_api_endpoints(base_url="http://127.0.0.1:8000/"):
    token = None
    captured_ids = {}
    timestamp = int(time.time())
    
    for endpoint in ENDPOINTS:
        method = endpoint["method"]
        url = f"{base_url}{endpoint['url']}"
        expected_status = endpoint["expected_status"]
        data = endpoint.get("data", None)

        # Replace placeholders in URL with captured IDs
        for key, value in captured_ids.items():
            url = url.replace(f"{{{key}}}", str(value))
        
        # Replace placeholders in data with captured IDs and timestamp
        if data:
            data = replace_placeholders_in_data(data, captured_ids, timestamp)

        headers = {'Content-Type': 'application/json'}
        if token:
            headers['authorization'] = f'Bearer {token}'

        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "PATCH":
            response = requests.patch(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        assert response.status_code == expected_status, f"Failed on {method} {url}: expected {expected_status}, got {response.status_code}, {response.text}"
        
        # Capture token from login
        if token is None and response.status_code == 200 and "access" in response.json().get("data", {}):
            token = response.json().get("data").get("access")
            print(f"Token captured: {token[:20]}...")
        
        # Capture ID if specified
        if "capture_id" in endpoint and response.status_code in [200, 201]:
            response_data = response.json().get("data", {})
            if "id" in response_data:
                captured_ids[endpoint["capture_id"]] = response_data["id"]
                print(f"Captured {endpoint['capture_id']}: {response_data['id']}")

        print(f"✓ {method} {url} - Status: {response.status_code}")

def replace_placeholders_in_data(data, captured_ids, timestamp):
    if isinstance(data, dict):
        return {k: replace_placeholders_in_data(v, captured_ids, timestamp) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_placeholders_in_data(item, captured_ids, timestamp) for item in data]
    elif isinstance(data, str):
        for key, value in captured_ids.items():
            data = data.replace(f"{{{key}}}", str(value))
        data = data.replace("{timestamp}", str(timestamp))
        return data
    return data

if __name__ == "__main__":
    try:
        test_api_endpoints()
        print("\nAll tests passed!")
    except Exception as e:
        print(f"\nTest failed: {e}")
