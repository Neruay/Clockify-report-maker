import re
from datetime import datetime
from types import NoneType

def fix_iso_format(time):
    fixed_time = time[:len(time)-1]
    return str(datetime.fromisoformat(fixed_time).date())

def convert_to_datetime(time):
    if type(time) == NoneType: # return zeroes if no time was spent on task
        return "00:00:00"

    hours = False
    minutes = False # initial flags of presense of different time values in unformatted time string
    seconds = False

    formatted_time = ""

    for char in range(2, len(time)): # loop to set flags
        if time[char] == "H":
            hours = True
        if time[char] == "M":
            minutes = True
        if time[char] == "S":
            seconds = True

    values = re.findall(r'\d+', time) # using regex to parse values
    values = ["%02d" % int(x) for x in values] # converting all single-digit time values to double-digit format
    
    current_value = 0
    if hours:                                   # if/else block to build formatted and easily readable time
        formatted_time += values[current_value] + ":"
        current_value += 1
    else:
        formatted_time += "00:"
    if minutes:
        formatted_time += values[current_value] + ":"
        current_value += 1
    else:
        formatted_time += "00:"
    if seconds:
        formatted_time += values[current_value]
    else:
        formatted_time += "00"
    
    formatted_time = str(datetime.strptime(formatted_time, "%H:%M:%S").time())
    return formatted_time

def grouper(item):
    return item[2] # sort by third element, task entry start date in this case

def add_time(time):
    total_time = datetime.strptime('00:00:00', '%H:%M:%S') 
    for index in range(len(time)):
        total_time -= datetime.strptime('00:00:00', '%H:%M:%S') # converting datetime to timedelta type to allow summing
        total_time += datetime.strptime(time[index], '%H:%M:%S')
    return total_time.time()