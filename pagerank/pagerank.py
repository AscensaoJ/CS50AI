import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Local variables
    # Holds odds (value) for given page (key) in corpus
    page_odds = dict()
    # Odds surfer navigates to a specific page at random given a damping factor and number of pages
    page_count = len(corpus)
    rand_odds = (1 - damping_factor) / page_count
    # Gets the number of links on page for later averaging
    links_on_page = len(corpus[page])


    # Iterate over each page i in corpus
    for i in corpus:
        # Add newly found page i as key with base value of random odds surfer will navigate to it
        if i not in page_odds:
            page_odds[i] = rand_odds
        # Logic for specific page whose links affect navigation odds
        if i == page:
            # Iterate over each page link j on page i
            for j in corpus[i]:
                # Add newly found page link j as key with base value of random odds surfer will navigate to it
                if j not in page_odds:
                    page_odds[j] = rand_odds
                # Adds average odds surfer will navigate to page link j
                page_odds[j] += damping_factor / links_on_page

    return page_odds

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Local variables
    pages = []
    # Holds sums for later averaging
    odds_sums = dict()
    # Holds average odds
    avg_odds = dict()

    # Get pages and fill dictionaries with base values for each key
    for page in corpus:
        pages.append(page)
        odds_sums[page] = 0
        avg_odds[page] = 0
    
    # Get initial sample
    rand_page = random.choice(pages)

    # Logic to calculate sums for later averaging
    for i in range(n):
        # Get odds for randomly chosen page
        page_odds = transition_model(corpus, rand_page, damping_factor)
        # Add odds to odds_sums
        for page in page_odds:
            odds_sums[page] += page_odds[page]
        # Get next sample
        rand_page = random.choices(pages, list(page_odds.values()))[0]

    # Average and store odds for each page
    for page in odds_sums:
        avg_odds[page] = odds_sums[page] / n

    return avg_odds

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Local variables
    page_count = len(corpus)
    pages = []
    rand_odds = (1 - damping_factor) / page_count
    page_odds = dict()
    # Resolution for iterative algorithm
    converge_scale = 0.00001
    max_change = 1
    # Get pages and fill dictionaries with base values for each key
    for page in corpus:
        pages.append(page)
        page_odds[page] = 1 / page_count

    # Iterative algorithm
    # Exits when the largest change is below defined resolution
    while max_change >= converge_scale:
        new_odds = dict()
        change = 0
        # Find page rank for given page
        for page in corpus:
            sum_odds = 0
            for other_page in corpus:
                # Prevent collision
                if page is other_page:
                    continue
                # Factor in pages that link to current page
                if page in corpus[other_page]:
                    sum_odds += page_odds[other_page] / len(corpus[other_page])
            # Calculate page rank
            new_odds[page] = rand_odds + (damping_factor * sum_odds)

        # Check and update changes and odds
        for page in corpus:
            # Calculate change
            page_change = abs(page_odds[page] - new_odds[page])
            # Update odds
            page_odds[page] = new_odds[page]
            # Update change if needed
            if page_change > change:
                change = page_change
        # Update maximum change for this loop
        max_change = change

    return page_odds

if __name__ == "__main__":
    main()
