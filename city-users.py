import requests
import csv

GITHUB_TOKEN = 'YOUR_TOKEN_HERE'  

API_URL = 'https://api.github.com/search/users?q=location:mumbai+followers:>100'

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

response = requests.get(API_URL, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    users = data.get('items', [])
    with open('users.csv', mode='w', newline='', encoding='utf-8') as users_file:
        users_writer = csv.writer(users_file)
        users_writer.writerow(['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at'])
        
        for user in users:
            users_writer.writerow([
                user.get('login', ''),
                user.get('name', ''),
                user.get('company', '').strip('@').strip().upper(),
                user.get('location', ''),
                user.get('email', ''),
                user.get('hireable', False),
                user.get('bio', ''),
                user.get('public_repos', 0),
                user.get('followers', 0),
                user.get('following', 0),
                user.get('created_at', '')
            ])

    print("City Users.csv created successfully.")
else:
    print(f"Error fetching data from GitHub API: {response.status_code} - {response.text}")