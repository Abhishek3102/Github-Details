import requests
import csv
import time

# Your GitHub token
GITHUB_TOKEN = 'YOUR_TOKEN_HERE'  

# Set the headers with authorization
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

# Function to fetch repositories for a given user
def fetch_repositories(user_login):
    repo_url = f'https://api.github.com/users/{user_login}/repos?per_page=500'
    response = requests.get(repo_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching repos for {user_login}: {response.status_code} - {response.text}")
        return []

# Read users from users.csv and fetch their repositories
with open('users.csv', mode='r', encoding='utf-8') as users_file:
    users_reader = csv.DictReader(users_file)
    
    with open('repositories.csv', mode='w', newline='', encoding='utf-8') as repos_file:
        repos_writer = csv.writer(repos_file)
        # Write the header
        repos_writer.writerow(['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name'])
        
        for user in users_reader:
            user_login = user['login']
            repos = fetch_repositories(user_login)
            
            for repo in repos:
                repos_writer.writerow([
                    user_login,
                    repo.get('full_name', ''),
                    repo.get('created_at', ''),
                    repo.get('stargazers_count', 0),
                    repo.get('watchers_count', 0),
                    repo.get('language', ''),
                    repo.get('has_projects', False),
                    repo.get('has_wiki', False),
                    repo.get('license')['name'] if repo.get('license') else ''  # Safely access the license name
                ])
            
            # Sleep to avoid hitting the rate limit
            time.sleep(1)  # Pause for 1 second between requests

print("repositories.csv created successfully.")