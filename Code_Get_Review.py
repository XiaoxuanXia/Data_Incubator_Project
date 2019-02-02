#!/usr/bin/env python
# coding: utf-8

# In[87]:


def get_total_reviews(year):
    import pandas as pd
    import requests
    import re
    from bs4 import BeautifulSoup
    
    def get_audience_reviews(part_url):
        audience_review_list = []
        for page in range(20):      #get reviews on first 20 pages
            url = "https://www.rottentomatoes.com%s/reviews/?page=%s&type=user&sort=" % (part_url, str(page+1))
            response = requests.get(url,allow_redirects=False)
            if not response.status_code == 200:
                break
            results_page = BeautifulSoup(response.content,'lxml')
            list_ = results_page.find_all('div', {'class':'user_review'})
            for review in list_: 
                audience_review_list.append(review.get_text())
        return audience_review_list
    
    def get_critic_reviews(part_url):
        critic_review_list = []
        for page in range(20):      #get reviews on first 20 pages
            url = "https://www.rottentomatoes.com%s/reviews/?page=%s&sort=" % (part_url, str(page+1))
            response = requests.get(url,allow_redirects=False)
            if not response.status_code == 200:
                break
            results_page = BeautifulSoup(response.content,'lxml')
            list_ = results_page.find_all('div', {'class':'review_desc'})
            for review in list_: 
                critic_review_list.append(review.get_text())
        return critic_review_list
    
    def get_movie_url(keyword, year):
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

###########################################################################################################################################        
#     Our original plan was to grab 600 films each year to do review text mining. In view of the endless running time as well as too high
#     the generalization of the topic, we adjust the plan to be grabing top five movies, 20 pages of reviews per film.
#     year = str(year)
###########################################################################################################################################
#     max_page = 6
#     for page in range(7):
#         url = "https://www.boxofficemojo.com/yearly/chart/?page=%s&view=releasedate&view2=domestic&yr=%s&p=.htm" % (str(page+1), year)
#         if requests.get(url,allow_redirects=False).status_code != 200:
#             max_page = page-1
#             break
#     if max_page == 0:
#         return "Less than 100 films this year >< Please change another year"
    
    audience_review = []
    critic_review = []
    page_ = '1'
    url = "https://www.boxofficemojo.com/yearly/chart/?page=%s&view=releasedate&view2=domestic&yr=%s&p=.htm" % (page_, year)
    df_list = pd.read_html(url)
    movie = df_list[5].iloc[2:102,1:8].reset_index().iloc[:,1:4]
    movie.columns = ['name','studio','total gross']
    result_list_name = movie['name']
    n = 0
    while n < 5:
        item = result_list_name[n]
        if re.search(r'\s\(',item):
            name = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]",'',item)
        else:
            name = item
        part_url = get_movie_url(name,year)
        if part_url == None:
            continue
        audience_review.append(get_audience_reviews(part_url))
        critic_review.append(get_critic_reviews(part_url))
        n += 1
        
    print('Succeed getting audience reviews of',len(audience_review),'films.')
    print('Succeed getting critic reviews of',len(critic_review),'films.')
    audience_path = 'audience_review_%s.txt'% str(year)
    critic_path = 'critic_review_%s.txt'% str(year)
    with open(audience_path, 'w') as file:
        for film in audience_review:
            for words in film:
                try:
                    file.write(str(words))
                except:
                    continue
        file.close()
    with open(critic_path, 'w') as file:
        for film in critic_review:
            for words in film:
                try:
                    file.write(str(words))
                except:
                    continue
        file.close()
    print('Output Complete!')
    return True


# In[88]:


get_total_reviews(2016)

