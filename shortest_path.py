#!/usr/bin/python3

# this script implements bidirectional breadth-first search for the citation network

import sys

from datetime import datetime
from collections import deque

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    input_file = "interactions_tuplets.txt"

print(input_file)


input_network = "pmid_citations.txt"

output_file = input_file + "_output.txt"

input_date_file = "pmid_date.txt"

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

print("Current Time:", current_time)

print("Reading publication dates...")

pmid_dates = {}

f_in = open(input_date_file, "r")

for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    pmid = int(data[0])
    date = data[1]
    pmid_dates[pmid] = int(date)

print("Reading network...")

f_in = open(input_network, "r")

counter = 0
graph = {}
for line in f_in:
    line = line[:-1]
    counter+=1
    if float(counter) / 100000 == int(float(counter) / 100000):
        print("Read " + str(counter) + " lines")
    edge = line.split("\t")
    node1 = int(edge[0])
    node2 = int(edge[1])
    if node1 in pmid_dates.keys():
        if node1 in graph.keys():
            graph[node1].append(node2)
        else:
            graph[node1] = [node2]
    if node2 in pmid_dates.keys():
        if node2 in graph.keys():
            graph[node2].append(node1)
        else:
            graph[node2] = [node1]

print("Computing shortest paths...")

f_in = open(input_file, "r")
f_out = open(output_file, "w")

# since it is birectional BFS, two queues are created and explored
counter = 0
for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    counter+=1
    print(data)
    start_node = int(data[2])
    end_node = int(data[6])
    reference_date = int(data[7])

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time:", current_time)

    print("Finding shortest path...")

    q1 = deque()
    q2 = deque()
    
    # initiate queues
    q1.append(start_node)
    q2.append(end_node)

    distance1 = {}
    distance2 = {}
    visited1 = set()
    visited2 = set()
    previous_node1 = {}
    previous_node2 = {}
    distance1[start_node] = 0
    distance2[end_node] = 0
    visited1.add(start_node)
    visited2.add(end_node)
    node1 = start_node
    node2 = end_node 
    shortest_path_found = False
    final_distance = -1
    current_layer1 = 0
    current_layer2 = 0
    while q1 and q2 and not shortest_path_found:
        # decide which queue to read first
        if len(q1) <= len(q2):
            next_node1 = q1[0]
            # once a queue is selected the entire layer needs to be read
            # otherwise the outcome could be suboptimal
            while distance1[next_node1] <= current_layer1 and q1:
                node1 = q1.popleft()
                if node1 in graph.keys():
                    # read nodes connected to the node of reference
                    neighboring_nodes = graph[node1]
                    reference_distance = distance1[node1]
                    new_reference_distance = reference_distance + 1
                    for neighboring_node in neighboring_nodes:
                        # add new nodes to the queue
                        if neighboring_node not in visited1:
                            q1.append(neighboring_node)
                            distance1[neighboring_node] = new_reference_distance
                            visited1.add(neighboring_node)
                            #######
                            #previous_node1[neighboring_node] = node1
                            #######
                            # if the new node overlaps with the other queue then stop search
                            if neighboring_node in visited2:
                                shortest_path_found = True
                                final_distance = distance1[neighboring_node] + distance2[neighboring_node]
                                intersecting_node = neighboring_node
                if q1:
                    next_node1 = q1[0]
            current_layer1 += 1
        else:
            # same thing but from the other end
            next_node2 = q2[0]
            while distance2[next_node2] <= current_layer2 and q2:
                node2 = q2.popleft()
                if node2 in graph.keys():
                    neighboring_nodes = graph[node2]
                    reference_distance = distance2[node2]
                    new_reference_distance = reference_distance + 1
                    for neighboring_node in neighboring_nodes:
                        if neighboring_node not in visited2:
                            q2.append(neighboring_node)
                            distance2[neighboring_node] = new_reference_distance
                            visited2.add(neighboring_node)
                            #######
                            #previous_node2[neighboring_node] = node2
                            #######
                            if neighboring_node in visited1: 
                                shortest_path_found = True
                                final_distance = distance1[neighboring_node] + distance2[neighboring_node]
                                intersecting_node = neighboring_node
                if q2:
                    next_node2 = q2[0]
            current_layer2 += 1

    if shortest_path_found == True:
        print("Distance: " + str(final_distance))
        ##############
        #next_node = intersecting_node
        #shortest_path1 = [intersecting_node]
        #while next_node != start_node:
        #    next_node = previous_node1[next_node]
        #    shortest_path1.append(next_node)
        #print("Shortest path from start: " + str(shortest_path1))
        #next_node = intersecting_node
        #shortest_path2 = [intersecting_node]
        #while next_node != end_node:
        #    next_node = previous_node2[next_node]
        #    shortest_path2.append(next_node)
        #print("Shortest path from end: " + str(shortest_path2))
        ##############
        f_out.write(line + "\t" + str(final_distance) + "\n")
    else:
        print("Shortest path not found.")
        f_out.write(line + "\t" + "-1" + "\n")

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time:", current_time)
