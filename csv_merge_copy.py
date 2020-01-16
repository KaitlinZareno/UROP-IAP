#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 12:10:04 2020

@author: kaitlinzareno
"""

import pandas as pd
import os
import re


names = []
affect_label_data = []

affect_labels = os.listdir("./p01_s1_al")

#def get_name():
#    for label in affect_labels:
#        #get names of the annotators 
#        r = re.findall('([A-Z][a-z]+)',label)
#        names.append(r[0])

#generate data frames for each csv file in directory 
def to_df():
    for label in affect_labels:   
        #get names of the annotators 
        r = re.findall('([A-Z][a-z]+)',label)
        names.append(r[0])
        #convert csv into data frame
        dataFrame = pd.read_csv("./p01_s1_al/"+label)
        #rename columns on affect and valence (parent and child) to include annotator's name
        dataFrame = dataFrame.rename(columns={"PARENT's valence": "PARENT's valence ("+ r[0]+")", "CHILD's valence": "CHILD's valence ("+ r[0]+")", 
                                              "PARENT's arousal" : "PARENT's arousal ("+ r[0]+")", "CHILD's arousal " : "CHILD's arousal ("+ r[0]+")"})
        #add all dataframes into an array -- each element is a dataset from a different annotator
        affect_label_data.append(dataFrame)
    
    #print(affect_label_data[0])
    return affect_label_data

def merge(affect_label_data):
    #merge takes in an array 
    new_df = pd.merge(affect_label_data[0], affect_label_data[1],  how='left', left_on=['clip-name'], right_on = ['clip-name'])
    
    print(new_df)
#    while len(affect_label_data)>1:
#        affect_label_data = [new_df,affect_label_data[1:]]
#        merge(affect_label_data)
#    else:
#        return new_df 

if __name__ == '__main__':
    data_array = to_df()
    merge(data_array)
    
