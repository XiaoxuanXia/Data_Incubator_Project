# Fantastic Film Industry Where to Find it? 

## Introduction
<br>The American film industry is the industry leader worldwide in the form of artistic expression that comes to dominate the Twenty-first Century. Meanwhile, over 89% of U.S. movie markets are shared by ‘Big Six’ film studios.</br> 
<br>In our project, we are interested in helping film lovers make in-depth discovery into the Americane Film Industry during certain period of time. All you should do is to pick one year, and we will show you this year's fantastic film industry by first digging into review texts of top five films to take the 'KEY' words of this year. With the 'KEY', we will then lead you opening the gate of data visualization and help you build general concepts on the industry by statistical analysis on the number of movies released by five major studios: Universal Pictures, Paramount Pictures, 20th Century Fox, Sony and Warner, as well as the profits earned from these films. At the end of the trip we will uncover the secret of what contributes a profitable film by examining the relationship between its box office revenue and various other features, including review rating, review numbers and so on.</br>
<br>Our film information and reviews come mainly from www.boxofficemojo.com and www.rottentomatoes.com.</br>

## How do you start your journey?
<br>We divide our codes into several parts for different functions in case of long waiting time as well as failing to meet memory requirement. Each part is a .py file, and what you need is to select a four-digit year number as the input, and run all the parts with Python 2.7 or higher version in a right order. So remember to follow steps below to assure you a comfortable experience.</br>

### Part 1: Preparation
#### Step 1: Open ```requirements.txt``` to install and import necessary libraries.
#### Step 2: Run ```Web_Scrapper.py``` and ```Name_Boxoffice_Url.py``` to gain films information from the internet.
#### Step 3: Run ```Code_Get_Review.py``` to grab films reviews.

### Part 2: Enjoy the journey
#### Step 4: Run ```Review_Text_Mining.py``` to print review text mining analysis results.
#### Step 5: Run ```Data_Visualization.py``` to print film information data visualization results.
#### Step 6: Run ```Data_Regression.py``` to print box office revenue regression results. 


## Specific Description of Files and Functions
<br>If you come across any questions or are curious about our codes, see the descriptions below.</br> 
### Data Collection
#### Web Scrapper Functions:
1. ```get_info_for_a_movie```: <br > This is the main function for scrapping the data/features of a movie. </br>
**- Input:** It takes a dataframe as an input, containing *name*, *box office* and *url*.  
**- Output:** It returns a dataframe with 9 features using for following analysis: *Name, Critic Rating, Critic Numbers, User Rating, User Numbers, Runtime(minutes), Genre, Studio, Box Office.*  
**- Steps of implementation:**  <br /> 1. Start looping through the list of movies. <br /> 2. Check if every movie's website is avaliable <br /> 3. Get critics' and users' ratings and numbers. <br /> 4. Call *```movie_info_dict```* to build dictionary and add each movie's attribute to the corresponding list. <br /> 5. Construct and return the final dataframe for analysis.
2.  ```get_response```:<br /> *```get_respnse```* is the fucntion that get the content result of the input link, using libraries of ```requests``` and ```BeautifulSoup```.<br />
3. ```movie_info_dict```:<br /> *```movie_info_dict```* turns the info of a certain movie to dictionary. As the info part from every movie's website is not the same, we build a dictionary to store the information, indexed by these features' name. <br />
Source code stored in Web_Scrapper.py 

#### Name, Box Office, Url Scrapper Functions:
1. ```get_film_name(year:int)```: <br> This is the main function for scrapping the name and the box office  of a movie from https://www.boxofficemojo.com. **- Input:** It take a year, a integer, from 2000. **- Output:** It returns a dataframe contains *name*, *box office* and *its rotten tomato url*.
2. ```get_movie_url(keyword)```: <br> *```get_movie_url(keyword)```* is the fucntion that get the movie's homepage url at Rotten Tomatoes given the movie's name.  </br>
Source code stored in Name_Boxoffice_Url,py 

### Text Mining
#### Grab reviews online
Grab audience and critic reviews by using the function in Code_Get_Review.py.  
```get_total_reviews(year)```:
![](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/materials/Readme_Code_get_review.png)
<br>Input a single four-digit year number, reviews of five films of this year will be grabbed and saved to local directory as .txt files.</br>
#### Analyze the text
Make analysis on the reviews by using the function in Review_Text_Mining.py.  
```Reviews_Text_Analysis(year)```:
![](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/materials/Readme_Review_Text_Mining_part2.png)
<br>Input a single four-digit year number, reviews will be automatically loaded from local directory .txt files, and analysis results will orderly be printed as shown in the example report.</br>

### Data Visualization
####  What affects Box Office Most?
Functions below all take a dataframe gained from ```get_info_for_a_movie``` as an input and will save the image to your local path.  
1. ```box_office_visual(dataframe)```: This is the function to show the relationship of *Critic Rating*, *Critic Numbers*, *User Rating*, *User Numbers* with *Box Office*. 
2. ```corr_heatmap(dataframe)```: This is the function to show the correlation coefficient of *Critic Rating*, *Critic Numbers*, *User Rating*, *User Numbers* and *Box Office* in a heatmap. 
#### Does the genre matter?
Functions below all take a dataframe and the year(str) gained from ```get_info_for_a_movie``` as an input and will save the image to your local path.  
1.```genre_count_visual(dataframe,year:str)```: This shows a bar plot for the numbers of movie of different genre in the given year.  
2.```genre_profit_visual(dataframe,year:str)```: This will shows a comparison the average Box Office among different genre in the given year.
#### Which studio wins for this year?
Here, we only compare 5 biggest company: Universal Pictures, Paramount Pictures, 20th Century Fox, Sony, Warner.  
Functions below all take a dataframe gained from ```get_info_for_a_movie``` as an input and will save the image to your local path.
1.```compare_studio_revenue(dataframe)```: The bar plot compares the total gross for each studio in the given year. 
2.```studio_different_genre(dataframe)```: This will shows the movie genre distribution for each studio in the given year.

### Movie Regression Function
### The input of the Movie_Regression Function is the file path of type Str.
Sub functions within the Movie_Regression Function:
#### Movie_dataframe(Movie_Data):
Function input is the movie data of a specific year in csv type. The aim of this functions is to construct cloumns of input variables and responses, then clear off rows with missing numerical values.Function output is the cleaned dataframe.
#### Model_Fitting(df):
Function input is the data frame returned from the Movie_dataframe function. The aim of this function is to constructing five regression models of distinct variable sets, then return a dictionary whose keys are the model and values are the responding model R^2 values.
#### Find_Best_Model(Best_Model):
Function input is the dictionary contains each model and its R^2 value. Find_Best_Model would select the regression model with the highest R^2 value and print the summary of that model out. Such model will be returned as the output of the function. 
<br> Source code stored in Data_Regression.py </br>

## Example Report
### Why not see what happened in 2016 Film Industry?
<br>In the folder *report_2016*, we use the year 2016 as an example to show our whole analysis process.</br> 
<br>Open file ```report_2016.md```to see our analysis results for the 2016 film industry.</br>

