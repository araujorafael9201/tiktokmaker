from selenium import webdriver
from selenium.webdriver.common.by import By

from api import get_posts

from audio import make_audio_files
from video import make_video

# Number of Comments in the Video
N_OF_COMMENTS = 4

url = get_posts()
url = url.replace('www', 'old')

texts_to_read = []

driver = webdriver.Firefox()

# Get post id from url
post_id = url.split("/")[6]

driver.get(f"{url}?limit={N_OF_COMMENTS}&depth=1")

# Get Post Text and Screenshot
divs = driver.find_elements(By.CLASS_NAME, "entry")
title = driver.find_elements(By.CLASS_NAME, "title")[2].text
texts_to_read.append(title)

post = driver.find_element(By.CLASS_NAME, "top-matter")
post.screenshot(f"screenshots/screenshot-0.png")

# Get Comments Divs to Screenshot
comments_divs = divs[1:]

# A single comment can have more than one <p> tag, so this is needed
for com in comments_divs:
    paragraphs = com.find_elements(By.TAG_NAME, "p")
    for i, p in enumerate(paragraphs):
        if i % 2 == 0 or p.text == "":
            continue
        texts_to_read.append(p.text)

print(texts_to_read)

# Get Comments Screenshot
for i, e in enumerate(comments_divs[:-1]):
    if i % 2 != 0:
        continue
    e.screenshot(f"screenshots/screenshot-{comments_divs.index(e) + 1}.png")

make_audio_files(texts_to_read)
make_video(title)
