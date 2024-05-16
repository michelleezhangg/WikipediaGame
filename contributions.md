# Contributions

## Project Preparation
In preparation for this project, the file `WGIP.md` outlines the entire improvement proposal from code analysis and breakdown to the improvement proposal with pseudo-code, a high-level description, benefits and costs, and an extensive project milestones section. Including so much detail in the preparation was crucial for me to process everything that needs to be done as well as showcase the improvements I was wishing to make and what is needed to get there.

## Project Implementation
The actual implementation of the project was very tricky. The preparation part were just thoughts, but the hands-on implementing was difficult because of unanticipated issues and time-consuming bugs.

With all of this being said, the implementation of the project, briefly speaking, is an **A\* Search Algorithm** which uses a priority queue that sorts the links based on a heuristic function determined by comparing the keywords from the current link to the final link from extracting the texts of the pages and finding the cosine similarity between them. The highest cosine similarity would sit at the top of the priority queue after adding all of the links of the current page which is a more efficient way to look through the links as opposed to the breadth-first search (BFS) algorithm of the original source code.

### `crawler2.py`
I started implementing this with a general A* algorithm. The priority queue stores the heuristic value or cost starting with the starting page set to 0.0. This main function lies in the `find_path()` function. The other helper functions and classes are the following:

- `get_links(page_url)`: This function uses the `page_url` and fetches the links on the current Wikipedia page using `BeautifulSoup`. The functionality of this is nearly the exact same as the one in the original implementation (`crawler.py`).
- `extract_title(page_url)`: This function takes in the `page_url` and extracts the title from it by taking the last part of the URL and replacing the underscores with spaces. There are issues with this function which can be improved to get the exact title of the Wikipedia page.
- `process_page(page_url)`: This function uses the `wikipedia` library to extract the contents of the page using the title obtained from `extract_title()` helper function. Since the helper function is flawed and may not return a current title, a try-catch statement was added that returns an empty string if a title cannot be found. This is a further improvement that needs to be made. Additionally, the actual essence of the page is included, but there are also additional unnecessary text that can be taken out for more accurate heuristic scores.
- `keyword_extraction(text)`: This function utilizes the `TfidVectorizer` from `sklearn` to extract all of the keywords from `text` which is the contents for the current page. The constant `NUM_FEATURES` is set to 30 as a default. Increasing this value would allow more keywords to be extracted and compared. The keywords are returned in a list sorted first being the top scoring keyword.
- `cosine_sim(current_keywords, finish_keywords)`: This function utilizes the `cosine_similarity()` function from `sklearn` which finds the cosine similarity between two vectors. In this case, since we have lists of keywords, I first made them a string of words separated with spaces and then fit them over a vectorizer which outputted matrices. Applying the function to them, I was able to retrieve the cosine similarity with is the output of this function.
- `heuristic_function(current_page, finish_keywords)`: This function puts together the keywords extraction and cosine similarity to return a find heuristic score (float).
- `class TimeoutErrorWithLogs(Exception)`: This class is exact the same as the one in the original implementation that addresses the possibility of a timeout error based on the `TIMEOUT` constant which I have set to 200 by default.

### `requirements.txt`
All of the libraries from the original implementation is the same. However, because of the added coded, I needed to import the following libraries for the following reasons:

- `wikipedia`: Used to extract the current page's contents. Used in `process_page()`.
- `scikit-learn`: Used for keyword extraction specifically `TfidVectorizer` from `feature_extraction.text` and `cosine_similarity` from `metrics.pairwise`. Used in `keyword_extraction()`, `cosine_sim()`, and `heuristic_function()`.

These were added so that the installation and running instructions in the `README.md` can stay the same.

### `server.py`
This file is all the same as the original implementation with the imports and uses of `crawler` commented out so if the user wished so switch back to that implementation, they can switch back and then comment the import and uses of `crawler2`.

## Documentation
The documentation for this project includes `WGIP.md` detailing the project preparation and improvement proposal, `README.md` detailing the project description, steps to setup and run the project as well as limitations and future work, and this file `contributions.md` documenting the post-implementation containing detailed descriptions of the work done on the project as well as my personal reflections.

Documentation is an important part of software development and serves as a trusted source to explain the code and thought-process behind its implementation. Therefore, I have found it very important to make sure all of these documents are as detailed as possible.

## Reflections
This project has taught me the process of improving an existing implementation. Before getting to the coding part, it is extremely vital to plan out the code and set milestones for oneself.

Certainly, there are things out of my control such as losing the initial progress and needing to get a new computer which set me back many weeks. Additionally, with my weak immune system, I got the flu a few days before finals week which also set me back. But, with all of these troubles, I still managed to implement as many changes that I could.

This taught me to communicate effectively and to persevere through the hardships and do the best I can. Although, my algorithm is not the most effective and I would have loved to have more time to implement the things I wanted to, it works with simple Wikipedia pages and I am able to document my progress along with future work and limitations. This goes back to the communication skill as well. It is important to communicate what has been going on with me along with things I wish I could have done given more time.

## Contributions
This project was done by myself without contributions from other students. I did references the original BFS source code and used Aider and ChatGPT to aid me with debugging and general installation and coding difficulties.