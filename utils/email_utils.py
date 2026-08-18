import requests
import time

API_URL = "https://mail.ssqa.digital/latest-email.php"

def get_latest_otp(username, previous_code=None, timeout=30, poll_interval=2):
    start_time = time.time()
    params = {'user': username}
    
    print(f"\nWaiting for a new OTP for user: {username}...")
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(API_URL, params=params, timeout=5)
            if response.status_code == 200:
                payload = response.json()
                current_code = payload.get("data", {}).get("code")
                
                # If we found a code, and it's not the stale one from the last test
                if current_code and current_code != previous_code:
                    print(f"New OTP Received: {current_code}")
                    return current_code
        except requests.RequestException as e:
            print(f"API Fetch warning: {e}")
            
        time.sleep(poll_interval)
        
    raise TimeoutError(f"Timed out waiting for a new OTP for {username} after {timeout}s")