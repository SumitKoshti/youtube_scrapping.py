#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Impoprting the libraries:

import requests
import pandas as pd
import time
import warnings
warnings.filterwarnings("ignore")

# Required instances:

API_KEY = input("Enter your api key: ")
CHANNEL_ID = input("Enter your channel id: ") 

# Constructing the url:

pageToken = ""
URL = "https://www.googleapis.com/youtube/v3/search?key="+API_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=10000"+pageToken

# Creating functions 
# Fetching views, like, favourite and comment count:

def get_video_details(video_Id):
    url_video_stats = "https://www.googleapis.com/youtube/v3/videos?id="+video_Id+"&part=statistics&key="+API_KEY
    response_video_stats = requests.get(url_video_stats).json()
    #response_video_stats

    view_count = response_video_stats["items"][0]["statistics"]["viewCount"]
    like_count = response_video_stats["items"][0]["statistics"]["likeCount"]
    favorite_Count = response_video_stats["items"][0]["statistics"]["favoriteCount"]
    comment_count = response_video_stats["items"][0]["statistics"]["commentCount"]
    
    return view_count, like_count, favorite_Count, comment_count
 
    
# Fetching id, title & update_date of video:

def get_videos(df):
    # make an api call
    pageToken = ""
    URL = "https://www.googleapis.com/youtube/v3/search?key="+API_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=10000"+pageToken

    response = requests.get(URL).json()
    time.sleep(1)

    for video in response["items"]:
        if video["id"]["kind"]=="youtube#video":   
            video_Id = video["id"]["videoId"]    
            video_title = video["snippet"]["title"]
            video_title = str(video_title).replace("&amp;","")
            upload_date = video["snippet"]["publishedAt"]
            upload_date = str(upload_date).split("T")[0]
        
            view_count, like_count, favorite_Count, comment_count= get_video_details(video_Id)
        
            # Save data in dataframe
            df = df.append({"video_Id":video_Id,"video_title":video_title, "upload_date":upload_date,
                        "view_count":view_count,"like_count":like_count,"favorite_Count":favorite_Count,
                        "comment_count":comment_count},ignore_index=True)
            
    return df


# In[4]:


# Building the dataframe

df = pd.DataFrame(columns=["video_Id", "video_title","upload_date","view_count","like_count","favorite_Count","comment_count"])
df = get_videos(df)
df


# In[ ]:




