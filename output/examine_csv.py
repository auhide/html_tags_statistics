import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


CSV = 'tag_symb.csv'
OUTPUT_DIR = 'full_tag_symb.csv'


def save_to_csv():
    df = pd.read_csv(CSV)

    df = df[df['Tag'] != 'style']
    df = df[df['Tag'] != 'script']

    symbols_sum = df['Symbols'].sum()

    df['Percentage'] = df['Symbols'] / symbols_sum
    df['Percentage'] = math.ceil(df['Percentage'] * 100)

    df.to_csv(OUTPUT_DIR, sep=',', index=False)



def plot_csv(show=False):
    
    df = pd.read_csv(OUTPUT_DIR)
    df = df[df['Percentage'] > 1]
    print(df.sort_values(by='Percentage', ascending=False))

    tags = np.asarray(df['Tag'])

    percentages = np.asarray(df['Percentage'])

    # plt.hist(df['Tag'], weights=df['Percentage'], histtype='barstacked')

    plt.plot(tags, percentages)
    plt.xlabel('Tag')
    plt.ylabel('Percentage')
    
    if show:
        plt.show()


if __name__ == "__main__":
    plot_csv(show=True)