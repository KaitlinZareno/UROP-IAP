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
        
        for path in self.paths:
            labels = self.set_labels(path)
            self.all_labels.append(labels)
        
            #create data frame for affect label
            affect_labels_dataframe = self.to_df(labels, path)
            self.all_affect_label_dataframes.append(affect_labels_dataframe)
            
            #working code
            merge1_and2 = self.merge(affect_labels_dataframe)
            new_arr = [merge1_and2]+affect_labels_dataframe[2:]
            merge_all = self.merge(new_arr)
            self.merged_all_df.append(merge_all)
            
#            al_df_list = affect_labels_dataframe[:]
#            for x in range(len(labels)-1):
#                al_df_list = al_df_list
#                new_df = self.merge(al_df_list)
#                #update list so that next element gets merged onto previous
#                al_df_list = [new_df] + affect_labels_dataframe[2:]
#            self.merged_all_df.append(pd.DataFrame(al_df_list))  

    #set csv files to merged_affect_labels obj
    def set_labels(self,path, suffix = ".csv"):
        filenames = os.listdir(path)
        csv_files = []
        for name in filenames:
            if name.endswith(suffix):
                csv_files.append(name)
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
    
#    #make merged csvs for all video files
#    def make_csv(self,dataframes,paths,names):
#        for x in range(len(paths)):
#            dataframe_to_convert = dataframes[x]
#            return (dataframe_to_convert.to_csv('./merged_affect_labels/'+names[x]+'tester!.csv'))
            

al = affect_labels()
all_labels = al.get_labels()
#print(all_labels)
al_df = al.get_df()
#print(al_df)
merged_df = al.get_merged_df()
#print(merged_df[0])
merged_df[0].to_csv('./merged_df_csv_merge_class_tester.csv')