
# coding: utf-8

# # Box Office

# In[143]:



#import pandas as pd
#data = pd.read_csv('movie_info_2016.csv')


# In[117]:


# clean data, transfer the box office to numerical
#delete the data that is  '-'
#the data is the final dataframe gain from the web_scaping
def clean_data(data):
    import pandas as pd
    data = data[data['Box Office'] != '-']
    data = data[data['Genre'] != '-']
    data['Critic Rating'] = data[data['Critic Rating'] != '-']['Critic Rating'].apply(pd.to_numeric)
    data['Critic Numbers'] = data[data['Critic Numbers'] != '-']['Critic Numbers'].apply(pd.to_numeric)
    data['User Rating'] = data[data['User Rating'] != '-']['User Rating'].apply(pd.to_numeric)
    data['User Numbers'] = data[data['User Numbers'] != '-']['User Numbers'].apply(pd.to_numeric)
    data['Box Office'] = data['Box Office'].apply(lambda x: x.strip('$').replace(',','')).apply(pd.to_numeric)
    return data

def box_office_visual(dataframe):
    #firstly clean the data
    data = clean_data(dataframe)
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib
    import seaborn as sns
    revenue = data[['Critic Rating', 'Critic Numbers', 'User Rating', 'User Numbers', 'Box Office']]
    
    fig = plt.figure(figsize=(12,12))
    ax1 = plt.subplot(2,2,1)
    ax1 = sns.regplot(x='Critic Rating', y='Box Office', data=revenue, x_jitter=.1)
    plt.title('Box Office by Critic Rating',fontsize=15)
    plt.xlabel('Critic Rating',fontsize=13)
    plt.ylabel('Box office',fontsize=13)

    ax2 = plt.subplot(2,2,2)
    ax2 = sns.regplot(x='Critic Numbers', y='Box Office', data=revenue, x_jitter=.1,color='g',marker='+')
    #ax2.text(6800,1.1e9,'r=0.78',fontsize=15)
    plt.title('Box office by Critic Numbers',fontsize=15)
    plt.xlabel('Critic Numbers',fontsize=13)
    plt.ylabel('Box office',fontsize=13)

    ax3 = plt.subplot(2,2,3)
    ax3 = sns.regplot(x='User Rating', y='Box Office', data=revenue, x_jitter=.1,color='g',marker='+')
    #ax2.text(6800,1.1e9,'r=0.78',fontsize=15)
    plt.title('Box office by User Rating',fontsize=15)
    plt.xlabel('Critic Numbers',fontsize=13)
    plt.ylabel('Box office',fontsize=13)

    ax4 = plt.subplot(2,2,4)
    ax4 = sns.regplot(x='User Numbers', y='Box Office', data=revenue, x_jitter=.1,color='g',marker='+')
    #ax2.text(6800,1.1e9,'r=0.78',fontsize=15)
    plt.title('Box office by User Numbers',fontsize=15)
    plt.xlabel('User Critic Numbers',fontsize=13)
    plt.ylabel('Box office',fontsize=13)
    
    plt.savefig("Box_Office_Visual.jpg")
    
#input is the final dataframe 
def corr_heatmap(dataframe):
    data = clean_data(dataframe)
    data_corr = data[['Critic Rating','Critic Numbers','User Rating','User Numbers','Box Office']].corr()
    f, ax = plt.subplots(figsize=(10,7))
    sns.heatmap(data_corr,cbar=True, annot=True,vmax=.8, cmap='PuBu',square=True)
    plt.savefig("corr_heatmap.jpg")


# # Movie Genre

# In[140]:


# create all genre set
# input is the final data table
def all_genre_set(data):
    data = clean_data(data)
    movie_genre = data['Genre']
    genre = set()   
    genre_set = set()
    for item in movie_genre:
        genre.update(str(item).strip().split(','))
    for item in genre:
        genre_set.add(str(item).strip())
    genre_set.remove('nan')
    return genre_set

def movie_genre_df(dataframe):
    genre_set = all_genre_set(data)
    genre_df = pd.DataFrame()
    for genre in genre_set:
        genre_df[genre] = data['Genre'].str.contains(genre).map(lambda x: 1 if x else 0)
    return genre_df


def genre_count_visual(dataframe,year:str):   
    import matplotlib.pyplot as plt
    import matplotlib
    import seaborn as sns
    genre_df = movie_genre_df(dataframe)
    genre_sum = genre_df.sum().sort_values(ascending = False)
    fig = plt.figure(figsize = (10,10))
    ax = plt.subplot(1,1,1)
    ax = genre_sum.plot.bar()
    plt.xticks(rotation=70)
    plt.title(f'Film genre in %s'%(year),fontsize = 18)
    plt.xlabel('genre', fontsize = 18)
    plt.ylabel('count', fontsize =18)
    plt.tight_layout()
    plt.savefig("genre_count_visual.jpg")

def genre_profit_visual(dataframe,year:str):
    genre_set = all_genre_set(dataframe)
    data = clean_data(dataframe)
    profit_by_genre = pd.Series(index = genre_set)
    genre_df = movie_genre_df(dataframe)
    genre_df['Box Office'] = data['Box Office']
    genre_sum = genre_df.sum().sort_values(ascending = False)
        
    for genre in genre_set:
        profit_by_genre.loc[genre] = genre_df[genre_df[genre] == 1]['Box Office'].sum()/genre_sum[genre]
    # plot the revenue of movie genre
    profit_by_genre = profit_by_genre.sort_values(ascending =False)
    
    fig = plt.figure(figsize = (10,10))
    ax = plt.subplot(1,1,1)
    ax = profit_by_genre.plot.bar()
    plt.xticks(rotation=70)
    plt.title(f'Film genre in %s'%(year),fontsize = 18)
    plt.xlabel('genre', fontsize = 18)
    plt.ylabel('average profit', fontsize =18)
    plt.tight_layout()
    plt.savefig("genre_profit_visual.jpg")


# # Studio Analysis

# In[163]:


# compare studio revenue
def compare_studio_revenue(dataframe):
    company_list = ['Universal Pictures', 'Paramount Pictures', '20th Century Fox','Sony','Warner']
    company_df = pd.DataFrame()
    genre_df = movie_genre_df(dataframe)
    data = clean_data(dataframe)
    
    for company in company_list:
        company_df[company]=data['Studio'].str.contains(company).map(lambda x:1 if x else 0)
    company_df = pd.concat([company_df,genre_df.iloc[:,:-1],data['Box Office']],axis=1)
    studio = pd.DataFrame(index=company_list,columns=company_df.columns[5:])
    
    for item in company_list:
        if company_df[item].sum() > 0:      
            studio.loc[item]=company_df.groupby(item,as_index=False).sum().iloc[1,5:]
    
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    studio['Box Office'].sort_values(ascending = False).plot(ax=ax,kind='bar')
    plt.xticks(rotation=60)
    plt.title('studio compares')
    plt.ylabel('Box office')
    plt.savefig("compare_studio_revenue.jpg")
    
def studio_different_genre(dataframe):
    company_list = ['Universal Pictures', 'Paramount Pictures', '20th Century Fox','Sony','Warner']
    company_df = pd.DataFrame()
    genre_df = movie_genre_df(dataframe)
    data = clean_data(dataframe)
    
    for company in company_list:
        company_df[company]=data['Studio'].str.contains(company).map(lambda x:1 if x else 0)
    company_df = pd.concat([company_df,genre_df.iloc[:,:-1],data['Box Office']],axis=1)
    studio = pd.DataFrame(index=company_list,columns=company_df.columns[5:])
    
    for item in company_list:
        if company_df[item].sum() > 0:      
            studio.loc[item]=company_df.groupby(item,as_index=False).sum().iloc[1,5:] 
    
    plt.figure(figsize=(20,15))
    for i in range(len(company_list)):
        item = company_list[i]
        if company_df[item].sum() > 0: 
            a = studio.loc[item].iloc[:-1]
            a['others'] = a.sort_values(ascending=False).iloc[8:].sum()
            a = a.sort_values(ascending=True).iloc[-9:]
            a = a[a>0]
            
            plt.subplot(2,3,1+i)
            plt.pie(a, labels=a.index, autopct='%.2f%%',startangle=90,pctdistance=0.75)
            plt.title(f'{item}',fontsize=15)
    plt.savefig("studio_different_genre.jpg")

