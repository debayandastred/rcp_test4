#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 13:55:28 2021

@author: rahulkoneru
"""

import pathlib
import pandas as pd
import numpy as np

PATH = pathlib.Path('__file__').parent
DATA_PATH = PATH.joinpath(
    "../Resource Capacity Planner/datasets").resolve()
resource_list = pd.read_excel(DATA_PATH.joinpath("01_Resource_List.xlsx"))  # List of resources
task_list = pd.read_excel(DATA_PATH.joinpath("03_Task_List.xlsx"))  # List of Tasks
holidays = pd.read_excel(DATA_PATH.joinpath('05_Holiday_List.xlsx'))
leaves = pd.read_excel(DATA_PATH.joinpath("06_Leave_List.xlsx"))
resource_project = pd.read_excel(DATA_PATH.joinpath("04_Resource_Capacity.xlsx"))
demand_agg_total = pd.read_excel(DATA_PATH.joinpath(
    "Resource_Capacity_Planner_Deman_Aggregate_Input.xlsx"))
project_list = pd.read_excel(DATA_PATH.joinpath("02_Project_List.xlsx"))

# Resource List Cleanup
resource_list["Skill Set"] = resource_list["Skill Set"].str.replace(
    ",", " , ").str.replace("  ", "")
resource_list["Skill Set"] = resource_list["Skill Set"].str.upper()

# Task List Cleanup
task_list["Engagement"] = np.where(
    task_list["Engagement"] != task_list["Engagement"], task_list['Client'], task_list['Engagement'])

# Project List Cleanup
project_list["Skills"] = project_list["Skills"].str.replace(",", " , ").str.replace("  ", " ")
project_list["Skills"] = project_list["Skills"].str.upper()
# resource_capacity_share["Client"] = np.where(
#    resource_capacity_share["Client"] != resource_capacity_share["Client"], "Tredence Internal", resource_capacity_share["Client"])

# Export Datasets
resource_list.to_excel(DATA_PATH.joinpath("01_Resource_List.xlsx"), index=False)
task_list.to_excel(DATA_PATH.joinpath("03_Task_List.xlsx"), index=False)
project_list.to_excel(DATA_PATH.joinpath("02_Project_List.xlsx"), index=False)
