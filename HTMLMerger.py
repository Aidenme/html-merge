import os
import glob
from bs4 import BeautifulSoup

COLLECTION_PATH = 'C:\Projects\HTML Merge\Collection'

#Finds all the HTML files in an individual text's folder
def collect_HTML():
    html_pathnames = []
    print("Collect runs")
    for root, dirs, files in os.walk(COLLECTION_PATH):
        for file in files:
            if file.endswith('.html'):
                html_pathnames.append(os.path.join(root, file))
            if file.endswith('.htm'):
                html_pathnames.append(os.path.join(root, file))
    
    return html_pathnames

for pathname in collect_HTML():
    print(pathname)