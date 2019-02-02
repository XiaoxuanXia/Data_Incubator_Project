import pandas as pd

# Build the df

def get_info_for_a_movie(movie_dataframe):    
    import re
    import numpy as np    
    import pandas as pd
    
    #using for get the content in the website

    def get_response(url):
        import requests
        from bs4 import BeautifulSoup

        response = requests.get(url)
        if response.status_code != 200:
            return None
        results_page = BeautifulSoup(response.content,'lxml')

        return results_page

    # Make the info of one movie as a dictionary
    # Conveneient for get_info_for_a_movie to create column 

    def movie_info_dict(movie_info):
        dict_ = {}
        category_name = movie_info.find_all('div',class_='meta-label subtle')
        movie_property =  movie_info.find_all('div',class_='meta-value')

        for i in range(len(category_name)):
            dict_[category_name[i].get_text().strip()] = movie_property[i].get_text().strip()

        return dict_

    # 10 variables in the final df
    
    list_input = list(movie_dataframe['url'])
    Name = list(movie_dataframe['name'])
    Total_Gross = list(movie_dataframe['total gross'])
    Critic_rating = []
    Critic_numbers = []
    User_rating = []
    User_numbers = [] 
    Genre = []
    Runtime = []     
    Studio = []

    for n in range(len(Total_Gross)):
        item = list_input[n]
        try:
            results_page = get_response('https://www.rottentomatoes.com' + item)
            if not results_page:
                raise ValueError

        #if the website is unavailable, add '-' to all its features

        except:
            User_rating.append('-')
            User_numbers.append('-')
            Critic_rating.append('-')
            Critic_numbers.append('-')
            
            Genre.append('-')
            Runtime.append('-')
            Studio.append('-')        
            continue

        # add every movie's feature on the website
        
        try:    
            User_rating.append(float(results_page.find('div',class_="audience-score meter").get_text().strip().split('\n')[0][:-1])/100)
        except:
            User_rating.append('-')
        try:
            User_numbers.append(int(results_page.find('div',class_="audience-info hidden-xs superPageFontColor").find_all('div')[1].get_text().strip().split('\n')[1].strip().replace(',', '')))
        except:
            User_numbers.append('-')
        try:
            Critic_rating.append(float(results_page.find('div',class_="critic-score meter").get_text().strip().split('\n')[0][:-1])/100)
        except:
            Critic_rating.append('-')
        try:    
            Critic_numbers.append(int(results_page.find('div',{'id':"scoreStats"}).find_all('div')[1].get_text().strip()[17:]))
        except:
            Critic_numbers.append('-')

        # because every movie's info is not quite same, create the dictionary to store the info
        # get the featrue if it exists in the dictionary, otherwise append '-'
            
        movie_info = results_page.find('ul',class_="content-meta info")
        info_dict = movie_info_dict(movie_info)            
            
        genre = ', '.join(re.findall(r'\b[\w &]+\b',info_dict['Genre:'])) if 'Genre:' in info_dict.keys() else '-'
        runtime = int(info_dict['Runtime:'].split(' ')[0]) if 'Runtime:' in info_dict.keys() else '-'
        studio = info_dict['Studio:'] if 'Studio:' in info_dict.keys() else '-'
        try:    
            Genre.append(genre)
        except:
            Genre.append('-')
        try:
            Runtime.append(runtime)
        except:
            Runtime.append('-')
        try:
            Studio.append(studio)
        except:  
            Studio.append('-')
    
    # put every feature(column) together to form the final df

    df = pd.DataFrame({'Name':Name,'Critic Rating':Critic_rating,'Critic Numbers':Critic_numbers,\
                       'User Rating':User_rating,'User Numbers':User_numbers,\
                       'Runtime (minutes)':Runtime,'Genre':Genre,'Studio':Studio,'Box Office': Total_Gross})    
    
    return df