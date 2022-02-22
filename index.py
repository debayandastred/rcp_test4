#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 17:01:42 2021

@author: rahulkoneru
"""

from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from layout import data_entry_layout, demand_capacity_layout, status_by_project_layout, skill_search_layout
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Data Inputs | ', href='/apps/data_entry'),
        dcc.Link('Demand vs Capacity | ', href='/apps/demand_capacity'),
        dcc.Link('Status by Project | ', href='/apps/status_by_project'),
        dcc.Link('Skill Search', href='/apps/skill_search'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/demand_capacity':
        return demand_capacity_layout
    if pathname == '/apps/data_entry':
        return data_entry_layout
    if pathname == "/apps/status_by_project":
        return status_by_project_layout
    if pathname == "/apps/skill_search":
        return skill_search_layout
    else:
        return data_entry_layout


if __name__ == '__main__':
    app.run_server(debug=True, port=8000, host='127.0.0.1')
