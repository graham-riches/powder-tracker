# -*- coding: utf-8 -*-
"""
@brief app layout for the main summary page
@author: Graham Riches
@date: Sat Dec 21 17:33:24 2019
@description
"""

import os
import json
import flask
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import datetime, timedelta

from pow_app import app
from nrcs_service import NRCSService
from web_scraper import WebScraper

STATIC_PATH = os.path.join(os.getcwd(), 'static')

layout = html.Div(children=[
         html.Div(dbc.Row([
                 dbc.Col(html.Img(src='/static/logo.png', height="70px")),
                 dbc.Col(dbc.NavbarSimple(children=[
                         dbc.NavItem(dbc.NavLink('Summary', href='/summary')),
                         ],
                        brand='Montana Powder Tracker',
                        brand_href='#',
                        color='dark',
                        dark=True))
                         ])),
        html.Div([
                  html.H1('Summary',
                          style={'width': '100%', 'display': 'inline-block',
                                 'text-align': 'center', 'padding': 10})
                 ]),
        html.Div(
                 dcc.Graph(id='current', style={'margin': 5}),
                 style={'width': '49%', 'display': 'inline-block',
                        'border-radius': 10, 'padding': 5, 'vertical-align': 'top'}
                ),
        html.Div(
                 dcc.Graph(id='temp', style={'margin': 5}),
                 style={'width': '49%', 'display': 'inline-block',
                        'border-radius': 10, 'padding': 5, 'vertical-align': 'top'}
                ),
        html.Div([
        html.Div([html.Div(html.H2('Whitefish Forecast', style={'width': '100%'}),
                          style={'width': '100%', 'display': 'inline-block', 'padding': 0,
                         'text-align': 'center', 'backgroundColor': '#343a40'},),
                 html.Div(html.Div(html.Pre(id='whitefish',
                                            style={'width': '98%',
                                                   'height': '98%',
                                                   'backgroundColor': 'white',
                                                   'margin': 'auto',
                                                   'padding': 5,
                                                   'border-radius': 5})),
                          style={'width': '100%', 'display': 'inline-block', 'padding': 5,
                         'text-align': 'center', 'backgroundColor': 'rgba(9, 99, 159, 0.5)',
                         'margin': 'auto'})],
                 style={'width': '49%', 'display': 'table-cell',
                        'border-radius': 10, 'padding': 5,
                        'text-align': 'center', 'backgroundColor': '#343a40',
                        'vertical-align': 'top'}
                ),
        html.Div([html.Div(html.H2('Kootenai Forecast', style={'width': '100%'}),
                          style={'width': '100%', 'display': 'inline-block', 'padding': 0,
                         'text-align': 'center', 'backgroundColor': '#343a40'},),
                 html.Div(html.Div(html.Pre(id='kootenai',
                                            style={'width': '98%',
                                                   'height': '98%',
                                                   'backgroundColor': 'white',
                                                   'margin': 'auto',
                                                   'padding': 5,
                                                   'border-radius': 5})),
                          style={'width': '100%', 'display': 'inline-block', 'padding': 5,
                         'text-align': 'center', 'backgroundColor': 'rgba(9, 99, 159, 0.5)',
                         'margin': 'auto'})],
                 style={'width': '49%', 'display': 'table-cell',
                        'border-radius': 10, 'padding': 5,
                        'text-align': 'center', 'backgroundColor': '#343a40',
                        'vertical-align': 'top'}
                ),], style={'display': 'table', 'width': '100%', 'height': '100%'}),
        html.Div(
                dcc.Interval(
                        id='interval-component',
                        interval=120000,  # update every two minutes
                        n_intervals=0)
                ),
        html.P(id='placeholder')
        ])

# html.Pre(id='whitefish', style={'backgroundColor': 'white'})

@app.callback(Output('current', 'figure'),
              [Input(component_id='interval-component', component_property='n_intervals')])
def get_overnight_stats(n):
    df = pd.read_csv('cache/summary_data.csv')
    with open('cache/latest.json') as latest_query:
        query_info = json.load(latest_query)

    return {'data': [go.Table(header=dict(values=['<b>Site</b>', '<b>Elevation</b>', '<b>Snow Depth</b>', '<b>SWE</b>', '<b>Temperature</b>'],
                                          line_color='black', fill_color='black',
                                          align='center',
                                          font=dict(color='white', size=16),
                                          height=40),
                              cells=dict(values=[df['name'], df['elev'], df['depth'], df['swe'], df['temp']],
                                         height=25, font=dict(color='black', size=12)),
                              columnorder=[1, 2, 3, 4, 5],
                              columnwidth=[80, 80, 80, 80, 80])],
            'layout': dict(height=400,
                           title='Current Measurements - {}'.format(query_info['date']),
                           margin=dict(left=20, right=20, top=60, bottom=20),
                           paper_bgcolor='rgba(9, 99, 159, 0.5)',
                           font=dict(color='white', size=18)),
            }


@app.callback(Output('whitefish', 'children'),
              [Input(component_id='interval-component', component_property='n_intervals')])
def get_whitefish_forecast(n):
    scraper = WebScraper('https://www.wrh.noaa.gov/mso/avalanche/sagwht.php')
    data = scraper.query_by_field('pre')
    with open('cache/whitefish.txt', 'w') as forecast:
        forecast.write(str(data))
    return str(data)


@app.callback(Output('kootenai', 'children'),
              [Input(component_id='interval-component', component_property='n_intervals')])
def get_kootenai_forecast(n):
    scraper = WebScraper('https://www.wrh.noaa.gov/mso/avalanche/sagktn.php')
    data = scraper.query_by_field('pre')
    with open('cache/kootenai.txt', 'w') as forecast:
        forecast.write(str(data))
    return str(data)

@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)


@app.callback(Output('placeholder', 'children'),
              [Input('interval-component', 'n_intervals')])
def run_query(n):
    """
    Query the data periodically using an app callback
    """
    with open('config.json') as config_file:
        site_list = json.load(config_file)
    elevation = []
    site_data = []
    site_name = []
    nrcs_service = NRCSService('powtracker.log')
    today = datetime.now()
    for site in site_list['sites']:
        metadata = nrcs_service.get_station_metadata(site)
        site_name.append(metadata['name'])
        elevation.append(int(metadata['elevation']))
        queries = ['SNWD', 'WTEQ', 'TOBS']
        data_row = []
        for idx, query in enumerate(queries):
            date = '{}-{}-{}'.format(today.year, today.month, today.day)
            request_data = {'stationTriplets': site, 'elementCd': query,
                            'ordinal': '1', 'beginDate': date,
                            'endDate': date, 'beginHour': 0,
                            'endHour': int(today.hour)}
            ts, data = nrcs_service.get_station_hourly_data(request_data)
            if len(data):
                data_row.append(data[-1])  # append the last value
            else:
                data_row.append('NA')
        site_data.append(data_row)
    site_data = np.asarray(site_data)
    df = pd.DataFrame(data=[site_name, elevation, site_data[:, 0],
                            site_data[:, 1], site_data[:, 2]]).transpose()
    df.columns = ['name', 'elev', 'depth', 'swe', 'temp']
    df.to_csv('cache/summary_data.csv')
    latest = {'date': datetime.strftime(today, '%Y-%m-%d %H:%M:%S')}
    with open('cache/latest.json', 'w') as latest_query:
        json.dump(latest, latest_query)
