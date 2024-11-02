import requests
from bs4 import BeautifulSoup
import re

GITHUB_TOKEN = 'YOUR_TOKEN_HERE'  
username = 'Abhishek3102'  

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

response = requests.get(f'https://api.github.com/users/{username}', headers=headers)

if response.status_code == 200:
    data = response.json()
    
    profile_details = {
        "profile_url": data.get("html_url"),
        "avatar_url": data.get("avatar_url"),
        "public_gists": data.get("public_gists"),
        "user_type": data.get("type"),
        "site_admin": data.get("site_admin"),
        "blog_url": data.get("blog"),
        "twitter_username": data.get("twitter_username"),
        "company": data.get("company"),
        "email": data.get("email"),
        "hireable": data.get("hireable")
    }

    # Attempt to extract additional social media links from bio and blog URL
    bio = data.get("bio", "")
    blog_url = data.get("blog", "")
    social_links = []

    # Regex pattern to find URLs in bio and blog URL
    url_pattern = r'https?://(?:www\.)?\S+'
    if bio:
        social_links.extend(re.findall(url_pattern, bio))
    if blog_url:
        social_links.append(blog_url)

    profile_page_url = f"https://github.com/{username}"
    page_response = requests.get(profile_page_url)
    if page_response.status_code == 200:
        soup = BeautifulSoup(page_response.text, 'html.parser')
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            if any(social in href for social in ["linkedin", "instagram", "twitter", "facebook"]):
                social_links.append(href)

    profile_details["social_links"] = social_links

    def fetch_all_pages(url):
        results = []
        while url:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                page_data = response.json()
                results.extend([user['login'] for user in page_data])
                
                if 'next' in response.links:
                    url = response.links['next']['url']
                else:
                    url = None
            else:
                print(f"Error fetching data from {url}: {response.status_code}")
                break
        return results

    followers_url = data["followers_url"]
    profile_details["followers"] = fetch_all_pages(followers_url)

    following_url = f'https://api.github.com/users/{username}/following'
    profile_details["following"] = fetch_all_pages(following_url)

    with open(f"{username}_profile_details.txt", "w") as file:
        for key, value in profile_details.items():
            file.write(f"{key.capitalize()}: {value}\n")

    print(f"Profile details saved to {username}_profile_details.txt")

else:
    print(f"Error fetching profile details: {response.status_code} - {response.text}")
