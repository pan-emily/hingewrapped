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

    # matches vs. liked vs. rejected 
    rejected_ct = len(matches[~matches['block'].isna()])
    matched_ct = len(matches[~matches['match'].isna()])
    liked_ct = len(matches[~matches['like'].isna()])
    match_counts = pd.DataFrame([['rejected_ct', rejected_ct], ['matched_ct', matched_ct], ['liked_ct', liked_ct]], 
                                 columns=["match_type", "count"])
    print(match_counts['count'])
    # return matches, rejected, matched, liked
    return matches, match_counts

def main():
    """ Main entry point of the app """
    # get the location of 'export' data:
    # dir = input()
    dir = "/Users/emilypan/Documents/export"
    os.chdir(dir)

    matches, match_counts = analyze_matches(dir)

    # plot pie chart of swipe breakdown 
    fig1 = px.pie(
        match_counts, # dataframe
        values='count', 
        names='match_type', 
        title="Swipe Breakdown", 
        labels={"rejected_ct" : "Rejected", "matched_ct" : "Matched", "liked_ct" : "Liked"}
    )
    # fig1.show()

    app = dash.Dash(__name__)

    app.layout = html.Div(
        children=[
            html.Div(
                children=[
                    html.P(children="🚓", style={'fontSize': "30px",'textAlign': 'center'}, className="header-emoji"), #emoji
                    html.H1(
                        children="Crime Analytics",style={'textAlign': 'center'}, className="header-title" 
                    ), #Header title
                    html.H2(
                        children="Analyze the crime records"
                        " by district in New Zealand"
                        " between 1994 and 2014",
                        className="header-description", style={'textAlign': 'center'},
                    ),
                ],
                className="header",style={'backgroundColor':'#F5F5F5'},
            ), #Description below the header
        
            
            html.Div(
                children=[
                    html.Div(
                    children = dcc.Graph(
                        id = 'pie',
                        figure = fig1,
                    #  config={"displayModeBar": False},
                    ),
                    style={'width': '50%', 'display': 'inline-block'},
                ),
            ],
            className = 'double-graph',
            ), 
        ]
    ) #Four graphs

    app.run_server(debug=True)
    


if __name__ == "__main__":
    main()

