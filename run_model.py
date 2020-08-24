#!/usr/bin/python3

# this script computes the ABC model statistics based on all combinatorially created pairs of facts

import pandas as pd
import datetime


input_file = "interactions_tuplets.txt"
output_file = "discoveries_by_distance.csv"

final_year = 2020
final_month = 1
final_day = 1

start_year_min = 0
start_year_max = 2020

def number_to_datetime(time_value):
    if time_value == 999999:
        time_value = str(final_year) + str(final_month).zfill(2) + str(final_day).zfill(2)
    time_number = float(time_value)
    year = int(round(time_number/10000))
    month = int(round((time_number - 10000*year)/100))
    day = int(time_number - year*10000 - month*100)
    time_datetime = datetime.datetime(year, month, day)
    return time_datetime

print("Reading input file...")
tuplet_data = pd.read_csv(input_file, index_col=False, sep="\t", names=["entity1", "id1", "pmid1", "date1","entity2", "id2", "pmid2", "date2","entity3", "id3", "pmid3", "date3", "distance"])
print("File read.")

# filter data if necessary to investigate time windows
tuplet_data = tuplet_data[tuplet_data["date2"] > start_year_min * 10000]
tuplet_data = tuplet_data[tuplet_data["date2"] < start_year_max * 10000]

# transform dates written as numbers to datetime objects
for column_name in ["date1", "date2", "date3"]:
    tuplet_data[column_name] = tuplet_data[column_name].apply(lambda x: number_to_datetime(x))

print("Max AC date: " + str(tuplet_data["date3"].max()))
print("Max BC date: " + str(tuplet_data["date2"].max()))

# compute time lapse between BC and AC
tuplet_data["diff23"] = tuplet_data["date3"] - tuplet_data["date2"]
tuplet_data["diff23"] = tuplet_data["diff23"].dt.days

# compute time covered by the event up to the limit date (January 1, 2020)
tuplet_data["time_window"] = datetime.datetime(final_year, final_month, final_day) - tuplet_data["date2"]
tuplet_data["time_window"] = tuplet_data["time_window"].dt.days

# eliminate some invalid entries
tuplet_data = tuplet_data[tuplet_data["diff23"] > 0]

tuplet_data["pmid3"] = tuplet_data["pmid3"].astype(str)



counts_data = []

step = 10

# compute the model output at 5 years without considering citation distance (i.e. the baseline)
print("Average at 5 years...")
reference_time = 1826
count_non_triplet = (tuplet_data["pmid3"][tuplet_data["diff23"] > reference_time] != "XXXXXXXX").sum() + (tuplet_data["pmid3"][tuplet_data["time_window"] >= reference_time] == "XXXXXXXX").sum()
count_triplet = (tuplet_data["pmid3"][tuplet_data["diff23"] <= reference_time] != "XXXXXXXX").sum()
counts_data.append(float(count_triplet) / (float(count_triplet) + float(count_non_triplet)))

print(counts_data)

counts_data = []

# compute the model output (discoveries per citation distance) at 5 years after the BC event
print("Values at 5 years...")
reference_time = 1826
for distance in range(1,8):
    tuplet_data1 = tuplet_data[tuplet_data["distance"] == distance].copy()
    count_non_triplet = (tuplet_data1["pmid3"][tuplet_data1["diff23"] > reference_time] != "XXXXXXXX").sum() + (tuplet_data1["pmid3"][tuplet_data1["time_window"] >= reference_time] == "XXXXXXXX").sum()
    count_triplet = (tuplet_data1["pmid3"][tuplet_data1["diff23"] <= reference_time] != "XXXXXXXX").sum()
    counts_data.append(float(count_triplet) / (float(count_triplet) + float(count_non_triplet)))


print(counts_data)

counts_data = pd.DataFrame()

# compute the model output in steps of 10 days and up to 2000 days
print("Stepwise sample...")
for distance in range(1,8):

    print("Distance=" + str(distance))
    tuplet_data1 = tuplet_data[tuplet_data["distance"] == distance].copy()

    for i in range(10, 2001, step):
        count_non_triplet = (tuplet_data1["pmid3"][tuplet_data1["diff23"] > i] != "XXXXXXXX").sum() + (tuplet_data1["pmid3"][tuplet_data1["time_window"] >= i] == "XXXXXXXX").sum()
        count_triplet = (tuplet_data1["pmid3"][tuplet_data1["diff23"] <= i] != "XXXXXXXX").sum()
        counts_data.loc[i, "distance " + str(distance)] = float(count_triplet) / (float(count_triplet) + float(count_non_triplet))

counts_data.to_csv(output_file, sep=",")

