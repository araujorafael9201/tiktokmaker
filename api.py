import requests
import json

# Get Authentication (Reddit API)
with open("credentials.json", "r") as cred_file:
    converted_text = json.loads(cred_file.read())

    access_token = converted_text["access_token"]
    username = converted_text["username"]

    headers = {
        "Authorization": f"bearer {access_token}",
        "User-Agent": f"{username}/0.1",
    }


def get_posts(n_of_posts=1):
    links = []

    content = requests.get(
        f"https://oauth.reddit.com/r/askreddit/controversial/", headers=headers
    )

    converted_content = content.json()

    for i in range(n_of_posts):
        post = converted_content["data"]["children"][i]["data"]["url"]

        links.append(post)

    return links
