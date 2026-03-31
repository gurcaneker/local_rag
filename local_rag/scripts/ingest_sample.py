import requests
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python ingest_sample.py <path_to_file>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    url = "http://127.0.0.1:8000/documents/upload"
    
    with open(file_path, "rb") as f:
        files = {"file": f}
        try:
            response = requests.post(url, files=files)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
