#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 16:59:28 2021

@author: rahulkoneru
"""
from dash import dcc
from dash import html
from dash import dash_table

from datetime import datetime as dt
import plotly.graph_objs as go
import pathlib
import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path().parent
DATA_PATH = PATH.joinpath("../Resource Capacity Planner/datasets/").resolve()
resource_project = pd.read_excel(DATA_PATH.joinpath("04_Resource_Capacity.xlsx"))
resource_list = pd.read_excel(DATA_PATH.joinpath("01_Resource_List.xlsx"))  # List of resources
resource_project_showcase = pd.merge(resource_project,
                                     resource_list[['Emp_ID', 'Name', 'Backup Resource Name', 'Backup Resource ID', 'Exit Date']], how='left', right_on='Emp_ID', left_on="Emp_ID")


skills_available = []
for x in resource_list['Skill Set'].unique():
    y = x.split(",")
    for i in y:
        skills_available.append(i.strip())
skills_available = list(set(skills_available))

# Import Data for the app
demand_agg_total = pd.read_excel(DATA_PATH.joinpath(
    "Resource_Capacity_Planner_Deman_Aggregate_Input.xlsx"))
data_entry_layout = html.Div([
    html.Div([html.H1('Data Input'),
              html.Button('Refresh Data', id='backend-data-refresh-button', n_clicks=0),
              html.Div(id='hidden-data-entry', children='Press Button to Refresh Backend')]),
    html.Div(
        dcc.Tabs(id="tabs-data-entry", value='resource-list', children=[
            dcc.Tab(label='Resource List', value='resource-list'),
            dcc.Tab(label='Project List', value='project-list'),
            dcc.Tab(label='Resource Project', value='resource-project'),
            dcc.Tab(label='Task List', value='task-list'),
            dcc.Tab(label='Leaves', value='leaves'),
            dcc.Tab(label='Holidays', value='holidays'),
            dcc.Tab(label='Actual Time Spent', value='time-spent'),
        ], style={
            'margin': '5px'
        })),
    html.Div(id='tabs-content-data-entry',
             style={'border-style': 'ridge',
                    'border-color': '#000000',
                    'padding': '5px'}),

], style={
    'margin': '5px',
    'padding': '7px'
})

demand_capacity_layout = html.Div([
    html.Div(
        children=html.Div([
            html.H3('Demand vs Capacity View'),
            html.Div(className='twelve columns', style={'border-style': 'ridge', 'border-color': '#000000', 'marign-bottom': '5px'},
                     children=[html.Div(className="three columns",
                                        children=[html.H6("Select Client"),
                                                  dcc.Dropdown(id='client_name_dropdown',
                                                               className='dropdown_list',
                                                               options=[{'label': i, 'value': i}
                                                                        for i in demand_agg_total.Client.unique()],
                                                               multi=False,
                                                               clearable=True,
                                                               placeholder="Select Client")]),
                               html.Div(className="three columns",
                                        children=[html.H6("Select Enagagement"),
                                                  dcc.Dropdown(id='engagement_dropdown',
                                                               className='dropdown_list',
                                                               options=[],
                                                               multi=True,
                                                               clearable=True,
                                                               placeholder='Selet Engagement')]),
                               html.Div(className="three columns",
                                        children=[html.H6("Select Employee(s)"),
                                                  dcc.Dropdown(id='emp_dropdown',
                                                               className='dropdown_list',
                                                               options=[],
                                                               multi=True,
                                                               clearable=True,
                                                               placeholder='Select Employee(s)')]),
                               html.Div(className="three columns",
                                        children=[html.H6("Select Date Range"),
                                                  dcc.DatePickerRange(
                                            id='my-date-picker-range',
                                            min_date_allowed=min(demand_agg_total['Date']),
                                            max_date_allowed=max(demand_agg_total['Date']),
                                            initial_visible_month=min(demand_agg_total['Date']),
                                            # end_date=max(demand_agg_total['Date']),
                                            day_size=50,
                                            display_format="DD MMM, Y")])
                               ]),
            html.Div(className='twelve columns', style={'margin-top': '5px'},
                     children=[html.Div(className="six columns",
                                        children=[html.H6("Team Overview", style={'text-align': 'center'}),
                                                  html.Div(className='H6',
                                                           children=[html.Div(className="two columns",
                                                                              children=[html.H6("Total Demand", style={'text-align': 'center'}),
                                                                                        html.Div(id="team-total-demand", className='H6', style={'text-align': 'center'})]),
                                                                     html.Div(className="two columns",
                                                                              children=[html.H6("Total Capacity", style={'text-align': 'center'}),
                                                                                        html.Div(id="team-total-capacity", className="H6", style={'text-align': 'center'})]),
                                                                     html.Div(className="two columns",
                                                                              children=[html.H6("Excess Capacity", style={'text-align': 'center'}),
                                                                                        html.Div(id="team-excess-capacity", className="H6", style={'text-align': 'center'})]),
                                                                     html.Div(className='two columns',
                                                                              children=[html.H6("Leave Capacity", style={'text-align': 'center'}),
                                                                                        html.Div(id='team-total-leave-capacity', className="H6", style={'text-align': 'center'})]),
                                                                     html.Div(className="two columns",
                                                                              children=[html.H6("Leave Coverage", style={'text-align': 'center'}),
                                                                                        html.Div(id='team-leave-coverage', className="H6", style={'text-align': 'center'})]),
                                                                     html.Div(className="two columns",
                                                                              children=[html.H6("Utliizn Status", style={'text-align': 'center'}),
                                                                                        html.Div(id='team-util-status', className='H6', style={'text-align': 'center'})])]),
                                                  html.Div(className="twelve columns",
                                                           children=[
                                                                     dcc.Graph(id="demand_graph", className='twelve columns',
                                                                               config={
                                                                                   'staticPlot': False,
                                                                                   'scrollZoom': False,
                                                                                   'doubleClick': 'reset',
                                                                                   'showTips': False,
                                                                                   'displayModeBar': False,
                                                                                   'watermark': False},
                                                                               style={'border-style': 'ridge',
                                                                                      'border-color': '#000000'
                                                                                      })])],
                                        style={'border-style': 'ridge', 'border-color': '#000000', 'padding': '5px'}),
                               html.Div(className='six columns',
                                        children=[html.H6('Engagement Employee Overview', style={'text-align': 'center'}),
                                                  html.Div(className='twelve columns',
                                                           children=[html.Div(className='two columns',
                                                                              children=[html.H6('Total Demand', style={'text-align': 'center'}),
                                                                                        html.Div(id='emp-total-demand', className='H6', style={'text-align': 'center'})]),
                                                                     html.Div(className='two columns',
                                                                              children=[html.H6('Total Capacity', style={'text-align': 'center'}),
                                                                                        html.Div(id='emp-total-capacity', className='H6', style={'text-align': 'center'})]),
                                                                     html.Div(className='two columns',
                                                                              children=[html.H6('Excess Capacity', style={'text-align': 'center'}),
                                                                                        html.Div(id='emp_excess_capacity', className='H6', style={'text-align': 'center'})]),
                                                                     html.Div(className='two columns',
                                                                              children=[html.H6('Leave Capacity', style={'text-align': 'center'}),
                                                                                        html.Div(id='emp_leave_capacity', className='H6', style={'text-align': 'center'})]),
                                                                     html.Div(className='two columns',
                                                                              children=[html.H6('Utilization %', style={'text-align': 'center'}),
                                                                                        html.Div(id='emp-util-per-cent', className='H6', style={'text-align': 'center'})]),
                                                                     html.Div(className='two columns',
                                                                              children=[html.H6('Utilizn Status', style={'text-align': 'center'}),
                                                                                        html.Div(id='emp-util-status', className="H6", style={'text-align': 'center'})])]),
                                                  html.Div(className='twelve columns',
                                                           children=[
                                                               dcc.Graph(id='emp_capacity_graph', className='twelve columns',
                                                                         config={
                                                                             'staticPlot': False,
                                                                             'scrollZoom': False,
                                                                             'doubleClick': 'reset',
                                                                             'showTips': False,
                                                                             'displayModeBar': False,
                                                                             'watermark': False},
                                                                         style={'border-style': 'ridge',
                                                                                'border-color': '#000000'})]
                                                           )],
                                        style={'border-style': 'ridge', 'border-color': '#000000', 'padding': '5px'})]),
            html.Div(className='twelve columns',
                     children=[html.H5('Resource to Project Allocation', style={'text-align': 'center'}),
                               dash_table.DataTable(
                         id='resource-list-table',
                         columns=[{
                             'name': '{}'.format(i),
                             'id': '{}'.format(i),
                             'deletable': True,
                             'renamable': True
                         } for i in resource_project_showcase.columns],
                         data=resource_project_showcase.to_dict(
                             'records'),

                         editable=False,
                         row_deletable=False,
                         selected_columns=[],        # ids of columns that user selects
                         selected_rows=[],           # indices of rows that user selects
                         # all data is passed to the table up-front or not ('none')
                         page_action="native",
                         page_current=0,             # page number that user is on
                         page_size=10,                # number of rows visible per page
                         style_cell={                # ensure adequate header width when text is shorter than cell's text
                             'minWidth': 95, 'maxWidth': 95, 'width': 95
                         },
                         style_data={  # overflow cells' content into multiple lines
                             'whiteSpace': 'normal',
                             'height': 'auto',

                         }

                     ),

                     ], style={'border-style': 'ridge',
                               'border-color': '#000000',
                               'padding': '5px',
                               'margin-top': '5px',
                               'margin-bottom': '5px'})
        ]), style={'margin': '5px',
                   'padding': '5px'})

])

status_by_project_layout = html.Div([
    html.Div(
        children=[html.Div([
            html.H3("Utilization Status By Project"),
            html.Div(className='twelve columns', style={'border-style': 'ridge', 'border-color': '#000000', 'marign-bottom': '5px'},
                     children=[html.Div(className="four columns",
                                        children=[html.H6("Select Client"),
                                                  dcc.Dropdown(id='client_name_dropdown-project-status',
                                                               className='dropdown_list',
                                                               options=[{'label': i, 'value': i}
                                                                        for i in demand_agg_total.Client.unique()],
                                                               multi=False,
                                                               clearable=True,
                                                               placeholder="Select Client")]),
                               html.Div(className="four columns",
                                        children=[html.H6("Select Enagagement"),
                                                  dcc.Dropdown(id='engagement_dropdown-project-status',
                                                               className='dropdown_list',
                                                               options=[],
                                                               multi=True,
                                                               clearable=True,
                                                               placeholder='Selet Engagement')]),

                               html.Div(className="four columns",
                                        children=[html.H6("Select Date Range"),
                                                  dcc.DatePickerRange(
                                            id='my-date-picker-range-project-status',
                                            min_date_allowed=min(demand_agg_total['Date']),
                                            max_date_allowed=max(demand_agg_total['Date']),
                                            initial_visible_month=min(demand_agg_total['Date']),
                                            # end_date=max(demand_agg_total['Date']),
                                            day_size=50,
                                            display_format="DD MMM, Y")])
                               ]),
            html.Div(className="twelve columns",
                     children=[
                               dcc.Graph(id="status-by-project", className='twelve columns',
                                         config={
                                             'staticPlot': False,
                                             'scrollZoom': False,
                                             'doubleClick': 'reset',
                                             'showTips': False,
                                             'displayModeBar': False,
                                             'watermark': False},
                                         style={'border-style': 'ridge',
                                                'border-color': '#000000',
                                                'margin-top': '5px'
                                                }),
                               dcc.Graph(id="status-by-project-with-resigns", className='twelve columns',
                                         config={
                                             'staticPlot': False,
                                             'scrollZoom': False,
                                             'doubleClick': 'reset',
                                             'showTips': False,
                                             'displayModeBar': False,
                                             'watermark': False},
                                         style={'border-style': 'ridge',
                                                'border-color': '#000000',
                                                'margin-top': '5px'
                                                })])
        ])
        ])
], style={
    'margin': '5px'
})


ALLOWED_TYPES = (
    "number",
)


skill_search_layout = html.Div([
    html.Div(
        children=[html.Div([
            html.H3("Skill Search For New Projects / Workthreads"),
            html.Div(className='twelve columns', style={'border-style': 'ridge',
                                                        'border-color': '#000000',
                                                        'margin-bottom': '5px',
                                                        'padding-bottom': '5px'},
                     children=[
                         html.Div(className='three columns',
                                  children=[html.H6('Select Resource Designation'),
                                            dcc.Dropdown(id='resource-designation-skill-search',
                                                         className='dropdown_list',
                                                         options=[{'label': i, 'value': i}
                                                                  for i in resource_list.Designation.fillna('Blank').unique()],
                                                         multi=True,
                                                         clearable=True,
                                                         placeholder='Select Resource Designation')]),
                         html.Div(className='three columns',
                                  children=[html.H6('Select Skills To Check For Availability'),
                                            dcc.Dropdown(id='skills-available-skill-search',
                                                         className='dropdown_list',
                                                         options=[{'label': i, 'value': i}
                                                                  for i in skills_available],
                                                         multi=True,
                                                         clearable=True,
                                                         placeholder='Select Skills For Checking Availability')]),
                         html.Div(className="three columns",
                                  children=[html.H6("Select Date Range"),
                                            dcc.DatePickerRange(
                                      id='my-date-picker-range-skill-search',
                                      min_date_allowed=min(demand_agg_total['Date']),
                                      max_date_allowed=max(demand_agg_total['Date']),
                                      initial_visible_month=min(demand_agg_total['Date']),
                                      # end_date=max(demand_agg_total['Date']),
                                      day_size=50,
                                      display_format="DD MMM, Y")]),
                         html.Div(className='three columns',
                                  children=[html.H6('Available Capacity Cutoff'),
                                            dcc.Input(
                                      id="input_range_2", type="number", placeholder="input with range",
                                      min=0, max=1000, step=1,
                                  ), ])
            ]),
        ]),

            html.Div(className='twelve columns',
                     style={'border-style': 'ridge',
                            'border-color': '#000000',
                            'margin-bottom': '5px'},
                     children=[
                         html.Div(className='three columns',
                                  children=[html.H6('Skill Total Demand',
                                                    style={'text-align': 'center'}),
                                            html.Div(id='skill-demand-skill-search',
                                                     className='H6',
                                                     style={'text-align': 'center'})
                                            ]),
                         html.Div(className='three columns',
                                  children=[html.H6('Skill Total Capacity',
                                                    style={'text-align': 'center'}),
                                            html.Div(id='skill-capacity-skill-search',
                                                     className='H6',
                                                     style={'text-align': 'center'})
                                            ]),
                         html.Div(className='three columns',
                                  children=[html.H6('Skill Available Capacity',
                                                    style={'text-align': 'center'}),
                                            html.Div(id='skill-available-capacity-skill-search',
                                                     className='H6',
                                                     style={'text-align': 'center'})]),
                         html.Div(className='three columns',
                                  children=[html.H6('Mitigation Action',
                                                    style={'text-align': 'center'}),
                                            html.Div(id='mitigation-action-skill-search',
                                                     className='H6',
                                                     style={'text-align': 'center'})])
                     ]),
            html.Div(className='twelve columns',
                     style={'border-style': 'ridge',
                            'border-color': '#000000',
                            'margin-bottom': '5px'},
                     children=[
                         dcc.Graph(id='resource-availability-skill-search',
                                   className='twelve columns',
                                   config={
                                             'staticPlot': False,
                                             'scrollZoom': False,
                                             'doubleClick': 'reset',
                                             'showTips': False,
                                             'displayModeBar': False,
                                             'watermark': False},
                                   style={
                                       'border-style': 'ridge',
                                       'border-color': '#000000',
                                       'margin-top': '5px'
                                   })
                     ])

        ],
        style={'margin': '5px'})])
