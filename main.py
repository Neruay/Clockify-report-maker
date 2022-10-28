import requests as rq
import json
import sys

key = sys.argv[1]
project_name = sys.argv[2]
data = {'x-api-key': key}

entries = []

try:

    # first request to get workspace & user id's which are required to get projects list
    r = rq.get('https://api.clockify.me/api/v1/workspaces/', headers=data, params={})
    workspace_id = r.json()[0].get("id")
    user_id = r.json()[0].get("memberships")[0].get("userId")

    # second request to get project id"
    r = rq.get('https://api.clockify.me/api/v1/workspaces/{}/projects'.format(workspace_id), headers=data, params={"name":project_name})
    project_id = r.json()[0].get("id")
    print(json.dumps(r.json(), indent = 4))
    
    # third and final request to get task entries
    r = rq.get('https://api.clockify.me/api/v1/workspaces/{}/projects/{}/tasks'.format(workspace_id, project_id), headers=data, params={})
    
    # if any entries are found, they are added to the list of results
    if len(r.json()) > 0:
        for entry in r.json():
            entries.append((entry.get("name")))
    entries.reverse()

    for entry in entries:
        print(entry, end="\n")

except:
    print("Error")
