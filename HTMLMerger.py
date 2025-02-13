import os
import glob
from bs4 import BeautifulSoup

COLLECTION_PATH = 'C:\Projects\HTML Merge\Collection'

#Finds all the HTML in an individual text's folder
def collect_HTML():
    print("Collect runs")
    for root, dirs, files in os.walk(COLLECTION_PATH):
        for file in files:
            if file.endswith('.html'):
                print(os.path.join(root, file))

collect_HTML()