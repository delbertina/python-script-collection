import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from selenium import webdriver

# make directory for output files
def prepare_output_dir() -> str:
    current_datetime = datetime.now() # get current datetime
    current_datetime_formatted = current_datetime.strftime("%Y-%m-%d_%H-%M-%S-%f") # format it to be a readable file folder name
    output_path = "./output/" + current_datetime_formatted # append the parent folder name to path
    Path(output_path).mkdir(parents=True, exist_ok=True) # make the path folders if they dont exist
    return output_path

# Fish emoji site, but replace to change
site = 'https://www.emoji.supply/kitchen/?%F0%9F%90%9F'

# Need to use selenium because using the easy way to fetch web content
# Doesn't allow the site to load in the pictures that we want to save
browser = webdriver.Firefox()
browser.get(site)
html = browser.page_source
browser.quit()

soup = BeautifulSoup(html, 'html.parser')
# We only want the images in the output div, not regular emojis
img_tags = soup.find("div", {"id": "mixmoji-content"}).find_all('img')

urls = [img['src'] for img in img_tags]

output_dir = prepare_output_dir()

for url in urls:
    filename = re.search(r'emojikitchen.*\/([\w_-]+[.](jpg|gif|png))$', url)
    if not filename:
         print("Regex didn't match with the url: {}".format(url))
         continue
    with open(output_dir + "/" + filename.group(1), 'wb') as f:
        if 'http' not in url:
            # sometimes an image source can be relative 
            # if it is provide the base url which also happens 
            # to be the site variable atm. 
            url = '{}{}'.format(site, url)
        response = requests.get(url)
        f.write(response.content)
        
print("Exited successfully. Check output folder for results.")