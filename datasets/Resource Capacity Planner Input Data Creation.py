#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 18:31:59 2021

@author: rahulkoneru
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Pending Tasks

"""
Created on Sun Oct  3 01:42:04 2021

@author: rahulkoneru
"""


# Functions

# Spread Demand Across Calendar based on start and end date




import pandas as pd
import numpy as np
import os
import datetime as dt
from datetime import datetime
import time
import pathlib
def week_day(day_act_name):
    # Mon_num --> Index Number of Monday
    # day_act_name --> Name of the day
    mon_num = 6
    switcher = {
        "Monday": mon_num,
        "Tuesday": mon_num+1,
        "Wednesday": mon_num+2,
        "Thursday": mon_num+3,
        "Friday": mon_num+4,
        "Saturday": mon_num+5,
        "Sunday": mon_num+6
    }
    return switcher.get(day_act_name, "nothing")


# Obtain Column Index of start date and end date

def column_location(x, df):
    x = "Date_" + str(x)[:10]
    y = df.columns.get_loc(x)
    return y


# get relative data folder
PATH = pathlib.Path().parent
DATA_PATH = PATH.joinpath("../Resource Capacity Planner/datasets/").resolve()

script_fn = 'datasets/input_data_cleanup.py'
exec(open(script_fn).read())

# Import Required Files
#
#
#
resource_list = pd.read_excel(DATA_PATH.joinpath(
    ("01_Resource_List.xlsx")))  # This is a list of all resources
# This is a list of all client along with their enagagements
project_list = pd.read_excel(DATA_PATH.joinpath("02_Project_List.xlsx"))
# This is the list of all the action items requiring resource investment
task_list = pd.read_excel(DATA_PATH.joinpath("03_Task_List.xlsx"))
# This is the list from which share of resource allocated to a project is obtained
resource_capacity_share = pd.read_excel(DATA_PATH.joinpath("04_Resource_Capacity.xlsx"))
# This is the list of Holidays in a year
holiday_list = pd.read_excel(DATA_PATH.joinpath("05_Holiday_List.xlsx"))
#
# This is the lsit of all leaves applied for by employees
leave_list = pd.read_excel(DATA_PATH.joinpath("06_Leave_List.xlsx"))
#

# Resource List Cleanup
resource_list["Skill Set"] = resource_list["Skill Set"].str.replace(",", " , ").str.strip()

# Task List Cleanup
task_list["Engagement"] = np.where(
    task_list["Engagement"] != task_list["Engagement"], task_list['Client'], task_list['Engagement'])

# Project List Cleanup
project_list["Skills"] = project_list["Skills"].str.replace(",", " , ").str.strip()

resource_capacity_share["Client"] = np.where(
    resource_capacity_share["Client"] != resource_capacity_share["Client"], "Tredence Internal", resource_capacity_share["Client"])


#
#
# Initiate Variables for computational use
#
# Initial Setting for plan period start and end date
#plan_start_date = dt.datetime(2021, 9, 27)
#plan_end_date = dt.datetime(2021, 10, 25)
plan_start_date = min(pd.to_datetime(task_list['Task_Start_Date']))
plan_end_date = max(pd.to_datetime(task_list['Task_End_Date']))

# Holiday Clean up
holiday_list.columns = ["Holiday_Name", "Date", "Description"]
#
# Leave List clean up
leave_start = min(pd.to_datetime(leave_list['Leave_Start_Date']))
leave_end = max(pd.to_datetime(leave_list['Leave_End_Date']))

leaves = pd.date_range(start=leave_start, end=leave_end)
leaves = pd.DataFrame(leaves)
leaves.columns = ['Date']
leave_list['join'] = 1
leaves['join'] = 1
leaves_planned = pd.merge(leave_list, leaves, how='left', on='join')

leaves_planned = leaves_planned.loc[((leaves_planned["Leave_Start_Date"] <= leaves_planned["Date"]) &
                                     (leaves_planned["Leave_End_Date"] >= leaves_planned["Date"])), :]

# Variabale for easy adjustment later
capacity_per_day = 8
capacity_weekend = 0
#
#
#
#
#
#
#
# Resource Capacity
resource_capacity = resource_capacity_share
resource_capacity["Day_Capacity"] = resource_capacity["Capacity_To_Engagement"] * capacity_per_day
#
#
#
# Data Manipulation for the tool
#
task_list["Plan_Start_Date"] = plan_start_date
task_list["Plan_End_Date"] = plan_end_date


task_list["Adj_Start_Date"] = np.where(
    task_list["Task_Start_Date"] < plan_start_date, task_list["Plan_Start_Date"], task_list["Task_Start_Date"])
task_list["Adj_End_Date"] = np.where(
    task_list["Task_End_Date"] > plan_end_date, task_list["Plan_End_Date"], task_list["Task_End_Date"])

task_list["Adj_Start_Date"] = pd.to_datetime(task_list["Adj_Start_Date"])
task_list["Adj_End_Date"] = pd.to_datetime(task_list["Adj_End_Date"])

dates_in_plan = pd.date_range(start=plan_start_date, end=plan_end_date)
dates_in_plan = pd.DataFrame(dates_in_plan)
dates_in_plan.columns = ["Date"]
dates_in_plan["Day_Name"] = dates_in_plan["Date"].dt.day_name()
dates_in_plan["join"] = 1

task_list["join"] = 1

test = pd.merge(task_list, dates_in_plan, how='left', on='join')

# Obtain demand from the task list and plan start date and end date

test['Plan_Period'] = np.where(((test["Task_Start_Date"] <= test["Date"]) &
                                (test["Task_End_Date"] >= test["Date"])), "In Period", "Out Period")
# demand = test.loc[((test["Task_Start_Date"] <= test["Date"]) &
#                     (test["Task_End_Date"] >= test["Date"])), :]
demand = test
del(test)

leaves_planned = leaves_planned[['Emp_ID', 'Leave_Start_Date', 'Leave_End_Date', 'Date']]

demand = pd.merge(demand, leaves_planned, how='left', on=['Emp_ID', 'Date'])

demand.drop("join", axis=1, inplace=True)
demand["Day_Name"] = demand["Day_Name"].str[0:3]

demand_list = task_list.melt(id_vars=["Client", "Engagement", "Task", "Emp_ID"], value_vars=[
                             "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
demand_list.columns = ['Client', 'Engagement', 'Task', 'Emp_ID', 'Day_Name', 'Day_Demand']

demand = pd.merge(demand, demand_list, how='left', on=[
                  'Client', 'Engagement', 'Task', 'Emp_ID', 'Day_Name'])

# Include Holidays if any in plan period in the Demand
holiday_list.columns = ['Holiday_Name', 'Date', 'Description']
demand = pd.merge(demand, holiday_list[["Holiday_Name", "Date"]], how='left', on="Date")
demand["Holiday_Name"] = demand["Holiday_Name"].fillna("Working Day")
demand['Day_Demand'] = demand['Day_Demand'].fillna(0)
demand['Day_Demand'] = np.where(demand['Plan_Period'] == "In Period", demand['Day_Demand'], 0)
# Get Demand in holiday
demand["Holiday_Demand"] = np.where(
    demand["Holiday_Name"] == "Working Day", 0, demand["Day_Demand"])
demand["Day_Demand"] = np.where(demand["Holiday_Name"] == "Working Day", demand["Day_Demand"], 0)

# Include leaves if any in the plan period
demand['Leave_Start_Date'] = demand['Leave_Start_Date'].fillna(dt.datetime(2010, 1, 1))
demand['Leave_End_Date'] = demand['Leave_End_Date'].fillna(dt.datetime(2010, 1, 2))
demand['Leave_Status'] = np.where((demand['Leave_Start_Date'] <= demand['Date']) & (
    demand['Leave_End_Date'] >= demand['Date']), "Leave", "Not on leave")

demand = pd.merge(
    demand, resource_list[['Emp_ID', 'Backup Resource ID', "Exit Date"]], how='left', on='Emp_ID')
# Aggregate demand from Emp_ID, Task, Enagagement level to Emp_ID, Engagement Level
demand_aggreagted = demand.groupby(["Client", "Engagement", "Emp_ID", "Backup Resource ID", "Date", "Day_Name", "Leave_Status"]).agg({
    'Day_Demand': 'sum', 'Holiday_Demand': 'sum'}, as_index=False)

demand_aggreagted.reset_index(inplace=True)


demand_aggreagted = pd.merge(demand_aggreagted, resource_capacity,
                             how='left', on=["Client", "Engagement", "Emp_ID"])

demand_aggreagted["Day_Capacity"] = np.where(((demand_aggreagted['Day_Name'] == "Sat") | (
    demand_aggreagted["Day_Name"] == "Sun")), capacity_weekend, demand_aggreagted["Day_Capacity"])


demand_aggreagted = pd.merge(demand_aggreagted,
                             resource_list[["Emp_ID", "Exit Date"]],
                             how='left',
                             right_on='Emp_ID',
                             left_on="Emp_ID")


demand_aggreagted['Day_Capacity'] = np.where(
    demand_aggreagted["Exit Date"] >= demand_aggreagted['Date'], 0, demand_aggreagted["Day_Capacity"])


demand_aggreagted["Excess_Capacity"] = demand_aggreagted["Day_Capacity"] - \
    demand_aggreagted["Day_Demand"]

demand_aggreagted['Leave_Capacity'] = np.where(
    demand_aggreagted["Leave_Status"] == "Leave", - demand_aggreagted["Day_Capacity"], 0)

# Tag Each enagement, Emp_ID combination as Over/Under/Fully Utilized
demand_aggreagted["Utilization_Status"] = np.where(demand_aggreagted["Excess_Capacity"] > 0, "Under Utilized", np.where(
    demand_aggreagted["Excess_Capacity"] < 0, "Over Utilized", "Fully Utilized"))

# Obtain totals for each Emp_ID for the demand and capacity
demand_agg_total = demand_aggreagted.groupby(["Client", "Engagement", "Emp_ID", "Backup Resource ID", "Capacity_To_Engagement"]).agg({
    "Day_Demand": 'sum', "Day_Capacity": 'sum', "Holiday_Demand": 'sum', "Leave_Capacity": 'sum', "Excess_Capacity": 'sum'})
demand_agg_total.reset_index(inplace=True)
demand_agg_total["Day_Name"] = "Total"
demand_agg_total["Date"] = plan_end_date
demand_agg_total["Utilization_Status"] = np.where(demand_agg_total['Excess_Capacity'] > 0, "Under Utilized", np.where(
    demand_agg_total['Excess_Capacity'] < 0, "Over Utilized", "Fully Utilized"))
demand_agg_total = pd.concat([demand_aggreagted, demand_agg_total], ignore_index=True)
demand_agg_total['Update_Date_Time'] = datetime.now()
demand_agg_total = demand_agg_total.fillna(0)

# Export Set 1
# This is the main data that powers the charts in the following view,
# 1) Data Inputs
# 2) Demand Vs Capacity
# 3) Status by Project

resource_backup_actual = demand_agg_total[demand_agg_total['Day_Name'] != "Total"]
resource_backup_actual = resource_backup_actual[["Emp_ID",
                                                 "Date",
                                                 'Excess_Capacity',
                                                 "Day_Demand",
                                                 "Day_Capacity"
                                                 ]]

resource_backup_actual = resource_backup_actual.groupby(["Emp_ID", "Date"]).agg(
    {"Day_Demand": 'sum', "Day_Capacity": 'sum', "Excess_Capacity": 'sum'})
resource_backup_actual.reset_index(drop=False, inplace=True)
resource_backup_actual.drop_duplicates()
resource_backup_actual.columns = ["Backup_ID",
                                  "Date",
                                  "Backup_Excess_Capacity",
                                  "Backup_Day_Demand",
                                  "Backup_Day_Capacity"
                                  ]

resource_backup_actual.reset_index(drop=True, inplace=True)

dtest = pd.merge(
    demand_agg_total[demand_agg_total['Day_Name'] != "Total"],
    resource_backup_actual,
    how='left',
    left_on=["Backup Resource ID", "Date"],
    right_on=["Backup_ID", "Date"])

dtest.to_excel(DATA_PATH.joinpath(
    "Demand_Capacity_Input_with_Resigns.xlsx"), index=False)

demand_agg_total.to_excel(DATA_PATH.joinpath(
    "Resource_Capacity_Planner_Deman_Aggregate_Input.xlsx"), index=False)

# demand_agg_total.columns
