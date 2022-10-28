import requests as rq
import sys
from utils import convert_to_datetime, fix_iso_format, grouper, add_time
from itertools import groupby

key = sys.argv[1]
project_name = sys.argv[2]
data = {'x-api-key': key}

task_entries = []
time_entries = []

try:

    # first request to get workspace & user id's which are required to get projects list
    r = rq.get('https://api.clockify.me/api/v1/workspaces/',
               headers=data, params={})
    workspace_id = r.json()[0].get("id")
    user_id = r.json()[0].get("memberships")[0].get("userId")

    # second request to get project id
    r = rq.get('https://api.clockify.me/api/v1/workspaces/{}/projects'.format(
        workspace_id), headers=data, params={"name": project_name})
    project_id = r.json()[0].get("id")

    # third request to get task entries
    r = rq.get('https://api.clockify.me/api/v1/workspaces/{}/projects/{}/tasks'.format(
        workspace_id, project_id), headers=data, params={})

    # if any entries are found, they are added to the list of results
    if len(r.json()) > 0:
        for entry in r.json():
            task_entries.append((entry.get("name"), convert_to_datetime(
                entry.get("duration")), entry.get("status")))
    task_entries.reverse()

    # fourth request to get time entries to sort them by day
    r = rq.get('https://api.clockify.me/api/v1/workspaces/{}/user/{}/time-entries'.format(
        workspace_id, user_id), headers=data, params={"hydrated": True, "project": project_id})
    if len(r.json()) > 0:
        for entry in r.json():
            time_entries.append((entry.get("task").get("name"), convert_to_datetime(entry.get(
                "timeInterval").get("duration")), fix_iso_format(entry.get("timeInterval").get("start"))))

    time_entries = sorted(time_entries, key=grouper)  # sort entries by date

    group_list = []  # list which contains all pairs [date - time entries[]]

    # grouping data and saving pairs in group_list
    for key, group_items in groupby((time_entries), key=grouper):
        group_list.append([key, list(group_items)])

    # combine multiple time entries on the same task inside each group
    for group in range(len(group_list)):
        sorted_time_entries = {}
        for name, duration, start in group_list[group][1]:
            sorted_time_entries.setdefault((name, start), []).append(duration)
        sorted_time_entries = [(name, str(add_time(vals)), duration) for (
            name, duration), vals in sorted_time_entries.items()]
        group_list[group][1] = sorted_time_entries

    print("Grouped by date")  # building "Grouped by date" report
    for group in range(len(group_list)):
        print("\nDate -", group_list[group][0], end="\n\n")
        print("Task | Duration\n")
        for time_entry in range(len(group_list[group][1])):
            print(group_list[group][1][time_entry][0], "-",
                  group_list[group][1][time_entry][1], end="\n")

    # building "All tasks, time entries and task status" report
    print("\nAll tasks, time entries and task status\n")
    for entry in task_entries:
        print("{} {} - {}".format(entry[0], entry[1], entry[2]), end="\n")

except:
    print("Error")
