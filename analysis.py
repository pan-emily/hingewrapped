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
import dash_daq as daq 
import plotly.express as px
import plotly.graph_objs as go
import seaborn as sns

def process_matches(matches):
    matches["blocks"] = matches['block'].where(matches['block'].isna(), 'reject')
    matches["matches"] = matches['match'].where(matches['match'].isna(), 'match')
    matches["likes"] = matches['like'].where(matches['like'].isna(), 'like')

    matches['we_mets'] = matches['we_met'].where(matches['we_met'].isna(), 'met')

    matches[['blocks', 'matches', 'likes', 'we_mets']] = matches[['blocks', 'matches', 'likes', 'we_mets']].fillna('')

    matches["match_type"] = matches["blocks"].combine(matches['matches'], lambda a, b: ((a or "") + (b or "")) or None, None)
    matches["match_type"] = matches["match_type"].combine(matches['likes'], lambda a, b: ((a or "") + (b or "")) or None, None)

    return matches

def swipe_breakdown(matches):
    # matches vs. liked vs. rejected 
    rejected_ct = len(matches[~matches['block'].isna()])
    matched_ct = len(matches[~matches['match'].isna()])
    liked_ct = len(matches[~matches['like'].isna()])
    match_counts = pd.DataFrame([['Rejected', rejected_ct], ['Matched', matched_ct], ['Liked', liked_ct]], 
                                 columns=["match_type", "count"])
    # return matches, rejected, matched, liked
    return match_counts

def analyze_matches(dir):
    # get matches
    with open("matches.json") as f:
        matches_dict = json.load(f)
    f.close()
    matches = pd.DataFrame.from_dict(matches_dict)

    matches = process_matches(matches)

    match_counts = swipe_breakdown(matches)
    # return matches, rejected, matched, liked
    return matches, match_counts


def main():
    """ Main entry point of the app """
    # get the location of 'export' data:
    # dir = input()
    dir = "/Users/emilypan/Documents/export"
    os.chdir(dir)

    matches, match_counts = analyze_matches(dir)

    # calculate total swipes
    total_swipes = len(matches)

    total_matches = match_counts['count'][1] + match_counts['count'][2]
    total_met = len(matches[~matches['we_met'].isna()])

    # get percentage of matches to swipes 
    match_percentage = round((total_matches) / total_swipes * 100, 2)

    # plot pie chart of swipe breakdown 
    fig1 = px.pie(
        match_counts, # dataframe
        values='count', 
        names='match_type', 
        title='Swipe Breakdown'
    )
    # fig1.show()

    # waffle plot of all people -> matched -> met (not matched + (matched - met) + met)
    waffle_data = pd.Series({'Rejected' : match_counts['count'][0], 'Matched but Not Met' : total_matches - total_met, 'Met' : total_met})
    title = 'How You Swiped'

    # ds = pd.Series({'Alpha' : 67, 'Bravo' : 30, 'Charlie' : 20, 'Delta': 12, 'Echo': 23, 'Foxtrot': 56})
    Xlim = 50
    Ylim = 13
    Xpos = 0
    Ypos = 40 ##change to zero for upwards
    series = []
    for name, count in waffle_data.iteritems():
        x = []
        y = []
        for j in range(0, count):
            if Xpos == Xlim:
                Xpos = 0
                Ypos -= 1 ##change to positive for upwards
            x.append(Xpos)
            y.append(Ypos)
            Xpos += 1
        series.append(go.Scatter(x=x, y=y, mode='markers', marker={'symbol': 'star', 'size': 8}, name=f'{name} ({count})'))


    fig2 = go.Figure(dict(data=series, layout=go.Layout(
        title={'text': title, 'x': 0.5, 'xanchor': 'center'},
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False,zeroline= False, showline=False, visible=False, showticklabels=False),
        yaxis=dict(showgrid=False,zeroline= False, showline=False, visible=False, showticklabels=False),
    )))

    app = dash.Dash(__name__)

    app.layout = html.Div(
        children=[
            html.Div(
                children=[
                    html.P(children="🚓", style={'fontSize': "30px",'textAlign': 'center'}, className="header-emoji"), #emoji
                    html.H1(
                        children="2022 Hinge Wrapped",style={'textAlign': 'center'}, className="header-title" 
                    ), #Header title
                    html.H2(
                        children="Dating Wrapped, but using real Hinge data",
                        className="header-description", style={'textAlign': 'center'},
                    ),
                ],
                className="header",style={'backgroundColor':'#F5F5F5'},
            ), #Description below the header

            html.Div(
                children=[ 
                    html.Div(
                        children=[
                            html.P(children="🚓"),
                        ],
                        style={'height':100, 'width':'40%', 'fontSize': "30px",'display':'inline-block', 'float': 'left', 'margin-left':100, 'mragin-right':0}
                    ),
                    html.Div(
                        children=[ 
                            html.P(
                                children="This year, you swiped on {total_swipes} people. ".format(total_swipes=total_swipes),
                            ),
                        ], style={'height':100, 'width':'40%', 'display':'inline-block', 'float':'right', 'textAlign':'center'}
                    )  
                ]
            ),
        
            html.Div([
                html.Div(
                    children=[
                        dcc.Graph(
                            id = 'pie',
                            figure = fig1,
                            ),
                    ],  style={'height':300, 'width':500, 'float':'left', 'margin':0}# style={'padding': 10, 'flex': 1}
                ), 

                html.Div(
                    children=[ 
                        html.P(
                            children="Out of the {total_swipes} people you met, you matched with {match_percentage}% of them.".format(total_swipes=total_swipes,
                                        match_percentage=match_percentage), 
                            style={'margin-top': 25}, 
                        ),
                    ],  style={
                        'height':350, 
                        'width':400, 
                        'background-color':'#3BA27A', 
                        'float':'right', 
                        'margin':0, 
                        'margin-top':50}# style={'padding':10, 'flex':1}
                ),
            ],  
            ),
        
            #number of 'we met's 
            html.Div(
                children=[ 
                    html.Div(
                        children=[ 
                            html.P(children="This year, you really enjoyed meeting new people. You met {we_met} people!".format(we_met=total_met)), 
                        ], 
                        style={
                            'height':100, 
                            'width':800, 
                            'margin-top':700
                            # 'background-color':'#111111', 
                        }
                    ),
                    html.Div(
                        children=[ 
                            dcc.Graph(
                            id='waffle', 
                            figure=fig2
                            )
                        ],
                    )
                ]
            )
        ]
    ) #Four graphs

    app.run_server(debug=True)
    


if __name__ == "__main__":
    main()

