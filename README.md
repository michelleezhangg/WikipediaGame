# WikipediaGame

## Project Description
This project is an extension of a project started by [Alexander Kurz](https://github.com/alexhkurz) of the Wikipedia link searching game with the source code being https://github.com/alexhkurz/WikipediaGame.git.

The original project utilizes a breadth-first search (BFS) algorithm that extracts the current Wikipedia page's links, stores them in a queue, and then traverses through the links in the queue to find the finishing page. This algorithm, while it is widely used to find the shortest path, can be improved.

My improved implementation is using an **A\* Search Algorithm** that uses a priority queue sorted based on a heuristic determined through keyword extractions and semantic similarities of the links. To gather more information, there is a preprocessing stage of extracting the meaningful words and phrases from the starting and finishing pages to determine the heuristic value for each page.

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

Play the game on [`localhost:5000`](http://127.0.0.1:5000/) (this link will only work after you started the server on your machine (watch the console in case the port number changed to eg `5001`)).

## Testing
The testing for this project involves incrementally writing lines of code and then running it to test it. So far, the overall structure and layout of the code is written, but the heuristic has not been implemented. This is likely going to be finished or at least improved on in the next few days which then, I will update the README with the appropriate testing I conducted. As of now, the testing is very straightforward and simple.

## Limitations

- The UI works as expected only for chrome-based browsers (Chrome, Brave, ...).
- Only tested for pages that are no further than two hops away. 
- Only works for wikipedia pages.
- Implemented via HTTP requests (no websocket connection between client and server).
- Users are identified by IP adress (no cookies or sessions).
- ...

## Parameters

- `RATELIMIT` in `server.py`.
- `TIMEOUT` in `crawler.py`.

## Further Ideas

- Improve the efficiency of the search.
- Add heuristics for faster search.
- Use LLMs to make better guesses, resulting in faster search.
- ...