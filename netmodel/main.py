import csv
import pandas as pd
import numpy as np
import io

import matplotlib.pyplot as plt
import networkx as nx
from functools import reduce

class Activity:
    def __init__(self, id, hours, predecessors, needs, complete_predecessorcs=[]):
        self.id = id
        self.hours = hours
        self.predecessors = predecessors.split(',') if predecessors != '-' else []
        self.needs = needs
        self.complete_predecessorcs = complete_predecessorcs

    def __str__(self):
        return f'Work({self.id}, {self.hours}, {self.predecessors}, {self.needs}, complete pred {self.complete_predecessorcs})'


class Logic:
    def __init__(self, activities):
        self.activities = activities

    @staticmethod
    def has(activities, uniquepredecessor):
        for activity in activities:
            if activity.id not in uniquepredecessor:
                return activity
        return False


    @staticmethod
    def define_unique(accumulator,activity):
        if activity.predecessors:
            for predecessor in activity.predecessors:
                accumulator.add(predecessor)
        return accumulator

    def get_root(self):
        uniquepredecessor = reduce(Logic.define_unique, self.activities, set())
        root = Logic.has(self.activities, uniquepredecessor)
        return root
    
    @staticmethod
    def retrieve_predecessors(root, activities):
        root.complete_predecessorcs = set()
        if len(root.predecessors) == 0:
            return root
        for id in root.predecessors:
            predecessor = Logic.retrieve_predecessors(next(filter((lambda activity: activity.id == id), activities)), activities)
            for cp in predecessor.complete_predecessorcs:
                root.complete_predecessorcs.add(cp)
            root.complete_predecessorcs.add(id)
        return root

if __name__ == '__main__':
    work_list = []

    with open('./tests/1.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)
        for id, hours, predecessors, needs in reader:
            work_list.append(Activity(id, hours, predecessors, needs))

    id_df = [work.id for work in work_list]
    predecessors_df = [work.predecessors for work in work_list]

    Logic = Logic(work_list)
    root = Logic.get_root()
    g = nx.DiGraph()

    Logic.retrieve_predecessors(root, work_list)
    for work in work_list:
        Logic.retrieve_predecessors(work, work_list)

    for work in work_list:
        print(work)
        g.add_node(work.id, work.complete_predecessorcs)
        
    print(g)

    

    