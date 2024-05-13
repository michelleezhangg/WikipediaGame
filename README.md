# WikipediaGame

## Project Description
This project is an extension of a project started by [Alexander Kurz](https://github.com/alexhkurz) of the Wikipedia link searching game with the source code located in the following repository: https://github.com/alexhkurz/WikipediaGame.git.

The original project utilizes a breadth-first search (BFS) algorithm that extracts the current Wikipedia page's links, stores them in a queue, and then traverses through the links in the queue to find the finishing page. This algorithm, while it is widely used to find the shortest path, can be improved.

My improved implementation is using an **A\* Search Algorithm** that uses a priority queue sorted based on a heuristic determined through keyword extractions and semantic similarities of the links. To gather more information, there is a processing stage of extracting the meaningful words and phrases from the every page to determine the heuristic value for each page using cosine similarity.

Certainly, there are improvements to be made mentioned further in this README file. This is merely the current implementation so far.

## Installation

(these instructions should work under GNU/Linux and Macos and WSL)

Prerequisites: Python

```
git clone https://github.com/michelleezhangg/WikipediaGame.git
cd WikipediaGame/server
source setup.sh
```

Starting the server:

```
python server.py
```

Note: if the code above did not work, use `python3`. This may because of newer chips such as an M3 Chip.

```
python3 server.py
```

Play the game on [`localhost:5000`](http://127.0.0.1:5000/) (this link will only work after you started the server on your machine (watch the console in case the port number changed to eg `5001`)).

## Testing
The testing for this project involves incrementally writing lines of code and then running it to test it. It involves using multiple print statements to locate where errors are arising.

In terms of experimenting with different Wikipedia pages, I started with a simple start and finish page such as `https://en.wikipedia.org/wiki/Cookie` and `https://en.wikipedia.org/wiki/Flour` and then moving onto more complex and unrelated finishing pages to the starting pages. However, in the process of doing these tests, errors have occurred which are addressed below.

## Parameters

### `crawler.py` (original implementation)
- `RATELIMIT` in `server.py`.
- `TIMEOUT` in `crawler.py`.

### `crawler2.py` (new implementation)
- `NUM_FEATURES` in `crawler2.py`.
- `TIMEOUT` in `crawler2.py`.

## Limitations

### Logistical Limitations
- The UI works as expected only for chrome-based browsers (Chrome, Brave, ...).
- Only tested for pages that are no further than two hops away. 
- Only works for wikipedia pages.
- Implemented via HTTP requests (no websocket connection between client and server).
- Users are identified by IP adress (no cookies or sessions).

### Algorithmic Limitations
- **Title/URL Mismatch**: The `wikipedia` library can only extract the text from the Wikipedia pages with the title of the page instead of the URL which is given. This makes it difficult for Wikipedia pages with complex titles where the title does not match the end of the URL. In my code, I chose to skip those pages and leave them for future work which can help to improve the search. As of now, these pages will just be skipped with a heuristic score of 0.
- **Similar Titled Pages**: Some Wikipedia pages have extremely similar titles or are subpages of other pages which makes it difficult for the `wikipedia` library to search for those pages because it runs into too many possibilities of other pages.

## Future Work

- **Title/URL Mismatch**: Either find a way to directly put in the URL or find a better way to extract the title from a Wikipedia page from the URL to make sure that all of the pages are visited.
- **Similar Titled Pages**: Similar to the first problem, if there was a way to uniquely identify a page using the URL with the constraint the `wikipedia` library only allowing Wikipedia page titles.
- **Extracting The Useful Text**: Currently, the text extracted from each page including everything on the page. Since not all of the information (especially the top and bottom of the Wikipedia page) are needed, removing these texts can lead to more accurate heuristics since we would truly get the essence of the page.