import requests
import requests.auth
import json

# Get Authentication (Reddit API)

with open("credentials.json", "r") as cred_file:
    # Get Access Token
    converted_text = json.loads(cred_file.read())

    client_auth = requests.auth.HTTPBasicAuth(
        converted_text["client_id"], converted_text["client_secret"]
    )
    post_data = {
        "grant_type": "password",
        "username": converted_text["username"],
        "password": converted_text["password"],
    }
    headers = {"User-Agent": f"{converted_text['username']}/0.1"}
    response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=client_auth,
        data=post_data,
        headers=headers,
    )

    access_token = response.json()["access_token"]
    username = converted_text["username"]

    # Define headers for future queries
    headers = {
        "Authorization": f"bearer {access_token}",
        "User-Agent": f"{username}/0.1",
    }


def get_posts():
    # i represents the index of the post that is being returned. If the selected post is nsfw or has already been used, it goes to the next one
    i = 0
    content = requests.get(
        f"https://oauth.reddit.com/r/askreddit/hot/", headers=headers
    )
    converted_content = content.json()
    # Check if post is nsfw os has already been used
    with open("used.txt", "r") as used:
        used_posts = used.read().splitlines()

    while (
        converted_content["data"]["children"][i]["data"]["over_18"]
        or converted_content["data"]["children"][i]["data"]["id"] in used_posts
    ):
        i += 1

    post = converted_content["data"]["children"][i]["data"]["url"]

    with open("used.txt", "a") as used:
        used.write(converted_content["data"]["children"][i]["data"]["id"] + "\n")

    return post
