

import os
import re
from reprlib import recursive_repr
import sys
import argparse
import requests
import concurrent.futures

from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from requests.exceptions import HTTPError, ConnectionError


def fix_img_path(link, logo_path):
    """
    This function checks whether an logo path is relative or absoult.
    If the function found the logo path as relative, it make sure to make it absolute

    Args:
        - link (str) : The link that the logo founds in
        - logo_path (str) : The path of the logo that under inspection

    Return:
        If the logo path is absolute return the same received path, otherwise, return the fixed logo path
    """

    # Fix the network location part if needed
    if not bool(urlparse(logo_path).netloc):
        logo_path = urljoin(link, logo_path)

    # Fix the scheme part if needed (assuming only https)
    if not str(logo_path).startswith(("https://", "http://")):
        logo_path = urljoin("https://", logo_path)

    return logo_path


def crawl_logo(link, soup):
    """
    This function search the website's logo and fix the logo's path
    (with the assumption that the website's logo will come first because 
    in the absolute most cases the logo is the first image in the HTML structure)

    Args:
        - link (str) : A link to the crawled website
        - soup (bs) : A BeauifulSoup object which will help to found the website's logo

    Return:
        Absolute logo path
    """
    img_tags = soup.select("a img")
    return fix_img_path(link, img_tags[0]["src"])


def clean_phones(phones):
    """
    This function clean any character from a phone number except '+', '(', ')'

    Args:
        - phones (list) : list of phone numbers

    Return:
        A cleaned phones list
    """
    clean_phones = []
    for phone in phones:
        # Clean unwanted chars
        phone = phone.replace("-", " ").replace("/", " ")
    
        # Clean small numbers
        if len(phone) < 11:
            continue

        clean_phones.append(phone)
    return clean_phones


def crawl_phones(soup):
    body_tag_strings = soup.body.strings
    found_phones = set()
    for string in body_tag_strings:
        string = string.replace("\r", "").replace("\n", "").replace("\r", "").replace(" ", "")
        phones = re.findall(r"[\d\+\(]?[\(]?[\d]+[\)\s\-\\\/]?[\s]?[\(]?[\-\\\/]?[\d]+[\s\-\\\/]?[\)]?[\s]?[\d]+[\s\-\\\/]?[\d]+[\s\-\\\/]?[\d]+", string)
        if len(phones) > 0:
            found_phones = found_phones.union(set(phones))

    return clean_phones(list(found_phones))


def crawl_link(link):
    """
    This function crawl a received link according to reuired in the assignment

    Args:
        - link (str) : link to a webpage to crawl

    Return:
        nothing
    """
    print(f"Start crawl link {link.rstrip()}", file=sys.stderr) if VERBOSE else None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    try:
        resp = requests.get(link.rstrip(), headers=headers)
    except ConnectionError:
        print("Connection error", file=sys.stderr)
    except HTTPError:
        print("Http error", file=sys.stderr)

    soup = BeautifulSoup(resp.text, "html.parser")
    try:
        link_data = {
            "logo": crawl_logo(link, soup),
            "phones": crawl_phones(soup),
            "website": link.rstrip()
        }
    except IndexError:
        print(f"No logos found in: {link.rstrip()} | Http status code is: " + str(resp.status_code), file=sys.stderr)

    print(f"Finish crawl link {link.rstrip()}", file=sys.stderr) if VERBOSE else None
    
    print(link_data, file=sys.stdout)


VERBOSE = None
THREADS_NUM = None

if __name__ == "__main__":
    # Create and define the argument parser object
    parser = argparse.ArgumentParser(description="CLI web crawler")
    parser.add_argument("-t", "--threads", dest="threads_num", type=int, metavar="", default=16, help="Specifying how many threads to use. Default is 16")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=False, help="Display application messages during running")
    parser.add_argument("infile", nargs="*", type=argparse.FileType, default=sys.stdin)
    args = parser.parse_args()

    # Update the VERBOS global variable with the user/default value
    VERBOSE = args.verbose
    
    # Check if some input supplied to stdin
    if sys.stdin.isatty():
        print("No input supplied to the CLI. Exit now", file=sys.stderr) if VERBOSE else None 
        os._exit(0)

    # Update the THREADS_NUM gloval variable that indicate how many threads to use during execution
    THREADS_NUM = args.threads_num
    print(f"The CLI will use {THREADS_NUM} threads", file=sys.stderr) if VERBOSE else None

    # Execute the the crawler concurrently using ThreadPool     
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS_NUM) as executor:
        results = executor.map(crawl_link, args.infile)