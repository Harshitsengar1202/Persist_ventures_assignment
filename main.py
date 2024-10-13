import requests
import json
import time
import os
import random  # Import random for selecting prompts

# Set up API endpoints and authentication details
SUNO_API_ENDPOINT = "https://api.suno.ai/v1"
LOGIN_ENDPOINT = f"{SUNO_API_ENDPOINT}/auth/login"
GENERATE_MUSIC_ENDPOINT = f"{SUNO_API_ENDPOINT}/music/generate"
DOWNLOAD_SONG_ENDPOINT = f"{SUNO_API_ENDPOINT}/music/download"

# Set up login options and credentials
LOGIN_CREDENTIALS = {
    "Google": {"username": "Harshit.sengar1202@gmail.com", "password": "Harshit@291003"},
    "Apple": {"username": "your_apple_username", "password": "your_apple_password"},
    "Discord": {"username": "your_discord_username", "password": "your_discord_password"}
}

# Set up multiple accounts for switching
ACCOUNTS = [
    {"username": "restrainedaudiocodec6913", "password": "account1_password"},
    {"username": "account2_username", "password": "account2_password"},
    {"username": "account3_username", "password": "account3_password"}
]

# Set up music generation prompts
PROMPTS = ["random prompt 1", "random prompt 2", "random prompt 3"]

# Function to login to Suno API
def login(login_option):
    login_credentials = LOGIN_CREDENTIALS[login_option]
    for attempt in range(5):  # Retry up to 5 times
        response = requests.post(LOGIN_ENDPOINT, json={"username": login_credentials["username"], 
                                                        "password": login_credentials["password"]})
        
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text)
        
        if response.status_code == 200:
            return response.json().get("access_token")
        elif response.status_code == 503:
            print("Service unavailable, retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            print("Login failed:", response.text)
            return None
            
    print("Max retries reached. Unable to login.")
    return None

def generate_music(access_token, prompt):
    headers = {"Authorization": f"Bearer {access_token}"}
    for attempt in range(5):  # Retry up to 5 times
        response = requests.post(GENERATE_MUSIC_ENDPOINT, headers=headers, json={"prompt": prompt})
        
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text)
        
        if response.status_code == 200:
            return response.json()["song_id"]
        elif response.status_code == 503:
            print("Service unavailable while generating music, retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            print("Error generating music:", response.text)
            return None
            
    print("Max retries reached. Unable to generate music.")
    return None
# Function to download generated song using Suno API
def download_song(access_token, song_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(DOWNLOAD_SONG_ENDPOINT, headers=headers, params={"song_id": song_id})
    if response.status_code == 200:
        with open(f"song_{song_id}.mp3", "wb") as f:
            f.write(response.content)
        return True
    else:
        return False

# Function to switch accounts if necessary
def switch_account(accounts, current_account_index):
    if current_account_index < len(accounts) - 1:
        return accounts[current_account_index + 1]
    else:
        return accounts[0]

# Main script
current_account_index = 0
current_account = ACCOUNTS[current_account_index]

while True:
    # Login to Suno API using the first available login option (you can modify this as needed)
    access_token = login("Google")  # Change this to the desired login option (Google, Apple, Discord)
    
    if access_token is None:
        print("Error logging in. Switching accounts.")
        current_account_index += 1
        current_account = switch_account(ACCOUNTS, current_account_index)
        continue

    # Generate music using Suno API
    prompt = random.choice(PROMPTS)
    song_id = generate_music(access_token, prompt)
    
    if song_id is None:
        print("Error generating music. Switching accounts.")
        current_account_index += 1
        current_account = switch_account(ACCOUNTS, current_account_index)
        continue

    # Download generated song using Suno API
    if not download_song(access_token, song_id):
        print("Error downloading song. Switching accounts.")
        current_account_index += 1
        current_account = switch_account(ACCOUNTS, current_account_index)
        continue

    print(f"Song generated and downloaded successfully using account {current_account['username']}!")
    
    time.sleep(2)  # Wait before the next iteration (adjust as needed)
