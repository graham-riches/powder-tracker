# -*- coding: utf-8 -*-
"""
@brief main pow tracker app
@author: Graham Riches
@date: Sat Dec 21 08:30:52 2019
@description
    Main dash application launching point.
"""

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions'] = True
server = app.server
