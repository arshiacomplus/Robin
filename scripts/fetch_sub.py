import requests
import sys

URL = "https://barko-app.whale-land-server.com/api/sub"
OUTPUT_FILE = "sub.txt"

def main():
    try:
        r = requests.get(URL, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print("Request failed:", e)
        sys.exit(1)

    try:
        data = r.json()
    except Exception:
        print("Response is not valid JSON")
        sys.exit(1)


    if "config" not in data:
        print("Key 'config' not found in response")
        sys.exit(1)

    config_value = data["config"]


    if not isinstance(config_value, str):
        print("'config' is not a string")
        sys.exit(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(config_value.strip() + "\n")

    print("sub.txt updated successfully")

if __name__ == "__main__":
    main()
