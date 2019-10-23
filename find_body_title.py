'''
Module with which I try to scrape the text off an article automatically
'''


from get_random_page import (single_tag_counter,
                             get_tags_counter)

import requests as req
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup



class AutomaticArticleScraper:

    def __init__(self, url):

        resp = req.get(url)
        html = resp.text

        self.src = html
        
        self.dct = get_tags_counter(self.src)
        self.df = self.__dct_to_df()



    def scrape_body(self):
        tag = self.find_body()

        soup = BeautifulSoup(self.src, 'lxml')
        for line in soup.find_all(tag):
            print(line)


    def find_body(self):

        try:
            self.df = self.df[self.df['Tag'] != 'style']
        except:
            print("There was no style in this DataFrame")

        try:
            self.df = self.df[self.df['Tag'] != 'a']
        except:
            print("There was no style in this DataFrame")
        
        try:
            self.df = self.df[self.df['Tag'] != 'script']
        except:
            print("There was no style in this DataFrame")


        max_row = self.df[self.df['Symbols'] == self.df['Symbols'].max()]

        tag = max_row['Tag'].to_string(index=False)

        return tag.strip()

    


    def __dct_to_df(self):
        df = pd.DataFrame(list(self.dct.items()))
        
        df.columns = ['Tag', 'Symbols']

        print(df)

        return df
    






if __name__ == "__main__":

    url = 'https://diarionline.com.br/index.php?s=noticia&id=113095'

    scraper = AutomaticArticleScraper(url)

    scraper.scrape_body()