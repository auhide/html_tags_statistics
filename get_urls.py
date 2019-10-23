
import os
import re

import pandas as pd
import numpy as np

from tabula import read_pdf



pdfs_folder = "downloads"
URLS_FILE = "urls.txt"



pdfs = os.listdir("downloads")

arr = np.asarray([])



if __name__ == "__main__":

    for i, pdf in enumerate(pdfs):
        
        curr_pdf_path = os.path.join(pdfs_folder, pdf)
        
        # Converting the pdf table to the DataFrame table
        curr_df = read_pdf(curr_pdf_path)
        curr_np_arr = np.asarray(curr_df["url"])

        arr = np.append(curr_np_arr, arr)


    with open(URLS_FILE, "w") as f:
        
        urls_set = set(arr)
        
        for url in urls_set:
            f.write(f"{url} \n")

            print(f"Added {url}")

    
