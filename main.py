from selenium import webdriver
from selenium.webdriver.common.by import By

from api import get_posts

N_OF_COMMENTS = 5
N_OF_POSTS = 5

links = get_posts(N_OF_POSTS)


driver = webdriver.Firefox()

for l in links:
    # Get post id from url
    post_id = l.split("/")[6]

    try:
        driver.get(f"{l}?limit={N_OF_COMMENTS}&depth=1")

        # Get Post
        post = driver.find_element(By.XPATH, "//div[@data-test-id='post-content']")
        post.screenshot(f"screenshots/{post_id}-post.png")

        # Get Comments
        elems = driver.find_elements(By.CLASS_NAME, "Comment")

        for e in elems:
            e.screenshot(f"screenshots/{post_id}-{elems.index(e)}.png")

    except:
        continue
