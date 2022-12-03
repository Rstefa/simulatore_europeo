#!/usr/bin/env python
# coding: utf-8

# In[797]:


from math import *
import matplotlib.pyplot as plt
import numpy as np
import os, glob
import imageio
from matplotlib.widgets import Slider,Button
import os
import random
import pandas as pd
df=pd.read_csv("fifa_ranking-2022-10-06.csv")
df=df[df['rank_date']=='2022-10-06']
df=df[['country_full','total_points','confederation']].reset_index()
df['total_points']=df['total_points']/100/2
df['total_points']=df.loc[:,'total_points'].apply('exp')
#df['total_points']=df.loc[:,'total_points']*df.loc[:,'total_points']*df.loc[:,'total_points']
#df['total_points']=pow(10,df['total_points'])
dfUEFA=df[df['confederation']=='UEFA']
dfUEFA['total_points']=dfUEFA['total_points']/dfUEFA.loc[:,'total_points'].sum()
dfUEFA["girone"] = np.nan
dfUEFA=dfUEFA.sort_values('total_points').reset_index()


# In[798]:


randomlist=np.random.choice(dfUEFA.loc[:,'country_full'].tolist(),size=13,replace=False,p=dfUEFA.loc[:,'total_points'].tolist())


# In[799]:


i=0
j=0
while i<len(dfUEFA['total_points']):
    if j==0:
        sorteggio=np.random.choice([1,2,3,4,5,6,7,8,9],size=9,replace=False)
    dfUEFA.iloc[i,5]=sorteggio[j]
    if j<8:
        j=j+1
    else: j=0
    i=i+1


# In[800]:


gruppo1=dfUEFA[dfUEFA['girone']==1.0][['country_full','total_points']]
gruppo2=dfUEFA[dfUEFA['girone']==2.0][['country_full','total_points']]
gruppo3=dfUEFA[dfUEFA['girone']==3.0][['country_full','total_points']]
gruppo4=dfUEFA[dfUEFA['girone']==4.0][['country_full','total_points']]
gruppo5=dfUEFA[dfUEFA['girone']==5.0][['country_full','total_points']]
gruppo6=dfUEFA[dfUEFA['girone']==6.0][['country_full','total_points']]
gruppo7=dfUEFA[dfUEFA['girone']==7.0][['country_full','total_points']]
gruppo8=dfUEFA[dfUEFA['girone']==8.0][['country_full','total_points']]
gruppo9=dfUEFA[dfUEFA['girone']==9.0][['country_full','total_points']]
gruppo1["punti"] = [0,0,0,0,0,0]
gruppo2["punti"] = [0,0,0,0,0,0]
gruppo3["punti"] = [0,0,0,0,0,0]
gruppo4["punti"] = [0,0,0,0,0,0]
gruppo5["punti"] = [0,0,0,0,0,0]
gruppo6["punti"] = [0,0,0,0,0,0]
gruppo7["punti"] = [0,0,0,0,0,0]
gruppo8["punti"] = [0,0,0,0,0,0]
gruppo9["punti"] = [0,0,0,0,0,0]


# In[801]:


def partita(grupp,i,j):
    tot=grupp.iloc[i,1]+grupp.iloc[j,1]
    risu=np.random.choice([i,j],size=2,replace=True,p=[grupp.iloc[i,1]/tot,grupp.iloc[j,1]/tot])
    if risu[0]==risu[1]==i:
        grupp.iloc[i,2]=grupp.iloc[i,2]+3
    if risu[0]==risu[1]==j:
        grupp.iloc[j,2]=grupp.iloc[j,2]+3
    if risu[0]!=risu[1]:
        grupp.iloc[i,2]=grupp.iloc[i,2]+1
        grupp.iloc[j,2]=grupp.iloc[j,2]+1
    


# In[802]:


def partita2(grupp,i,j):
    tot=grupp.iloc[i,2]+grupp.iloc[j,2]
    risu=np.random.choice([i,j],size=2,replace=True,p=[grupp.iloc[i,2]/tot,grupp.iloc[j,2]/tot])
    if risu[0]==risu[1]==i:
        grupp.iloc[i,2]=grupp.iloc[i,2]+3
        grupp.iloc[i,3]=grupp.iloc[i,3]+3
    if risu[0]==risu[1]==j:
        grupp.iloc[j,2]=grupp.iloc[j,2]+3
        grupp.iloc[j,3]=grupp.iloc[j,3]+3
    if risu[0]!=risu[1]:
        grupp.iloc[i,2]=grupp.iloc[i,2]+1
        grupp.iloc[j,2]=grupp.iloc[j,2]+1
        grupp.iloc[i,3]=grupp.iloc[i,3]+1
        grupp.iloc[j,3]=grupp.iloc[j,3]+1


# In[803]:


def girone(grupp):
    i=j=0
    while i<len(grupp):
        while j<len(grupp):
            if i!=j:
                partita(grupp,i,j)
            j=j+1
        i=i+1
        j=0


# In[804]:


def girone2(grupp):
    i=j=0
    while i<len(grupp):
        while j<len(grupp):
            if i!=j and i>j:
                partita2(grupp,i,j)
            j=j+1
        i=i+1
        j=0


# In[805]:


def secca(grupp2):
    tot=grupp2.iloc[0,1]+grupp2.iloc[1,1]
    y=np.random.choice([0,1],size=1,replace=True,p=[grupp2.iloc[0,1]/tot,grupp2.iloc[1,1]/tot])
    return grupp2.iloc[[y[0]]]


# In[806]:


def sesonouguali(grupp3):
    i=0
    grupp3=grupp3.sort_values('punti',ascending=[False])
    while i<len(grupp3)-1:
        if grupp3.iloc[i,2]==grupp3.iloc[i+1,2]:
            tot=grupp3.iloc[i,1]+grupp3.iloc[i+1,1]
            y=np.random.choice([i,i+1],size=1,replace=True,p=[grupp3.iloc[i,1]/tot,grupp3.iloc[i+1,1]/tot])
            grupp3.iloc[y,2]=grupp3.iloc[y,2]+0.5
        i=i+1 
    i=0
    grupp3=grupp3.sort_values('punti',ascending=[False])
    while i<len(grupp3)-1:
        if grupp3.iloc[i,2]==grupp3.iloc[i+1,2]:
            tot=grupp3.iloc[i,1]+grupp3.iloc[i+1,1]
            y=np.random.choice([i,i+1],size=1,replace=True,p=[grupp3.iloc[i,1]/tot,grupp3.iloc[i+1,1]/tot])
            grupp3.iloc[y,2]=grupp3.iloc[y,2]+0.2
        i=i+1 
    i=0
    grupp3=grupp3.sort_values('punti',ascending=[False])
    while i<len(grupp3)-1:
        if grupp3.iloc[i,2]==grupp3.iloc[i+1,2]:
            tot=grupp3.iloc[i,1]+grupp3.iloc[i+1,1]
            y=np.random.choice([i,i+1],size=1,replace=True,p=[grupp3.iloc[i,1]/tot,grupp3.iloc[i+1,1]/tot])
            grupp3.iloc[y,2]=grupp3.iloc[y,2]+0.05
        i=i+1 
    grupp3=grupp3.sort_values('punti',ascending=[False])
    return grupp3
    
    


# In[807]:


def sesonouguali2(grupp3):
    i=0
    grupp3=grupp3.sort_values('punti2',ascending=[False])
    while i<len(grupp3)-1:
        if grupp3.iloc[i,3]==grupp3.iloc[i+1,3]:
            tot=grupp3.iloc[i,1]+grupp3.iloc[i+1,1]
            y=np.random.choice([i,i+1],size=1,replace=True,p=[grupp3.iloc[i,1]/tot,grupp3.iloc[i+1,1]/tot])
            grupp3.iloc[y,3]=grupp3.iloc[y,3]+0.5
        i=i+1 
    i=0
    grupp3=grupp3.sort_values('punti2',ascending=[False])
    while i<len(grupp3)-1:
        if grupp3.iloc[i,3]==grupp3.iloc[i+1,3]:
            tot=grupp3.iloc[i,1]+grupp3.iloc[i+1,1]
            y=np.random.choice([i,i+1],size=1,replace=True,p=[grupp3.iloc[i,1]/tot,grupp3.iloc[i+1,1]/tot])
            grupp3.iloc[y,3]=grupp3.iloc[y,3]+0.2
        i=i+1 
    i=0
    grupp3=grupp3.sort_values('punti2',ascending=[False])
    while i<len(grupp3)-1:
        if grupp3.iloc[i,3]==grupp3.iloc[i+1,3]:
            tot=grupp3.iloc[i,1]+grupp3.iloc[i+1,1]
            y=np.random.choice([i,i+1],size=1,replace=True,p=[grupp3.iloc[i,1]/tot,grupp3.iloc[i+1,1]/tot])
            grupp3.iloc[y,3]=grupp3.iloc[y,3]+0.05
        i=i+1 
    grupp3=grupp3.sort_values('punti2',ascending=[False])
    return grupp3
    


# In[808]:


print('Gruppi di qualificazione')
print('Gruppo A')
print(gruppo1[['country_full']])
print('Gruppo B')
print(gruppo2[['country_full']])
print('Gruppo C')
print(gruppo3[['country_full']])
print('Gruppo D')
print(gruppo4[['country_full']])
print('Gruppo E')
print(gruppo5[['country_full']])
print('Gruppo F')
print(gruppo6[['country_full']])
print('Gruppo G')
print(gruppo7[['country_full']])
print('Gruppo H')
print(gruppo8[['country_full']])
print('Gruppo I')
print(gruppo9[['country_full']])


# In[809]:


girone(gruppo1)
girone(gruppo2)
girone(gruppo3)
girone(gruppo4)
girone(gruppo5)
girone(gruppo6)
girone(gruppo7)
girone(gruppo8)
girone(gruppo9)
gruppo1=sesonouguali(gruppo1)
gruppo2=sesonouguali(gruppo2)
gruppo3=sesonouguali(gruppo3)
gruppo4=sesonouguali(gruppo4)
gruppo5=sesonouguali(gruppo5)
gruppo6=sesonouguali(gruppo6)
gruppo7=sesonouguali(gruppo7)
gruppo8=sesonouguali(gruppo8)
gruppo9=sesonouguali(gruppo9)
q1=gruppo1.sort_values('punti',ascending=[False]).head(2)
q2=gruppo2.sort_values('punti',ascending=[False]).head(2)
q3=gruppo3.sort_values('punti',ascending=[False]).head(2)
q4=gruppo4.sort_values('punti',ascending=[False]).head(2)
q5=gruppo5.sort_values('punti',ascending=[False]).head(2)
q6=gruppo6.sort_values('punti',ascending=[False]).head(2)
q7=gruppo7.sort_values('punti',ascending=[False]).head(2)
q8=gruppo8.sort_values('punti',ascending=[False]).head(2)
q9=gruppo9.sort_values('punti',ascending=[False]).head(2)


# In[810]:


print('Gruppi di qualificazione')
print('Gruppo A')
print(gruppo1[['country_full','punti']])
print('Gruppo B')
print(gruppo2[['country_full','punti']])
print('Gruppo C')
print(gruppo3[['country_full','punti']])
print('Gruppo D')
print(gruppo4[['country_full','punti']])
print('Gruppo E')
print(gruppo5[['country_full','punti']])
print('Gruppo F')
print(gruppo6[['country_full','punti']])
print('Gruppo G')
print(gruppo7[['country_full','punti']])
print('Gruppo H')
print(gruppo8[['country_full','punti']])
print('Gruppo I')
print(gruppo9[['country_full','punti']])


# In[811]:


quali=pd.concat([q1,q2,q3,q4,q5,q6,q7,q8,q9])


# In[812]:


terze=pd.concat([gruppo1.sort_values('punti',ascending=[False]).iloc[[2]],gruppo2.sort_values('punti',ascending=[False]).iloc[[2]],gruppo3.sort_values('punti',ascending=[False]).iloc[[2]],gruppo4.sort_values('punti',ascending=[False]).iloc[[2]],gruppo5.sort_values('punti',ascending=[False]).iloc[[2]],gruppo6.sort_values('punti',ascending=[False]).iloc[[2]],gruppo7.sort_values('punti',ascending=[False]).iloc[[2]],gruppo8.sort_values('punti',ascending=[False]).iloc[[2]],gruppo9.sort_values('punti',ascending=[False]).iloc[[2]]])
terze=terze.sort_values('punti',ascending=[False])
terze=sesonouguali(terze)


# In[813]:


quali=pd.concat([quali,terze.head(3)])


# In[ ]:





# In[815]:


print('Spareggi')
print(terze.iloc[3,0] + ' vs '+ terze.iloc[8,0])
print(terze.iloc[4,0] + ' vs '+ terze.iloc[7,0])
print(terze.iloc[5,0] + ' vs '+ terze.iloc[6,0]) 


# In[816]:


sp1=pd.concat([terze.iloc[[3]],terze.iloc[[8]]])
sp2=pd.concat([terze.iloc[[4]],terze.iloc[[7]]])
sp3=pd.concat([terze.iloc[[5]],terze.iloc[[6]]])
q11=secca(sp1)
q22=secca(sp2)
q33=secca(sp3)
print('Vincitori spareggi')
print(q11.iloc[0,0])
print(q22.iloc[0,0])
print(q33.iloc[0,0])
quali=pd.concat([quali,q11,q22,q33])
quali=sesonouguali(quali)
print('Squadre qualificate')
print(quali[['country_full','punti']])


# In[817]:


quali["girone"] = np.nan
i=0
j=0
while i<len(quali['girone']):
    if j==0:
        sorteggio=np.random.choice([1,2,3,4,5,6],size=6,replace=False)
    quali.iloc[i,3]=sorteggio[j]
    if j<5:
        j=j+1
    else: j=0
    i=i+1


# In[818]:


gruppo1=quali[quali['girone']==1.0][['country_full','total_points','punti']]
gruppo2=quali[quali['girone']==2.0][['country_full','total_points','punti']]
gruppo3=quali[quali['girone']==3.0][['country_full','total_points','punti']]
gruppo4=quali[quali['girone']==4.0][['country_full','total_points','punti']]
gruppo5=quali[quali['girone']==5.0][['country_full','total_points','punti']]
gruppo6=quali[quali['girone']==6.0][['country_full','total_points','punti']]
gruppo1["punti2"] = [0,0,0,0]
gruppo2["punti2"] = [0,0,0,0]
gruppo3["punti2"] = [0,0,0,0]
gruppo4["punti2"] = [0,0,0,0]
gruppo5["punti2"] = [0,0,0,0]
gruppo6["punti2"] = [0,0,0,0]
gruppo1["giron"] = [1,1,1,1]
gruppo2["giron"] = [2,2,2,2]
gruppo3["giron"] = [3,3,3,3]
gruppo4["giron"] = [4,4,4,4]
gruppo5["giron"] = [5,5,5,5]
gruppo6["giron"] = [6,6,6,6]


# In[819]:


print('Gironi Europeo')
print('Gruppo A')
print(gruppo1[['country_full']])
print('Gruppo B')
print(gruppo2[['country_full']])
print('Gruppo C')
print(gruppo3[['country_full']])
print('Gruppo D')
print(gruppo4[['country_full']])
print('Gruppo E')
print(gruppo5[['country_full']])
print('Gruppo F')
print(gruppo6[['country_full']])


# In[820]:


girone2(gruppo1)
girone2(gruppo2)
girone2(gruppo3)
girone2(gruppo4)
girone2(gruppo5)
girone2(gruppo6)
gruppo1=sesonouguali2(gruppo1)
gruppo2=sesonouguali2(gruppo2)
gruppo3=sesonouguali2(gruppo3)
gruppo4=sesonouguali2(gruppo4)
gruppo5=sesonouguali2(gruppo5)
gruppo6=sesonouguali2(gruppo6)


# In[821]:


print('Gruppi di qualificazione')
print('Gruppo A')
print(gruppo1[['country_full','punti2']])
print('Gruppo B')
print(gruppo2[['country_full','punti2']])
print('Gruppo C')
print(gruppo3[['country_full','punti2']])
print('Gruppo D')
print(gruppo4[['country_full','punti2']])
print('Gruppo E')
print(gruppo5[['country_full','punti2']])
print('Gruppo F')
print(gruppo6[['country_full','punti2']])
print('Gruppo G')


# In[822]:


terze=pd.concat([gruppo1.sort_values('punti2',ascending=[False]).iloc[[2]],gruppo2.sort_values('punti2',ascending=[False]).iloc[[2]],gruppo3.sort_values('punti2',ascending=[False]).iloc[[2]],gruppo4.sort_values('punti2',ascending=[False]).iloc[[2]],gruppo5.sort_values('punti2',ascending=[False]).iloc[[2]],gruppo6.sort_values('punti2',ascending=[False]).iloc[[2]]])
terze=sesonouguali2(terze)


# In[823]:


terze=terze.head(4).sort_values('giron',ascending=[False])
configurazione=0
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(4,3,2,1):
    configurazione=1
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(5,3,2,1):
    configurazione=2
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(6,3,2,1):
    configurazione=3
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(5,4,2,1):
    configurazione=4
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(6,4,2,1):
    configurazione=5
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(6,5,2,1):
    configurazione=6
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(5,4,3,1):
    configurazione=7
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(6,4,3,1):
    configurazione=8
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(6,5,3,1):
    configurazione=9
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(6,5,4,1):
    configurazione=10
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(5,4,3,2):
    configurazione=11
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(6,4,3,2):
    configurazione=12
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(6,5,3,2):
    configurazione=13
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(6,5,4,2):
    configurazione=14
if (terze.iloc[0,4],terze.iloc[1,4],terze.iloc[2,4],terze.iloc[3,4])==(6,5,4,3):
    configurazione=15
configurazione


# In[824]:


match2=pd.concat([gruppo1.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo3.sort_values('punti2',ascending=[False]).iloc[[1]]])
match4=pd.concat([gruppo4.sort_values('punti2',ascending=[False]).iloc[[1]],gruppo5.sort_values('punti2',ascending=[False]).iloc[[1]]])
match6=pd.concat([gruppo4.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo6.sort_values('punti2',ascending=[False]).iloc[[1]]])
match8=pd.concat([gruppo1.sort_values('punti2',ascending=[False]).iloc[[1]],gruppo2.sort_values('punti2',ascending=[False]).iloc[[1]]])
if configurazione==1 or configurazione==2 or configurazione==3:
    match1=pd.concat([gruppo2.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo1.sort_values('punti2',ascending=[False]).iloc[[2]]])
if configurazione==4 or configurazione==5:
    match1=pd.concat([gruppo2.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo4.sort_values('punti2',ascending=[False]).iloc[[2]]])
if configurazione==6 or configurazione==7 or configurazione==9 or configurazione==10 or configurazione==11:
    match1=pd.concat([gruppo2.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo5.sort_values('punti2',ascending=[False]).iloc[[2]]])
if configurazione==8 or configurazione>11:
    match1=pd.concat([gruppo2.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo6.sort_values('punti2',ascending=[False]).iloc[[2]]])

if configurazione==6 or configurazione==7 or configurazione==8 or configurazione==9 or configurazione==10:
    match3=pd.concat([gruppo6.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo1.sort_values('punti2',ascending=[False]).iloc[[2]]])
if configurazione==4 or configurazione==5 or configurazione==14 or configurazione==13 or configurazione==12:
    match3=pd.concat([gruppo6.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo2.sort_values('punti2',ascending=[False]).iloc[[2]]])
if configurazione==15 or configurazione==11 or configurazione==1 or configurazione==2 or configurazione==3:
    match3=pd.concat([gruppo6.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo3.sort_values('punti2',ascending=[False]).iloc[[2]]])
    

if configurazione==4 or configurazione==5:
    match5=pd.concat([gruppo5.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo1.sort_values('punti2',ascending=[False]).iloc[[2]]])
if configurazione==1 or configurazione==2 or configurazione==3 or configurazione==6 or configurazione==11:
    match5=pd.concat([gruppo5.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo2.sort_values('punti2',ascending=[False]).iloc[[2]]])
if configurazione==7 or configurazione==8 or configurazione==9 or configurazione==12 or configurazione==13:
    match5=pd.concat([gruppo5.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo3.sort_values('punti2',ascending=[False]).iloc[[2]]])
if configurazione==14 or configurazione==15 or configurazione==10:
    match5=pd.concat([gruppo5.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo4.sort_values('punti2',ascending=[False]).iloc[[2]]])

if configurazione==1 or configurazione==7 or configurazione==8 or configurazione==11 or configurazione==12:
    match7=pd.concat([gruppo3.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo4.sort_values('punti2',ascending=[False]).iloc[[2]]])
if configurazione==2 or configurazione==4 or configurazione==13 or configurazione==14 or configurazione==15:
    match7=pd.concat([gruppo3.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo5.sort_values('punti2',ascending=[False]).iloc[[2]]])
if configurazione==3 or configurazione==5 or configurazione==6 or configurazione==9 or configurazione==10:
    match7=pd.concat([gruppo3.sort_values('punti2',ascending=[False]).iloc[[0]],gruppo6.sort_values('punti2',ascending=[False]).iloc[[2]]])


# In[825]:


print('Ottavi')
print(match1.iloc[0,0] + ' vs '+ match1.iloc[1,0])
print(match2.iloc[0,0] + ' vs '+ match2.iloc[1,0])
print(match3.iloc[0,0] + ' vs '+ match3.iloc[1,0])
print(match4.iloc[0,0] + ' vs '+ match4.iloc[1,0])
print(match5.iloc[0,0] + ' vs '+ match5.iloc[1,0])
print(match6.iloc[0,0] + ' vs '+ match6.iloc[1,0])
print(match7.iloc[0,0] + ' vs '+ match7.iloc[1,0])
print(match8.iloc[0,0] + ' vs '+ match8.iloc[1,0])


# In[826]:


match1=secca(match1)
match2=secca(match2)
match3=secca(match3)
match4=secca(match4)
match5=secca(match5)
match6=secca(match6)
match7=secca(match7)
match8=secca(match8)
print('Vincitori ottavi')
print(match1.iloc[0,0])
print(match2.iloc[0,0])
print(match3.iloc[0,0])
print(match4.iloc[0,0])
print(match5.iloc[0,0])
print(match6.iloc[0,0])
print(match7.iloc[0,0])
print(match8.iloc[0,0])


# In[827]:


quarto1=pd.concat([match1,match2])
quarto2=pd.concat([match3,match4])
quarto3=pd.concat([match5,match6])
quarto4=pd.concat([match7,match8])
print('Quarti')
print(quarto1.iloc[0,0] + ' vs '+ quarto1.iloc[1,0])
print(quarto2.iloc[0,0] + ' vs '+ quarto2.iloc[1,0])
print(quarto3.iloc[0,0] + ' vs '+ quarto3.iloc[1,0])
print(quarto4.iloc[0,0] + ' vs '+ quarto4.iloc[1,0])


# In[828]:


quarto1=secca(quarto1)
quarto2=secca(quarto2)
quarto3=secca(quarto3)
quarto4=secca(quarto4)
print('Vincitori quarti')
print(quarto1.iloc[0,0])
print(quarto2.iloc[0,0])
print(quarto3.iloc[0,0])
print(quarto4.iloc[0,0])


# In[829]:


semi1=pd.concat([quarto1,quarto2])
semi2=pd.concat([quarto3,quarto4])
print('Semifinali')
print(semi1.iloc[0,0] + ' vs '+ semi1.iloc[1,0])
print(semi2.iloc[0,0] + ' vs '+ semi2.iloc[1,0])


# In[830]:


semi1=secca(semi1)
semi2=secca(semi2)
print('Vincitori semifinali')
print(semi1.iloc[0,0])
print(semi2.iloc[0,0])


# In[831]:


finale=pd.concat([semi1,semi2])
print('Finale')
print(finale.iloc[0,0] + ' vs '+ finale.iloc[1,0])
finale=secca(finale)
print('Vincitori europeo')
print(semi1.iloc[0,0])


# In[ ]:




