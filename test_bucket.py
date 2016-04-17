# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 18:16:02 2016

@author: huisu
"""
import numpy as np
class Bucket():
    def __init__(self,entities_b,ran):
        lat_min = min([entities_b[entity_b]["latitude"] for entity_b in entities_b if entities_b[entity_b]["latitude"]])
        lat_max = max([entities_b[entity_b]["latitude"] for entity_b in entities_b if entities_b[entity_b]["latitude"]])
        lon_min = min([entities_b[entity_b]["longitude"] for entity_b in entities_b if entities_b[entity_b]["longitude"]])
        lon_max = max([entities_b[entity_b]["longitude"] for entity_b in entities_b if entities_b[entity_b]["longitude"]])

        self.geo_dict = {}
        self.lon_list = np.arange(lon_min,lon_max,ran)
        self.lat_list = np.arange(lat_min,lat_max,ran)
        for lon in self.lon_list:
            for lat in self.lat_list:
                self.geo_dict[(lon,lat)]={}
    def binarysearch(self,item,alist):
        high,low = len(alist)-1,0
        while high >= low:
            mid = (high+low)/2
            if alist[mid] > item:
                high = mid - 1
            elif alist[mid] < item:
                low = mid + 1
            else:
                return [alist[mid]]
        if low >= len(alist):
            return [alist[high]]
        elif high < 0:
            return [alist[low]]
        else:
            return [alist[high],alist[low]]
        
    def addbucket(self,entity):
        lat = entity["latitude"]
        lon = entity["longitude"]
        latlist =  self.binarysearch(lat,self.lat_list)
        loglist = self.binarysearch(lon,self.lon_list)
        
        for i in latlist:
            for j in loglist:
                self.geo_dict[(j,i)][entity['id']]=entity
    def getbucket(self,lon,lat):
        latlist =  self.binarysearch(lat,self.lat_list)
        loglist = self.binarysearch(lon,self.lon_list)
        latkey = min([i for i in latlist],key=lambda p: abs(p-lat))
        lonkey = min([i for i in loglist],key=lambda p: abs(p-lon))
        return self.geo_dict[(lonkey,latkey)]
        
                
                    
            
            

            
            
        
        
    