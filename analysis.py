"""
Hinge Wrapped Dataset Analysis
"""
__author__ = "Emily Pan"
__version__ = "0.1.0"

import json 
import os
import pandas as pd
import numpy as np

import dash 
from dash import dcc, html
import plotly.express as px
import seaborn as sns

def analyze_matches(dir):
    # get matches
    with open("matches.json") as f:
        matches_dict = json.load(f)
    f.close()
    matches = pd.DataFrame.from_dict(matches_dict)
    matches["blocks"] = matches['block'].where(matches['block'].isna(), 'reject')
    matches["matches"] = matches['match'].where(matches['match'].isna(), 'match')
    matches["likes"] = matches['like'].where(matches['like'].isna(), 'like')

    matches[['blocks', 'matches', 'likes']] = matches[['blocks', 'matches', 'likes']].fillna('')

    matches["match_type"] = matches["blocks"].combine(matches['matches'], lambda a, b: ((a or "") + (b or "")) or None, None)
    matches["match_type"] = matches["match_type"].combine(matches['likes'], lambda a, b: ((a or "") + (b or "")) or None, None)

    # # matches vs. liked vs. rejected 
    # rejected = matches[~matches['block'].isna()]
    # matched = matches[~matches['match'].isna()]
    # liked = matches[~matches['like'].isna()]

    # return matches, rejected, matched, liked
    return matches

def main():
    """ Main entry point of the app """
    # get the location of 'export' data:
    # dir = input()
    dir = "/Users/emilypan/Documents/export"
    os.chdir(dir)

    matches = analyze_matches(dir)

    # # plot pie chart of matches
    # fig1 = px.pie(
    #     matches # dataframe
    #     values = 
    # )
    


if __name__ == "__main__":
    main()

