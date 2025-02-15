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
    prob_distr = dict()

    if len(corpus[page]) < 1:
        # no outgoing pages, choosing randomly from all possible pages
        for key in corpus.keys():
            prob_distr[key] = 1 / len(corpus)
    else:
        # adds 'page' to dictionary
        prob_distr[page] = (1 - damping_factor) / (len(corpus[page]) + 1)

        # adds links from 'page' to dictionary
        for key in corpus[page]:
            prob_distr[key] = ((damping_factor / len(corpus[page])) +
                               ((1 - damping_factor) / (len(corpus[page])+1)))

    return prob_distr


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()
    sample = None

    # makes pagerank dictionary
    for key in corpus:
        pagerank[key] = 0

    # makes 'n' samples
    for i in range(n):

        # other than 1st sample
        if sample:
            prob_dist = transition_model(corpus, sample, damping_factor)
            sample = random.choices(list(prob_dist.keys()),
                                    list(prob_dist.values()), k=1)[0]

        # 1st sample
        else:
            sample = random.choice(list(corpus.keys()))

        # adds sample to dictionary
        pagerank[sample] += 1

    # formats the data
    for key in pagerank:
        pagerank[key] = pagerank[key] / n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()
    delta = []
    for key in corpus:
        pagerank[key] = 1 / len(corpus)
        delta.append(0)

    check = True
    while check:
        for i, key in enumerate(pagerank):
            # calculates the sum
            sum = 0
            for corpus_key in corpus:
                if key in corpus[corpus_key]:
                    sum += pagerank[corpus_key] / len(corpus[corpus_key])
                if len(corpus[corpus_key]) == 0:
                    sum += pagerank[corpus_key] / len(corpus)
            sum *= damping_factor

            # calculates deltas and new pagerank value
            old = pagerank[key]
            pagerank[key] = ((1 - damping_factor) / len(corpus)) + sum
            delta[i] = abs(old - pagerank[key])

        # checks if all deltas are below 0.001
        check = False
        for val in delta:
            if val >= 0.001:
                check = True

    return pagerank


if __name__ == "__main__":
    main()
