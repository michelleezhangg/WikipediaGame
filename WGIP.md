# Project 3: Wikipedia Game Improvement Proposal
Author: Michelle Zhang
Email: mizhang@chapman.edu
Course: CPSC 406-01 Algorithm Analysis

## Question
Use *Aider* to study the breadth-first search (BFS) algorithm of the *Wikipedia Game*. Propose an improvement on the Wikipedia Game. Give a high-level description of your improvement. Also provide a pseudo-code description. If you need special libraries (such as word embeddings) say what you are planning to use.

## Code Analysis
First, I used Aider to study the breadth-first search algorithm of the Wikipedia Game. I told it to analyze the coder in server/crawler.py and some improvements that it would make. The improvements are summarized below:

* **Repeated HTTP requests**: The current implementation makes an HTTP request to fetch the page content for every page. This can be slow if the same page gets added to the queue which can lead to unnecessary repeated requests. To combat this, perhaps we can fetch and store and links of a page when it is first visited and then retrieve them from memory when needed. This can cut down on the runtime.
* **Use of a set for a queue**: A set is used to remove duplicated links, however, the set $discovered$ already ensures this. Therefore, removing it from the code could simplify the algorithm and save some memory.
* **Logging**: The code logs a message for each link that is added to the queue. While this is helpful, removing it would help the runtime a little bit.
* **Error handling**: The code raises a $TimeoutErrorWithLogs$ exception if the search time limit is exceeded. This can be handled differently so the caller can handle the situation better. Slight optimization can be used here.
* **Use of $pop(0)$ for dequeuing**: In Python, the $pop(0)$ operation performed on a list is a $O(n)$ runtime. A more efficient operation such as $popleft()$ from the $collections.deque$ library has a time complexity of $O(1)$ and would greatly reduce the runtime since this operation is performed very frequently in the algorithm.
* **Use of $in$ operator for checking if a page is the finished page**: The $in$ operator on Python in a list has a time complexity of $O(n)$. It may be more efficient to store the elements into another data structure that more efficiently checks if an element is in it.

It also pointed out that the BFS algorithm is pretty efficient in terms of time complexity which is $O(V + E)$ where $V$ is the number of Wikipedia pages and $E$ is the number of Wikipedia links. Additionally, each page and each link is only visited once which means it is pretty efficient. A BFS algorithm is quite common to find the shortest path but in this case, it may not be the most intelligent one because we must check all pages regardless of whether the pages seem related or not.

I asked Aider what other algorithms would be useful and yield better time complexity than the current implementation. One response stuck out to me the most: **A\* Search**.

## Improvement Proposal
**A\* Search** uses a *priority queue* instead of a regular queue to decide which page to visit next can be more efficient especially if the algorithm is intelligent enough to find out which words are more similar in meaning. The priority is determined using a **heuristic function** which estimates the cost from the current page to the next page numerically as well as the cost from the current page to the final page. The cost can be decided using the *relevance* of the pages to each other. To numerate the relevance of the pages, there are a combination of strategies that can be used:

* **Keyword Extraction**: Identify words or phrases that can be used to provide context to a body of text through multiple metrics such as word frequency, co-occurrences, Named Identity Recognition (NIR), and more.
* **Semantic Similarity**: Can be done using techniques from Natural Language Processing (NLP) such as $Word2Vec$ or $Doc2Vec$ which can capture the semantic meaning of the word.
* **Link Analysis**: Analyzing the links on the current page. If the pages are closely related to the target page then that means the pages are more relevant to each other.
* **Machine Learning**: You can train a machine learning model if you have access to a large amount of labeled data. The model can learn to predict the relevance of pages with each other which would be able to make the algorithm more accurate. However, this would require a lot of computation resources.

Combining these to create the heuristic is a difficult task but can be extremely beneficial to develop a more sophisticated and efficient algorithm.

## Pseudo-Code
```
# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin
import heapq # for priority queue
from nltk.corpus import stopwords # for keyword extraction
from gensim.models import Word2Vec # for semantic similarity

# Define constants
TIMEOUT = 500 # time limit in seconds for the search

# Define helper functions
def get_links(page_url):
    # Fetch the page content and extract the links
    # Return the links

def preprocess_page(page_url):
    # Fetch the page content and preprocess it
    # Extract the keywords, compute the semantic vector, and analyze the links
    # Return the preprocessed information

def heuristic_function(current_page, finish_page):
    # Compute the estimated cost from the current page to the finish page
    # Use the preprocessed information and a combination of methods
    # Return the estimated cost

# Define the main function
def find_path(start_page, finish_page):
    # Preprocess the start and finish pages
    start_info = preprocess_page(start_page)
    finish_info = preprocess_page(finish_page)

    # Initialize the priority queue and the set of visited pages
    queue = [(0,0, start_page, [start_page])]
    visited = set()

    # Start the timer
    start_time = time.time()

    # Main loop
    while queue and time.time() - start_time < TIMEOUT:
        # Dequeue the tuple with the lowest total cost
        total_cost, cost, current_page, path = heapq.heappop(queue)

        # Check if the current page is the finish page
        if current_page == finish_page:
            # Return the path to the finish page
            return path

        # Mark the current page as visited
        visited.add(current_page)

        # Fetch the links on the current page
        links = get_links(current_page)

        # For each link that has not been visited yet
        for link in links:
            if link not in visited:
            # Compute the cost from the start page to the link
            new_cost = cost + 1

            # Compute the estimated cost from the link to the finish page
            estimated_cost = heuristic_function(link, finish_page)

            # Enqueue the tuple with the total cost
            heapq.heappush(queue, (new_cost + estimated_cost, new cost, link, path + [link]))

    # If the loop finishs without the finish page, return a special value
    return None
```

## High-Level Description
During the preprocessing stage, it would be helpful to preprocess the content of the start and finish pages and extract the keywords, compute the semantic vectors, and analyze links. This information will then be stored in the heuristic function for later use. Some methods that can be used are $Word2Vec$ or $Doc2Vec$ for semantic meaning. The priority queue will be a heap that minimizes the cost calculated by the heuristic function. The main part of the algorithm is a huge while loop that will keep going as long as the queue is not empty and the time limit has not been exceeded. Each iteration of the loop involves dequeuing from the priority queue to retrieve the page with the lowest estimated cost from the finish page and then storing those page's links into the queue. The algorithm will check to see if the final page is reached or if it isn't, it will return $None$ to show that there was no path or that the time limit exceeded.

The heuristic function will be a combination of the methods mentioned before. For instance, the relevance can be computed based on common keywords, semantic similarity, and link analysis. Then, this number will be normalized so it can be compared with the other scores in the priority queue.

## Heuristic Function
A combination of **keyword extractions** and **semantic similarity**.

### Keyword Extractions
The **keyword extractions** would consist of taking out the *stopwords* which are English words like "the", "is", "in", etc. to keep the more unique informative words in the text. Then, the leftover words would be tokenized and stored into a hashmap/dictionary mapping an ID to the word. The frequency of each word would be collected and stored to show which words were the most frequent. To add another layer of complexity, we can create a TF-IDF model from the corpus which would assign a score to each word in the text that represents the relevance of the word to the whole body of text relative to all other documents in the corpus. The keywords would be the highest scored words.

### Semantic Similarity
A popular way to use semantic similarity is using **word embeddings** which creates vector representation of words where words similar in meaning will have similar vector representations. A popular model to do so is *Word2Vec*. However, there are others like *GloVe* and *FastText*. We can also use **cosine similarity** which is done using a *BERT model*. This works by using a tokenizer that converts the sentences into a format that the BERT model can understand. The tokenizer tokenizes the sentences and gets the embeddings for each of the sentences where sentences with similar meaning will have similar vector representations instead of words now. Then, the mean embedding is calculated for the sentences and then we are able to derive the cosine similarity between the mean embeddings. The cosine similarity is a measure of the cosine of the angle between the two vectors and is a common measure of similarity in high-dimensional space.

### Other Options

## Benefits and Costs
A huge benefit is that the algorithm is *more efficient and optimal* than the initial BFS algorithm. The heuristic function will use many combined methods to efficiently find the shortest path by prioritizing pages that are more similar and closely related to the finish page instead of simply searching through all links in a page without factoring in relevance. However, a cost is that this *increases the complexity and expensiveness* of the algorithm severely. The heuristic function can get quite complex to actually be effective. Additionally, there are a lot more computational resources needed to achieve such high efficiency and complexity. There are many *challenges with building a good heuristic function* as well. This requires a lot of testing and experimenting. The heuristic function fetches all of the content of both the start page and finish page. This can slow down the search time and not be as effective as the BFS if the path to the pages are close to begin with. Lastly, *more memory is consumed* with this algorithm because in the worst case, all of the possible links from every page in the path can be stored in the priority queue. Overall, although we want to achieve greater efficiency and complexity in the search algorithm, it is important to acknowledge the costs that come with them. It is constantly a struggle to balance the two in programming.