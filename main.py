import requests
import time
import random

# Set up Freesound API endpoint and authentication details
FREESOUND_API_ENDPOINT = "https://freesound.org/apiv2/search/text/"
API_KEY = "po8uhWUgIhFoJVs5mfkJzt4JGs9w0K7VbsUgAKaD"  # Replace with your actual Freesound API key

# Set up music generation prompts
PROMPTS = [
    "Create a relaxing piano piece.",
    "Generate a cheerful pop song.",
    "Compose a dramatic orchestral score."
]

# Function to search for sounds using Freesound API
def search_sounds(prompt):
    headers = {
        "Authorization": f"Token {API_KEY}"
    }
    
    params = {
        "query": prompt,
        "page_size": 5  # Number of results to return
    }
    
    for attempt in range(5):  # Retry up to 5 times
        response = requests.get(FREESOUND_API_ENDPOINT, headers=headers, params=params)
        
        print("Response Status Code:", response.status_code)
        
        if response.status_code == 200:
            sounds = response.json()["results"]
            if not sounds:  # Check if there are no results
                print("No sounds found for the prompt.")
                return None
            
            # Process and display sound information
            for sound in sounds:
                print(f"Found sound: {sound['name']} - Preview URL: {sound['previews']['preview-lq-mp3']}")
            return sounds
        elif response.status_code == 429:
            print("Quota exceeded, please check your plan. Retrying after delay...")
            time.sleep(60)  # Wait for a minute before retrying
        elif response.status_code == 503:
            print("Service unavailable while searching sounds, retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            print("Error searching sounds:", response.text)
            return None
            
    print("Max retries reached. Unable to search sounds.")
    return None

# Main script
while True:
    # Randomly select a prompt from the list
    prompt = random.choice(PROMPTS)
    
    # Search for sounds using Freesound API
    sounds = search_sounds(prompt)
    
    if sounds is None:
        print("Error searching sounds.")
        continue  # Handle error appropriately
    
    # Process and display sound information (for demonstration)
    for sound in sounds:
        print(f"Found sound: {sound['name']} - {sound['previews']['preview-lq-mp3']}")

    time.sleep(2)  # Wait before the next iteration (adjust as needed)
