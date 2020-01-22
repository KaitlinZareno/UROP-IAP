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
        self.labels = self.set_labels(self.get_paths())
        
        #create data frame for affect label
        self.affect_labels_dataframe = self.to_df(self.get_labels(), self.get_paths())
        
        #merged data frame
        self.merged_data = self.merge(self.get_df(),self.get_paths())

    #set csv files to merged_affect_labels obj
    def set_labels(self,paths, suffix = ".csv"):
        for path in paths:
            filenames = os.listdir(path)
            csv_files = []
            for name in filenames:
                if name.endswith(suffix):
                    csv_files.append(name)
        return csv_files
    
    #get csv files
    def get_labels(self):
        return self.labels   
     
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
    def to_df(self, labels, paths):
        all_affect_label_data= [] 
        affect_label_data = []
        names = []
        for path in paths:
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
            all_affect_label_data.append(affect_label_data)
            
        return all_affect_label_data
    
    #return dataframe of csv files of each annotator
    def get_df(self):
        return self.affect_labels_dataframe
    
    #merge dataframes for all annotations in video subdirectories -- get a merged dataframe of annotations for every video
    
    #NOT MERGING PROPERLY -- GIVES WACK VALUES
    def merge(self,affect_label_data, paths):
        all_affect_label_lists = []
        for path in paths:
            #copy list of dataframes to be able to manipulate list
            end = int(len(affect_label_data)/2)
            affect_label_list = affect_label_data[:end]
            #each annotator is getting listed twice, so to merge properly need only 1 instance of annotation
            #get only 1 annotation csv file per annotator
            len_unique_annotators = int(len(affect_label_data)/2)
            #merge first two items in the list 
            for x in range(len_unique_annotators-1):          
                 new_df = pd.merge(affect_label_list[0], affect_label_list[1],  how='left', left_on=['clip-name','index'], right_on = ['clip-name','index'])
                 #update list so that next element gets merged onto previous
                 affect_label_list = [new_df] + affect_label_list[2:]
                 
            all_affect_label_lists.append(pd.DataFrame(affect_label_list))
            
        return all_affect_label_lists
    
    #return merged dataframe
    def get_merged_dataframes(self):
        return self.merged_data
    
    #make merged csvs for all video files
    def make_csv(self,dataframes,paths,names):
        for x in range(len(paths)):
            dataframe_to_convert = dataframes[x]
            return (dataframe_to_convert.to_csv('./merged_affect_labels/'+names[x]+'tester!.csv'))
            
            
mal = affect_labels()
paths = mal.get_paths()
print(len(paths))
names = mal.get_names()
print(names)
labels = mal.get_labels()
affect_label_data = mal.get_df()
merged = mal.get_merged_dataframes()
print(type(merged[0]))

csv = mal.make_csv(merged,paths,names)


    