import json
import os
import statistics

def get_data_from_file():
    json_list = []
    folder = "questionnaires"
    for filename in os.listdir(folder):
        with open(folder + "/" + filename) as json_file:
            data = json.load(json_file)
            if isinstance(data, list):
                json_list.extend(data)
            else:
                json_list.append(data)
    return json_list

data = get_data_from_file()
noted_diff_comments = []
noted_diff = []
noted_dots = []
influenced = []
cred_general = []
harder_read = []
for item in data:
    for key, value in item.items():
        if key == "notedGramDiffrenze":
            noted_diff_comments.append(value)
            noted_diff.append(int(value[0]))
        elif key == "participantsNotedDots":
            noted_dots.append(int(value))
        elif key == "itInfluenzedPartizipants":
            influenced.append(int(value))
        elif key == "credibleChangeGeneral":
            cred_general.append(int(value))
        elif key == "harderToRead":
            harder_read.append(int(value))
print("noticed any difference:", noted_diff.count(1), "/", len(data))
print("noticed dots: immediately:", noted_diff.count(1), "| yes, but no attention:", noted_diff.count(2), "| no:", noted_diff.count(3))
print("avg rating for influenced:", statistics.mean(influenced))
print("avg rating for influenced:", statistics.mean(influenced))
print("avg rating for general judgements:", statistics.mean(cred_general))
print("avg rating for harder to read:", statistics.mean(harder_read))