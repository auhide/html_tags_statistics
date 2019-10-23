import os
import re

import requests
from bs4 import BeautifulSoup


dir_path = os.path.dirname(os.path.realpath(__file__))

# Creating the path for the folder in which we are going to save the PDFs
DOWNLOAD_PATH = os.path.join(dir_path, 'downloads')


if not os.path.exists(DOWNLOAD_PATH):
    os.mkdir('downloads')


BASE_URL = "http://biglistofwebsites.com/"
resp = requests.get(BASE_URL)
src = resp.text


# Regex for all urls that have a download link for the PDFs
re_lists = r"href\s*=\s*[\'\"](list-top[^\"]+)[\'\"]\s*>"

matches = re.findall(pattern=re_lists,
                     string=src,
                     flags=re.IGNORECASE|re.MULTILINE
)





def download_pdf(url, filename):

    pdf_resp = requests.post(url, verify=False)

    content = pdf_resp.content

    print(f"URL::: {url}")

    print(f"Content::: {str(content)}")

    full_path = os.path.join(DOWNLOAD_PATH, filename + ".pdf")

    print(full_path)

    with open(full_path, "wb") as f:
        f.write(content)


def main():
    pdf_number = 1

    for match in matches:
        
        # Removing the list- from the suburl
        match = re.sub(pattern='list-',
                       repl="", 
                       string=match)

        download_pdf(BASE_URL + "download-" + match, str(pdf_number))
        pdf_number += 1


if __name__ == "__main__":
    main()


# with open(DOWNLOAD_PATH, 'wb'):
#     pass
