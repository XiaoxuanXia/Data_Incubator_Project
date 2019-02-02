
# coding: utf-8

# In[1]:

# get the url for a specific movie

# coding: utf-8

# In[1]:

# get the url for a specific movie
def get_movie_url(keyword):
    import pandas as pd
    import requests
    import re
    from bs4 import BeautifulSoup
    url = "https://www.rottentomatoes.com/search/?search=%s"  % (keyword)
    response = requests.get(url)
    if not response.status_code == 200:
        return None
    try:
        results_page = BeautifulSoup(response.content,'lxml')
        #print(results_page.prettify())
        div_tag = results_page.find('div',{'id':"main_container"})
        data_string = div_tag.find('script').get_text().strip()
        pattern = re.compile(r'(\"year\"):(%s),(\"url\"):(\".*?\")'%(str(year)))
        movie_url = re.search(pattern, data_string)
        return movie_url.group(4).strip('"')
    except:
        return None
    
def get_film_name(year:int):
    import pandas as pd
    import requests
    import re
    from bs4 import BeautifulSoup
    
    
   # the maximum number of movies for each year set to be 600 
    year = str(year)
    max_page = 6
    for page in range(7):
        url = "https://www.boxofficemojo.com/yearly/chart/?page=%s&view=releasedate&view2=domestic&yr=%s&p=.htm" % (str(page+1), year)
        if requests.get(url,allow_redirects=False).status_code != 200:
            max_page = page-1
            break
    if max_page == 0:
        return "Less than 100 films this year >< Please change another year"
  
    # get the name, total_gross list (from  box office mojo) and its url in Rotten Tomato for each movie in a specific year
    name_list = []
    gross_list = []
    for n in range(max_page):
        page_ = str(n+1)
        url = "https://www.boxofficemojo.com/yearly/chart/?page=%s&view=releasedate&view2=domestic&yr=%s&p=.htm" % (page_, year)
        df_list = pd.read_html(url)
        movie = df_list[5].iloc[2:102,1:8].reset_index().iloc[:,1:4]
        movie.columns = ['name','studio','total gross']
        result_list_name = movie['name']
        for item in result_list_name:
            if re.search(r'\s\(',item):
                item_ = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]",'',item)
                name_list.append(item_)
            else:
                name_list.append(item)
        gross_list.extend(movie['total gross'])
        
    movie = pd.DataFrame({'name':name_list, 'total gross':gross_list})
    movie['url'] = movie['name'].apply(lambda x: get_movie_url(x))
    return movie

    
def get_film_name(year:int):
    import pandas as pd
    import requests
    import re
    from bs4 import BeautifulSoup
    
    
   # the maximum number of movies for each year set to be 600 
    year = str(year)
    max_page = 6
    for page in range(7):
        url = "https://www.boxofficemojo.com/yearly/chart/?page=%s&view=releasedate&view2=domestic&yr=%s&p=.htm" % (str(page+1), year)
        if requests.get(url,allow_redirects=False).status_code != 200:
            max_page = page-1
            break
    if max_page == 0:
        return "Less than 100 films this year >< Please change another year"
  
    # get the name, total_gross list (from  box office mojo) and its url in Rotten Tomato for each movie in a specific year
    name_list = []
    gross_list = []
    for n in range(max_page):
        page_ = str(n+1)
        url = "https://www.boxofficemojo.com/yearly/chart/?page=%s&view=releasedate&view2=domestic&yr=%s&p=.htm" % (page_, year)
        df_list = pd.read_html(url)
        movie = df_list[5].iloc[2:102,1:8].reset_index().iloc[:,1:4]
        movie.columns = ['name','studio','total gross']
        result_list_name = movie['name']
        for item in result_list_name:
            if re.search(r'\s\(',item):
                item_ = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]",'',item)
                name_list.append(item_)
            else:
                name_list.append(item)
        gross_list.extend(movie['total gross'])
        
    movie = pd.DataFrame({'name':name_list, 'total gross':gross_list})
    movie['url'] = movie['name'].apply(lambda x: get_movie_url(x))
    return movie

