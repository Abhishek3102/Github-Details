import requests

GITHUB_TOKEN = 'YOUR_TOKEN_HERE'
username = 'anshshah23'

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

repos_url = f'https://api.github.com/users/{username}/repos'
repos_response = requests.get(repos_url, headers=headers)

commit_and_pr_details = []
if repos_response.status_code == 200:
    repos = repos_response.json()
    
    for repo in repos:  
        repo_name = repo["name"]
        
        commits_url = f'https://api.github.com/repos/{username}/{repo_name}/commits'
        commits_response = requests.get(commits_url, headers=headers)
        commits = [commit['commit']['message'] for commit in commits_response.json()[:5]]
        
        prs_url = f'https://api.github.com/repos/{username}/{repo_name}/pulls?state=all'
        prs_response = requests.get(prs_url, headers=headers)
        prs = [pr['title'] for pr in prs_response.json()[:5]]
        
        commit_and_pr_details.append({
            "repo": repo_name,
            "commits": commits,
            "pull_requests": prs
        })

    with open(f"{username}_commit_and_pr_details.txt", "w") as file:
        for item in commit_and_pr_details:
            file.write(f"Repository: {item['repo']}\n")
            file.write("Commits:\n")
            for commit in item["commits"]:
                file.write(f"  - {commit}\n")
            file.write("Pull Requests:\n")
            for pr in item["pull_requests"]:
                file.write(f"  - {pr}\n")
            file.write("\n")

    print(f"Commit and PR details saved to {username}_commit_and_pr_details.txt")
else:
    print(f"Error fetching repositories: {repos_response.status_code} - {repos_response.text}")
