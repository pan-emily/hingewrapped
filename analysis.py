"""
Hinge Wrapped Dataset Analysis
"""
__author__ = "Emily Pan"
__version__ = "0.1.0"

import json 
import os
import pandas as pd

def analyze_matches(matches):
    matches.to_csv('matches.csv')
    return 

def main():
    """ Main entry point of the app """
    # get the location of 'export' data:
    # dir = input()
    dir = "/Users/emilypan/Documents/export"
    os.chdir(dir)

    # get matches
    with open("matches.json") as f:
        matches_dict = json.load(f)
    f.close()
    matches = pd.DataFrame.from_dict(matches_dict)
    analyze_matches(matches)
    

if __name__ == "__main__":
    main()

