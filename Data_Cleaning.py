#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import operator
import sys


def get_str_real_type(item_):
    if isinstance(item_,str):
        if item_.upper()=='NAN':
            return float
        try:
            t=eval(f"type({item_})") 
            return t if t !=type else str
        except Exception as e:
            return str
    return type(item_)

def most_frequent_type(df, col_name):
    dic_types = {}
    for item_ in df[col_name]:
        item_type = get_str_real_type(item_)
        if item_type in dic_types:
            dic_types[item_type]+=1
        else:
            dic_types[item_type] = 1

    return max(dic_types.items(), key=operator.itemgetter(1))[0]

def mean_for_float(feature,data):
    temp_sum = 0
    temp_amount = 0
    for item_ in data[feature]:
        if type(item_) == float and not item_ is np.nan:
            temp_sum += item_
            temp_amount +=1
    return 0 if temp_amount==0 else temp_sum/temp_amount

def standard_lowerAndStrip(df,freq_types_dict):
    for feature in df.columns:
        if freq_types_dict[feature]==str:
            df[feature]=df[feature].str.lower().str.strip()
        if freq_types_dict[feature] in [float ,bool, int]:
            
            for item_ in df[feature]:
                if type(item_)==str:    
                    df[feature]=df[feature].replace(item_, item_.lower().strip())
        df[feature].apply(lambda val: np.nan if isinstance(val,str) 
                                and val.upper() in ['NAN','NULL','NA'] else val)

        
def drop_rows(data):
    if data.shape[0]>50:
        data.dropna(axis=0, thresh=0.2*data.shape[1],inplace=True)    

        
#def is_binary_col(feature,data):
#    value_dic = {}
#    for item_ in data[feature]:
#        if not item_ is np.nan:
#            value_dic[item_]= 1
#    return len(value_dic) in [1,2]  
    
    
def missing_values(data,freq_types_dict):
    for feature in data:
        NAN_percentage = data[feature].isna().sum()/data.shape[0]
        if NAN_percentage>0.8:
            data.dropna(axis=1, thresh=0.2*data.shape[0],inplace=True)
        #if is_binary_col(feature, data):
            
        if freq_types_dict[feature] == float:
            if NAN_percentage<0.1:
                mean_ = mean_for_float(feature,data)
                data[feature].fillna(value=mean_, inplace=True)
    drop_rows(data)
             
def correlation(data):      
    correlation = data.corr().abs()
    upper_tri = correlation.where(np.triu(np.ones(correlation.shape), k=1).astype(np.bool))
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.95)]
    data.drop(to_drop, axis=1, inplace=True)    



def DataCleaner(df):
    file_name = df.strip('csv')+'_cleaned.csv'
    data = pd.read_csv(df)
    max_type_dic = {}
    for feature in data:
        max_type_dic[feature] = most_frequent_type(data, feature)
    standard_lowerAndStrip(data,max_type_dic)
    data.drop_duplicates(inplace=True, ignore_index=True)
    missing_values(data,max_type_dic)
    data.to_csv(file_name,index=False,encoding='utf-8-sig')
    correlation(data)
#df_types=pd.DataFrame(max_type_dic.items())
 #   df_types.columns = ['Feature', 'Type']



file=sys.argv[1]
DataCleaner(file)







