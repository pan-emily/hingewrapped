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
from datetime import datetime

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

def parse_time(active_months, active_times, dt):
    month_to_alpha = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', 
                    '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
    day_raw, time_raw = dt.split('T')
    year, month, day = day_raw.split('-')
    hour = time_raw.split(':')[0]
    if year == '2022':
        active_months[month_to_alpha[month]] += 1
        active_times[hour] += 1
    return active_months, active_times

def analyze_activity(matches):
    active_months = {'January': 0, 'February': 0, 'March': 0, 'April': 0, 'May': 0, 
                'June': 0, 'July': 0, 'August': 0, 'September': 0, 'October': 0, 
                'November': 0, 'December': 0}
    active_times = {'00': 0, '01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0, 
                    '07': 0, '08': 0, '09': 0, '10': 0, '11': 0, '12': 0, '13': 0, 
                    '14': 0, '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0, 
                    '21': 0, '22': 0, '23': 0}
    for index, row in matches.iterrows():
        if type(row['like']) == type([]):
            # date in form yyyy-mm-ddThh:mm:ss
            dt = row['like'][0]['timestamp']
            active_months, active_times = parse_time(active_months, active_times, dt)
        if type(row['match']) == type([]):
            # date in form yyyy-mm-ddThh:mm:ss
            dt = row['match'][0]['timestamp']
            active_months, active_times = parse_time(active_months, active_times, dt)
        if type(row['block']) == type([]):
            # date in form yyyy-mm-ddThh:mm:ss
            dt = row['block'][0]['timestamp']
            active_months, active_times = parse_time(active_months, active_times, dt)

    months = pd.DataFrame(list(active_months.items()), columns=['Month', 'Swipes'])
    hours = pd.DataFrame(list(active_times.items()), columns=['Hour', 'Swipes'])
            
    return months , hours


def main():
    """ Main entry point of the app """
    # get the location of 'export' data:
    dir = input("Enter directory of export folder: ")
    currdir = os.getcwd()
    os.chdir(dir)

    matches, match_counts = analyze_matches(dir)
    months, hours = analyze_activity(matches)

    os.chdir(currdir)

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

    # waffle plot of all people -> matched -> met (not matched + (matched - met) + met)
    waffle_data = pd.Series({'Rejected' : match_counts['count'][0], 'Matched but Not Met' : total_matches - total_met, 'Met' : total_met})
    title = 'How You Swiped'

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

    fig3 = px.bar(months, x='Month', y='Swipes')

    fig4 = px.bar(hours, x='Hour', y='Swipes')

    app = dash.Dash(__name__)

    app.layout = html.Div(
        children=[
            html.Div(
                children=[
                    html.Div( children=[
                        html.Img(src='assets/hinge_logo.png', style={'height':'50%', 'width':'50%'})
                        ], style={'textAlign': 'center'}
                    ),
                    html.H1(
                        children="2022 Hinge Wrapped",style={'textAlign': 'center', 'font-family':'impact, sans-serif', 'font-size':'40px'}, className="header-title" 
                    ), #Header title
                    html.H2(
                        children="Dating Wrapped, but using real Hinge data",
                        style={'textAlign': 'center', 'font-family': 'gill sans, sans-serif', 'color': '#808080'},
                    ),
                ],
                className="header", # style={'backgroundColor':'#F5F5F5'},
            ), #Description below the header

            html.Div(
                children=[ 
                    html.Div(
                        children=[ 
                            html.H2(
                                children="This year, you swiped on {total_swipes} people. ".format(total_swipes=total_swipes),
                                style={'fontSize':'35px', 'font-family': 'gill sans, sans-serif'}
                            ),
                        ], style={'height':'100%', 'width':'50%', 'display':'inline-block', 'float':'left', 'margin-left' : '20%', 'textAlign':'center', }
                    ), 
                    html.Div(
                        children=[
                            html.Img(src='assets/trophy.png', style={'width':'60%'})
                        ],
                        style={'height':'100%', 'width':'20%', 'fontSize': "30px",'display':'inline-block', 'mragin-right':0}
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
            ), 

            html.Div(
                children=[
                    html.Div(
                        children=[
                            dcc.Graph(figure=fig3), 
                        ]
                    ), 
                    html.Div(
                        children=[
                            dcc.Graph(figure=fig4), 
                        ]
                    )
                ]
            )
        ],
    ) 

    # app.run_server(debug=True)
    app.run_server()
    


if __name__ == "__main__":
    main()

