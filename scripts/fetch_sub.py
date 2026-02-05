from curl_cffi import requests
import json
import sys
import os

URL = "https://barko-app.whale-land-server.com/api/sub"
OUTPUT_FILE = "sub.txt"
SERIAL_KEY = "30ad9c094ea575867e05d795fdd13f32477bbcf6544fa9d553a2743b5649672a44869e4b9e79d78f0d6d1549f76d0fb0f004efde1ab0ec120a5577dc19af7ac4a023b365eb694a708359760852f16190ae6168e1907ec549cc30dc5cbb7cc7392032a3c1425eef7427519463c7a437b5d0613e8128146bbf704167a1fa9e83794f698cf256fc170f16adcf9877aa962491688eba8f30d1002088a92b7f132d0213d0a35791667fee3ce5909f8256775bf03050c4c362191492548d0be78244304be233427b9cd0e501272fd3f84372b73fbd0e9ae73c12ff67d0df1edebbb5fe3cc700150ad3df8b9515076532a2c2c3ce9c015f7d92c6e927e6134e46f9406753568e4833ae7cbecbd0"

def main():
    print("--- Initialization ---")
    headers = {
        "User-Agent": "torob/2.1",
        "Package-Name": "com.barkovpn.app",
        "Device-ID": "94c77d03-9fe2-4fcf-a586-91ca9c7292dd",
        "Finger-Print": "A47218C3DF",
        "Signal-Id": "null",
        "Android-Api": "33",
        "android": "6d79acbc5fd56fc6",
        "Mobile": "2312FPCA6G",
        "Type": "import",
        "App-Version": "2.1",
        "App-Version-Code": "20260203",
        "serial": SERIAL_KEY,
        "Host" : "barko-app.barko-land-server.com",
        "Accept-Encoding": "gzip",
        "Connection": "close",
    }

    try:
        print(f"Requesting URL: {URL}")
        # استفاده از impersonate برای شبیه‌سازی دقیق TLS Fingerprint
        response = requests.get(
            URL, 
            headers=headers, 
            impersonate="chrome110", # شبیه‌سازی مرورگر مدرن
            timeout=30
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")

        if response.status_code != 200:
            print(f"❌ Error: Server returned status {response.status_code}")
            print("Response text:", response.text)
            sys.exit(1)

        # لاگ متن خام پاسخ (برای بررسی فیک بودن)
        raw_body = response.text
        print("\n--- RAW RESPONSE START ---")
        print(raw_body)
        print("--- RAW RESPONSE END ---\n")

        data = response.json()
        all_configs = []

        # استخراج هوشمند تمام کانفیگ‌ها
        keys_to_check = ["config", "adsNormalConfig", "customConfig"]
        for key in keys_to_check:
            if key in data and data[key]:
                content = data[key].strip()
                # حذف مقادیر فیک یا خالی Base64
                if content and content not in ["W10=", "[]", ""]:
                    all_configs.append(content)
                    print(f"✅ Found data in key: {key}")

        if not all_configs:
            print("⚠️ Warning: No valid configs found. Server might be sending fake data.")
            sys.exit(1)

        # ترکیب و ذخیره
        final_output = "\n".join(all_configs)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(final_output + "\n")

        print(f"DONE: {OUTPUT_FILE} updated.")

    except Exception as e:
        print(f"❌ Fatal Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
