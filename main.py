from selenium import webdriver
from selenium.webdriver.common.by import By

from api import get_posts

from audio import make_audio_files
from video import make_video

# Number of Comments in the Video
N_OF_COMMENTS = 4

url = get_posts()

texts_to_read = []

driver = webdriver.Firefox()

# Get post id from url
post_id = url.split("/")[6]

driver.get(f"{url}?limit={N_OF_COMMENTS}&depth=1")

# Get Post Text and Screenshot
post = driver.find_element(By.XPATH, "//div[@data-test-id='post-content']")
title = driver.find_element(By.TAG_NAME, "h1").text
texts_to_read.append(title)
post.screenshot(f"screenshots/screenshot-0.png")

# Get Comments Divs to Screenshot
comments_divs = driver.find_elements(By.CLASS_NAME, "Comment")


# Get Comments Texts
comments_content = driver.find_elements(
    By.XPATH,
    "//div[contains(concat(' ', normalize-space(@class), ' '), ' RichTextJSON-root ')]",
)

# A single comment can have more than one <p> tag, so this is needed
for com in comments_content:
    com_full_text = []
    paragraphs = com.find_elements(By.TAG_NAME, "p")
    for p in paragraphs:
        com_full_text.append(p.text)

    # Some threads have empty <p> tags
    if com.text != "":
        texts_to_read.append(" ".join(com_full_text))

# Get Comments Screenshot
for e in comments_divs:
    e.screenshot(f"screenshots/screenshot-{comments_divs.index(e) + 1}.png")


make_audio_files(texts_to_read)
make_video(title)
