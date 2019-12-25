# -*- coding: utf-8 -*-
"""
@brief launcher file that contains nav links between different pages
@author: Graham Riches
@date: Sat Dec 21 17:38:10 2019
@description
    This file contains the main launcher and page switching callback. To add
    new pages, make sure they are included in here and linked in the switching
    callback function.
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from pow_app import app
from pages import summary_page

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/summary_page':
        return summary_page.layout
    else:
        return summary_page.layout


if __name__ == '__main__':
    app.run_server(debug=True)
