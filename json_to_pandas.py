import pandas as pd
import json
import io
from json2txttree import json2txttree

def join_duplicate_keys(ordered_pairs):
    # this function is used to solve the problem of duplicate keys in json
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            if type(d[k]) == list:
                d[k].append(v)
            else:
                newlist = []
                newlist.append(d[k])
                newlist.append(v)
                d[k] = newlist
        else:
            d[k] = v
    return d

class Node:
    def __init__(self, text):
        self.text = text
        self.children = []

    def addChild(self, node):
        self.children.append(node)

    def __str__(self) -> str:
        return self.text

class JSONtree(object):
    def __init__(self, jsonFile):
        # initialize the root of the json tree
        self.root = Node("root")
        # read the json file
        self.jsonFile = jsonFile
        with open(self.jsonFile, 'r') as file:
            self.jsonData = file.read().replace('\n', '')
        # convert the json to python dictionary
        self.jsonData = json.loads(self.jsonData, object_pairs_hook=join_duplicate_keys)
        self.jsonData = {'root': self.jsonData}
        # build the tree
        self.build()
        self.rows = []
        # traverse the tree and get the rows
        self.traverse_tree()
        # remove the column names "@contextRef" and "#text"
        self.remove_column_name()
        # convert the rows to dataframe
        self.df = self.to_dataframe()

    def build(self):
        # build the tree recursively
        self.root = self.build_recursive(self.root, self.jsonData)
    
    def build_recursive(self, node: Node, parentDict: dict):
        # get the text of the node
        key = node.text
        if isinstance(parentDict[key], dict):
            # if the node is a dictionary, then create a new node for each key in the dictionary
            for text, value in parentDict[key].items():
                newNode = Node(text)
                node.addChild(newNode)
                self.build_recursive(newNode, parentDict[key])
        elif isinstance(parentDict[key], list):
            # if the node is a list, then create a new node for each item in the list
            for item in parentDict[key]:
                for text, value in item.items():
                    newNode = Node(text)
                    node.addChild(newNode)
                    self.build_recursive(newNode, item)
        else:
            # if the node is a string, then create a new node for the string
            node.addChild(Node(parentDict[key]))
        return node

    def print(self):
        # print the tree
        self.print_recursive(self.root, 0)

    def print_recursive(self, node: Node, level: int):
        print("\t" * level, (node.text))
        for child in node.children:
            self.print_recursive(child, level=level+1)

    def traverse_tree(self):
        # traverse the tree and get the rows
        self.traverse_tree_recursive(self.root, [])
        new_rows = []
        for i in range(0, len(self.rows), 2):
            contextRef_row = self.rows[i]
            text_row = self.rows[i+1]
            contextRef_row.append(text_row[-2])
            contextRef_row.append(text_row[-1])
            new_rows.append(contextRef_row)
        self.rows = new_rows
        # print(self.rows)

    def traverse_tree_recursive(self, node: Node, current_lst):
        if len(node.children) == 0:
            current_lst.append(node.text)
            self.rows.append(current_lst)
        else:
            for child in node.children:
                next_lst = current_lst + [node.text]
                self.traverse_tree_recursive(child, next_lst)

    def remove_column_name(self):
        for row in self.rows:
            row.remove("@contextRef")
            row.remove("#text")
            row.remove("root")

    def to_dataframe(self):
        max_row_length = max([len(row) for row in self.rows])
        # print(max_row_length)
        for row in self.rows:
            while len(row) < max_row_length:
                row.insert(-2, "")

        df = pd.DataFrame(self.rows, columns=['']*(max_row_length-2) + ["contextRef", "#text"])

        return df

    def to_csv(self, filename):
        self.df.to_csv(filename, index=True)

    def to_excel(self, filename):
        self.df.to_excel(filename, index=True)
