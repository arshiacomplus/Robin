import requests
import json
import sys

# تنظیمات اصلی
URL = "https://barko-app.whale-land-server.com/api/sub"
OUTPUT_FILE = "sub.txt"
SERIAL_KEY = "30ad9c094ea575867e05d795fdd13f32477bbcf6544fa9d553a2743b5649672a44869e4b9e79d78f0d6d1549f76d0fb0f004efde1ab0ec120a5577dc19af7ac4a023b365eb694a708359760852f16190ae6168e1907ec549cc30dc5cbb7cc7392032a3c1425eef7427519463c7a437b5d0613e8128146bbf704167a1fa9e83794f698cf256fc170f16adcf9877aa962491688eba8f30d1002088a92b7f132d0213d0a35791667fee3ce5909f8256775bf03050c4c362191492548d0be78244304be233427b9cd0e501272f0d9a7ec16a4cbc0e9a0176dcff67d0df1edebbb5fe3cc700150ad3df8b9515076532a2c2c3ce9c015f7d92c6e927e6134e46f9406753568e4833ae7cbecbd0"

def fetch_sub():
    session = requests.Session()
    
    # هدرها مطابق با دقیق‌ترین جزئیات ارسالی شما
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
        "Accept-Encoding": "gzip",
        "Connection": "close"
    }

    try:
        print("--- Sending Request ---")
        response = session.get(URL, headers=headers, timeout=25)
        
        # لاگ وضعیت پاسخ
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")

        response.raise_for_status()
        
        # لاگ متن خام پاسخ برای عیب‌یابی (بسیار مهم)
        raw_data = response.text
        print("\n--- Raw Response Body (First 500 chars) ---")
        print(raw_data[:500]) 
        print("--- End of Raw Response ---\n")

        data = response.json()
        
        configs = []
        # استخراج از تمام فیلدهای احتمالی
        for key in ["config", "adsNormalConfig", "customConfig"]:
            if key in data and data[key]:
                val = data[key].strip()
                if val and val != "W10=": # فیلتر کردن مقادیر خالی base64 مثل []
                    configs.append(val)
                    print(f"Found valid content in key: '{key}'")

        if not configs:
            print("❌ Error: No valid configs found in JSON keys.")
            return

        final_content = "\n".join(configs)
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(final_content)
        
        print(f"\n✅ Success! File '{OUTPUT_FILE}' updated with {len(final_content.splitlines())} lines.")

    except requests.exceptions.JSONDecodeError:
        print("❌ Error: Response is not JSON. Check Raw Response above.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_sub()
