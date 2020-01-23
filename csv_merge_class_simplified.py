#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 13:56:53 2020

@author: kaitlinzareno
"""
import pandas as pd
import os 
import re


class affect_labels:    
    def __init__(self):
        #initialize paths to specific annotator, names of annotator, labels of csv files
        self.paths, self.names = self.set_paths_and_names()
        
        self.all_labels = []
        self.all_affect_label_dataframes = []
        self.merged_all_df = []

    #set csv files to merged_affect_labels obj
    def set_labels(self,path, suffix = ".csv"):
        filenames = os.listdir(path)
        csv_files = []
        for name in filenames:
            if name.endswith(suffix):
                csv_files.append(name)
        self.all_labels.append(csv_files)
        return csv_files
    
    #get csv files
    def get_labels(self):
        return self.all_labels   
     
    #get paths of subdirectories that start with letter p (indicates video clips) . ex) p01_s1
    def set_paths_and_names(self):
        path_list = []
        name_list = []
        for name in os.listdir("."):
            if name.startswith("p"):
                path_list.append(os.path.abspath(name))
                name_list.append(name)
        return path_list,name_list
        
    #get paths of annotators csv files
    def get_paths(self):
        return self.paths
    
    #get names of annotators
    def get_names(self):
        return self.names
    
    #generate dataframes for each csv file in subdirectory
    def to_df(self, labels, path):
        affect_label_data = []
        names = []
        for label in labels:   
            #get names of the annotators 
            r = re.findall('([A-Z][a-z]+)',label)
            names.append(r[0])
            #convert csv into data frame
            dataFrame = pd.read_csv(path+'/'+label)
            #rename columns on affect and valence (parent and child) to include annotator's name
            dataFrame = dataFrame.rename(columns={"answer-timestamp" : "answer-timestamp ("+ r[0]+")", "Storyreading" : "Storyreading ("+ r[0]+")",
                                                  "PARENT's valence": "PARENT's valence ("+ r[0]+")", "CHILD's valence": "CHILD's valence ("+ r[0]+")", 
                                                  "PARENT's arousal" : "PARENT's arousal ("+ r[0]+")", "CHILD's arousal" : "CHILD's arousal ("+ r[0]+")"})
            #add all dataframes into an array -- each element is a dataset from a different annotator
            affect_label_data.append(dataFrame)
        
        self.all_affect_label_dataframes.append(affect_label_data)  

        return affect_label_data
   
    #return dataframe of csv files of each annotator
    def get_df(self):
        return self.all_affect_label_dataframes
    
    #merge dataframes for all annotations in video subdirectories -- get a merged dataframe of annotations for every video    
    def merge(self,affect_labels_dataframe):
        new_df = pd.merge(affect_labels_dataframe[0], affect_labels_dataframe[1],  how='left', left_on=['clip-name','index'], right_on = ['clip-name','index'])
        return new_df
    
    def get_merged_df(self):
        return self.merged_all_df
    
    #make merged csvs for all video files
    def make_csv(self,dataframe,name):
        return (dataframe.to_csv('./merged_affect_labels/'+name+'tester!!.csv'))
            
if __name__ == '__main__':
    
    al = affect_labels()
    
    all_names = al.get_names()
    paths = al.get_paths()
    
    al_df = []
    all_labels = []
    merged_all_df = []
    
    for path in paths:
        labels = al.set_labels(path)
        all_labels.append(labels)
    
        #create data frame for affect label
        affect_labels_dataframe = al.to_df(labels, path)
        al_df.append(affect_labels_dataframe)
        
        #working code
        merge1_and2 = al.merge(affect_labels_dataframe)
        new_arr = [merge1_and2]+affect_labels_dataframe[2:]
        merge_all = al.merge(new_arr)
        merged_all_df.append(merge_all)
    
    for x in range(len(all_names)):
        dataframe = merged_all_df[x]
        name = all_names[x]
        to_csv = al.make_csv(dataframe,name)
        #print(to_csv)