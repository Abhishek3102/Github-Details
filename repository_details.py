import requests

GITHUB_TOKEN = 'YOUR_TOKEN_HERE'
username = 'ashish48maurya'  

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

repos_url = f'https://api.github.com/users/{username}/repos'
repos_response = requests.get(repos_url, headers=headers)

if repos_response.status_code == 200:
    repos = repos_response.json()
    repo_details = [{
        "name": repo["name"],
        "description": repo.get("description"),
        "language": repo.get("language"),
        "fork_count": repo.get("forks_count"),
        "stargazers_count": repo.get("stargazers_count"),
        "open_issues_count": repo.get("open_issues_count"),
        "license": repo.get("license")["name"] if repo.get("license") else "No license",
        "default_branch": repo.get("default_branch")
    } for repo in repos]

    # Save repository details to a file
    with open(f"{username}_repository_details.txt", "w") as file:
        for repo in repo_details:
            file.write(f"Repository Name: {repo['name']}\n")
            for key, value in repo.items():
                if key != "name":
                    file.write(f"{key.capitalize()}: {value}\n")
            file.write("\n")

    print(f"Repository details saved to {username}_repository_details.txt")
else:
    print(f"Error fetching repository details: {repos_response.status_code} - {repos_response.text}")
