#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 12:10:04 2020

@author: kaitlinzareno
"""

import pandas as pd
import os
import re

#get csv files 
def get_affect_labels(path, suffix = ".csv"):
    filenames = os.listdir(path)
    csv_files = []
    for name in filenames:
        if name.endswith(suffix):
            csv_files.append(name)
    return csv_files

#generate data frames for each csv file in directory 
def to_df(affect_labels):
    affect_label_data= [] 
    names = []
    for label in affect_labels:   
        #get names of the annotators 
        r = re.findall('([A-Z][a-z]+)',label)
        names.append(r[0])
        #convert csv into data frame
        dataFrame = pd.read_csv("./p01_s1_al/"+label)
        #rename columns on affect and valence (parent and child) to include annotator's name
        dataFrame = dataFrame.rename(columns={"answer-timestamp" : "answer-timestamp ("+ r[0]+")", "Storyreading" : "Storyreading ("+ r[0]+")",
                                              "PARENT's valence": "PARENT's valence ("+ r[0]+")", "CHILD's valence": "CHILD's valence ("+ r[0]+")", 
                                              "PARENT's arousal" : "PARENT's arousal ("+ r[0]+")", "CHILD's arousal" : "CHILD's arousal ("+ r[0]+")"})
        #add all dataframes into an array -- each element is a dataset from a different annotator
        affect_label_data.append(dataFrame)
    
    #print(affect_label_data[0])
    return affect_label_data

def merge(affect_label_data):
    #merge takes in an array 
    new_df = pd.merge(affect_label_data[0], affect_label_data[1],  how='left', left_on=['clip-name','index'], right_on = ['clip-name','index'])    
    return new_df


if __name__ == '__main__':  
    
    #initialize clip_name and path
    clip_name = "p01_s1"
    path = "./p01_s1_al"
    
    #get csv files, transform to dataFrames and rename columns to include annotator's name
    affect_labels = get_affect_labels(path)
    data_array = to_df(affect_labels)
    
    #merge data of first two annotators
    merge1_and2 = merge(data_array)
    
    #create new list of dataFrames that contains the merged dataFrames and the last dataFrame in directory
    new_data_array = []
    new_data_array.append(merge1_and2)
    new_data_array.append(data_array[2])
    
    #merge all dataFrames
    merge_all = merge(new_data_array)
    #save merged dataFrames as csv
    merge_all.to_csv('./merged_affect_labels/'+clip_name+".csv")
    
