
import requests as req
import re
from get_urls import URLS_FILE

from bs4 import BeautifulSoup
import pandas as pd


FORMATTING_TAGS = [
        "b",
        "strong",
        "i",
        "em",
        "mark",
        "small",
        "del",
        "ins",
        "sub",
        "sup",
]


OUTPUT_DIR = 'output/tag_symb.csv'


TAG_COUNTER = {}



def generate_src(url):
    '''
    Tries to send a GET request to a website and then returns the source code.
    If the GET request is not successful this function returns None
    '''

    url = url.replace('\n', '')
    url = url.replace(' ', '')
    src = None

    print(f"Curr URL: {url}")
    https_activate = False

    try:
        resp = req.get(f"http://www.{url}", verify=False)
        src = resp.text

    except Exception:
        https_activate = True

    if https_activate:
        
        try:
            resp = req.get(f"https://www.{url}", verify=False)
            src = resp.text

        except Exception:
            pass
    if src:
        return src



def single_tag_counter(html, tag):
    '''Returns a tuple of (tag, characters_inside_tag)'''
    
    get_tag_text = f"<({tag})(?:[^>]+)?>([^<]+)<\/{tag}>"

    # List of matched tuples(1st group, 2nd group)
    tag_count = re.findall(get_tag_text, html)

    tag_counter = 0

    for _, curr_count in tag_count:
        tag_counter += len(curr_count)

    return (tag, tag_counter) 
    


# 1. Scrape the html using BeautifulSoup
# 2. Count all characters corresponding to certain tags
def get_tags_counter(html):
    '''
    Returns a Dictionary with key:value - tag:symbols
    '''
    
    soup = BeautifulSoup(html, 'lxml')
    new_soup = BeautifulSoup(html, 'lxml')
    
    tags = set()

    for tag in soup.find_all():
        tags.add(tag.name)

    tags = sorted(list(tags))
    tag_counter_dict = {}

    for i, tag in enumerate(tags):

        soup_formatted = new_soup
        if tag not in FORMATTING_TAGS:

            for f_tag in FORMATTING_TAGS:
                
                for curr_subtag in soup_formatted(f_tag):
                    curr_subtag.decompose()

        tag_counter = single_tag_counter(str(soup_formatted), tag)
        
        # If there are characters inside the tag
        if tag_counter[1]:
            tag_counter_dict[tag_counter[0]] = tag_counter[1]

    
    print(tag_counter_dict)
    return tag_counter_dict


def add_to_global_dict(dct):

    for key, val in dct.items():
        
        if key in TAG_COUNTER.keys():
            TAG_COUNTER[key] += val
        else:
            TAG_COUNTER[key] = val


        
def main():

    with open(URLS_FILE, "r") as f:
        
        urls = f.readlines()

    for url in urls:
        html = generate_src(url)

        if html:
            curr_dict = get_tags_counter(html)
            add_to_global_dict(curr_dict)


    print(TAG_COUNTER)

    # Creating a DataFrame out of the dictionary
    dataframe = pd.DataFrame(list(TAG_COUNTER.items()))
    dataframe.columns = ['Tag', 'Symbols']

    print(dataframe.sort_values(by=['Symbols'], ascending=False))
    # Writing the DataFrame in a CSV file
    dataframe.to_csv(OUTPUT_DIR, sep=',', index=False)


if __name__ == "__main__":
    # main()
    pass
