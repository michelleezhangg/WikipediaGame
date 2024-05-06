# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin
import heapq # for priority queue
import wikipedia
from rake_nltk import Rake
# from gensim.models import Word2Vec # for semantic similarity

# Define constants
TIMEOUT = 1 # time limit in seconds for the search

# Define helper functions
def get_links(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_links = [urljoin(page_url, a['href']) for a in soup.find_all('a', href=True) if '#' not in a['href']]
    links = [link for link in all_links if re.match(r'^https://en\.wikipedia\.org/wiki/[^:]*$', link) and '#' not in link]
    print(f"Found {len(links)} links on page: {page_url}")
    return links

def extract_title(page_url):
    title = page_url.split("/")[-1]
    title = title.replace("_", " ")
    print(title)
    return title

def preprocess_page(page_url):
    page_title = extract_title(page_url)
    page = wikipedia.page(page_title)
    page_contents = page.content
    return page_contents

def keyword_extraction(text):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases

def heuristic_function(current_page, finish_page):
    # Compute the estimated cost from the current page to the finish page
    # Use the preprocessed information and a combination of methods
    # Return the estimated cost
    current_keywords = keyword_extraction(current_page)
    finish_keywords = keyword_extraction(finish_page)
    return 0

# Define the main function
def find_path(start_page, finish_page):
    logs = []

    # Preprocess the start and finish pages
    start_info = preprocess_page(start_page)
    finish_info = preprocess_page(finish_page)

    # Initialize the priority queue and the set of discovered pages
    queue = [(0,0, start_page, [start_page])]
    discovered = set()

    # Start the timer and calculate elapsed time
    start_time = time.time()
    elapsed_time = time.time() - start_time

    # Main loop
    while queue and elapsed_time < TIMEOUT:
        # Dequeue the tuple with the lowest total cost
        total_cost, cost, current_page, path = heapq.heappop(queue)

        # Check if the current page is the finish page
        if current_page == finish_page:
            # Return the path to the finish page
            logs.append(f"Found finish page: {current_page}")
            print(f"Found finish page: {current_page}")
            logs.append(f"Search took {elapsed_time} seconds.")
            print(f"Search took {elapsed_time} seconds.")
            return path + [current_page], logs, elapsed_time, len(discovered)

        # Mark the current page as discovered
        discovered.add(current_page)

        # Fetch the links on the current page
        links = get_links(current_page)

        # For each link that has not been discovered yet
        for link in links:
            if link not in discovered:
                # Compute the cost from the start page to the link
                new_cost = cost + 1

                # Compute the estimated cost from the link to the finish page
                estimated_cost = heuristic_function(link, finish_page)

                # Enqueue the tuple with the total cost
                heapq.heappush(queue, (new_cost + estimated_cost, new_cost, link, path + [link]))

        elapsed_time = time.time() - start_time
    
    logs.append(f"Search took {elapsed_time} seconds.")
    print(f"Search took {elapsed_time} seconds.") # Add a print statement to log the elapsed time
    logs.append(f"Discovered pages: {len(discovered)}")
    print(f"Discovered pages: {len(discovered)}")
    logs.append(f"Total cost: {total_cost}")
    print(f"Total cost: {total_cost}")
    raise TimeoutErrorWithLogs("Search exceeded time limit.", logs, elapsed_time, len(discovered))

class TimeoutErrorWithLogs(Exception):
    def __init__(self, message, logs, time, discovered):
        super().__init__(message)
        self.logs = logs
        self.time = time
        self.discovered = discovered