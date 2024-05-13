# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin
import heapq # for priority queue
import wikipedia # extract page contents
from sklearn.feature_extraction.text import TfidfVectorizer # keyword extraction
from sklearn.metrics.pairwise import cosine_similarity # heuristic cosine similarity

# Define constants
TIMEOUT = 200 # time limit in seconds for the search
NUM_FEATURES = 30 # number of features for keyword extractions

# Define helper functions
def get_links(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, features='lxml')
    all_links = [urljoin(page_url, a['href']) for a in soup.find_all('a', href=True) if '#' not in a['href']]
    links = [link for link in all_links if re.match(r'^https://en\.wikipedia\.org/wiki/[^:]*$', link) and '#' not in link]
    print(f"Found {len(links)} links on page: {page_url}")
    return links

def extract_title(page_url):
    title = page_url.split("/")[-1]
    title = title.replace("_", " ")
    print("Current title:", title)
    return title

def process_page(page_url):
    try:
        page_title = extract_title(page_url)
        page = wikipedia.page(page_title)
        page_contents = page.content
        return page_contents
    except Exception as e:
        print('Error:', e)
        return ''

def keyword_extraction(text):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform([text])

    index = 0
    feature_names = tfidf_vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix[index].toarray().flatten()

    sorted_indices = tfidf_scores.argsort()[::-1]
    keywords = [feature_names[i] for i in sorted_indices[:NUM_FEATURES]]
    return keywords

def cosine_sim(current_keywords, finish_keywords):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([' '.join(current_keywords), ' '.join(finish_keywords)])
    cos_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0]
    return cos_sim

def heuristic_function(current_page, finish_keywords):
    page_text = process_page(current_page)
    if not page_text:
        return 0.0
    page_keywords = keyword_extraction(page_text)
    similarity = cosine_sim(page_keywords, finish_keywords)
    return float(similarity[0])

# Define the main function
def find_path(start_page, finish_page):
    logs = []

    # Process the finish page
    finish_text = process_page(finish_page)
    finish_keywords = keyword_extraction(finish_text)

    # Initialize the priority queue and the set of discovered pages
    queue = [(0.0, 0.0, start_page, [start_page])]
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

                if link == finish_page:
                    logs.append(f"Found finish page: {link}")
                    print(f"Found finish page: {link}")
                    logs.append(f"Search took {elapsed_time} seconds.")
                    print(f"Search took {elapsed_time} seconds.")
                    return path + [link], logs, elapsed_time, len(discovered)
                
                # Compute the cost from the start page to the link
                new_cost = cost + 1.0

                # Compute the estimated cost from the link to the finish page
                estimated_cost = heuristic_function(link, finish_keywords)
                print("Current estimated cost:", estimated_cost)

                # Enqueue the tuple with the total cost
                heapq.heappush(queue, (new_cost + estimated_cost, new_cost, link, path + [link]))
            
            # Update elapsed time
            elapsed_time = time.time() - start_time
        
         # Update elapsed time
        elapsed_time = time.time() - start_time
        
    logs.append(f"Search took {elapsed_time} seconds.")
    print(f"Search took {elapsed_time} seconds.")
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