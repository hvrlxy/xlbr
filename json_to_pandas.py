import pandas as pd
import json
import io
from json2txttree import json2txttree

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
        self.root = Node("root")
        self.jsonFile = jsonFile
        self.jsonData = {'root': json.load(io.open(self.jsonFile, 'r', encoding='utf-8-sig'))}
        self.build()
        self.rows = []
        self.traverse_tree()
        self.remove_column_name()
        self.df = self.to_dataframe()

    def build(self):
        self.root = self.build_recursive(self.root, self.jsonData)
    
    def build_recursive(self, node: Node, parentDict: dict):
        key = node.text
        if isinstance(parentDict[key], dict):
            for text, value in parentDict[key].items():
                newNode = Node(text)
                node.addChild(newNode)
                self.build_recursive(newNode, parentDict[key])
        elif isinstance(parentDict[key], list):
            adict = parentDict[key][0]
            for text, value in adict.items():
                newNode = Node(text)
                node.addChild(newNode)
                self.build_recursive(newNode, adict)
        else:
            node.addChild(Node(parentDict[key]))
        return node

    def print(self):
        self.print_recursive(self.root, 0)

    def print_recursive(self, node: Node, level: int):
        print("\t" * level, (node.text))
        for child in node.children:
            self.print_recursive(child, level=level+1)

    def traverse_tree(self):
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
            row.remove("contextRef")
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
