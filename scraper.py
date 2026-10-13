#-------------------------------------------------------------------------
# AUTHOR: Jason Le
# FILENAME: scraper.py
# SPECIFICATION: Crawls the Circular Links section of TestingURL.dev from the
#                seed URL using the Question 1 crawler pseudocode. Prints each
#                page's <h1> text and, at the end, every URL in seen.
# FOR: CS 4250 - Assignment #2
# TIME SPENT: 4 hours
#-------------------------------------------------------------------------

# Importing Python libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag

# Defining the seed URL
seed = "https://testingurl.dev/scraping/links/circular"
baseURL = "https://testingurl.dev"

# Creating the frontier and seen collections
frontier = [seed]             
seen = {seed}                    


# Crawling until the frontier is empty
while frontier:

    # Removing the first URL from the frontier
    url = frontier.pop(0) 


    # Retrieving and parsing the Web page
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Request failed:", url, e)
        continue
    soup = BeautifulSoup(response.text, "html.parser")


    # Printing the text contained in the <h1> element
    h1 = soup.find("h1")
    if h1 is not None:
        print(h1.get_text(strip=True))


    # Extracting and processing hyperlinks
    links = []
    for a in soup.find_all("a", href=True):
        link = urljoin(url, a["href"].strip())  
        link = urldefrag(link)[0]                 
        if link.startswith(seed):               
            links.append(link)
    links = sorted(set(links))     
    
    for link in links:
        if link not in seen:
            seen.add(link)
            frontier.append(link)             


# Printing all URLs in seen
print()
for url in sorted(seen):
    print(url)