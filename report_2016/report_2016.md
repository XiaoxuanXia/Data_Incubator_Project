# Data Visualization

## What factors will affect the Box Office

<br>Firstly, we create scatter plots with regression line betwee Box Office, Critic Ratings, Critic Numbers, User Ratings and User Numbers.</br>
![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/Box_Office_Visual.jpg)
<br>We find that the numbers of reviews affects the Box Office more that the rating metric.</br>

<br>Then, we can create a heatmap for these variables to see their corrlation.</br>
![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/corr_heatmap.jpg)
<br>It's obvious that the number of reviews has the strongest relationship with the Box Office. It's important to spare no effort to promte the movie to get a good revenue.</br>

## Does the genre matter?

<br>We can count the number of movies for each genre to see which one is the most popular.</br>
![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/genre_count_visual.jpg)

<br>We can also check the average profit for each genre to see which one can be the most profitable.</br>
![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/genre_profit_visual.jpg)


## Which studio wins for this year?

<br>Here, we only compare 5 biggest company: Universal Pictures, Paramount Pictures, 20th Century Fox, Sony, Warner.</br>
<br>Firstly, we can sum the Box Office for each company.</br>
![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/compare_studio_revenue.jpg)
Then, we calculate the movie genre distribution for each studio.
![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/studio_different_genre.jpg)

# Regression

## Examine the Independence between variables

Before adding the interaction terms into our dataframe, we are interested in if there exist correlations between the 'Number of critic reviews' and 'Critic rating', if the 'Number of users review' is interrealted with 'User's Rating'.

By plotting each data point, we can tell from the graph 'Critic Ratings' are not independent of 'Number of critic reviews', so does the 'User Rating'. Therefore, we add two interaction terms into the base regression model.

![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/independence_1.png)

![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/independence_2.png)


## Model Fitting

We are interested in factors to influence the movie's box office in a specific year. Hence, we set 'Box Office' of 500+ movies as response variables, the factors input are: 'Name','Critic Rating','Critic Numbers','User Rating' and'User Numbers'.

Five models each takes variables as listed below:

![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/models_fitting.png)


## Model Selection
=======

The best model to fit is the model with highest R^2 value, which indicate a percentage of total response value captured by the model. The summary of the fit is as followed:

![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/Model_Selection.png)


## Residual Plotting
=======

The below graph plots the residual of the best model to fit in respect to each variable. Overall, the regression model captures the majority of noise of its box office in terms of variables input.

![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/Residual_Plotting.png)

# Text Mining

<br>Films reviews we have obtained online are divided into two types: audience reviews and critic reviews. We adopt various analysis methods trying to acquire information they deliver to us in various dimonsions.</br>

## Text Statistics Data Frame: what general information do the film reviews deliver to us?

![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/Text_Mining_Dataframe.png)
<br>We apply four-dimension analysis by creating this data frame. First of all, we count the percentage of positive and negative words in the text. As you can see, percentage of pos words is over two times than the neg in both audience and critic reviews. It shows consistent trend in both types that the overral comment this year on the films is positive. Then comes the emotion analysis. 'Positive', 'Trust' and 'Joy' show outstanding numbers. Last two rows show us the word frequency statistics and complexity calculation.</br>

## Dispersion Plot: how does each type of comment distribute across the text?

<br>Audience_Reviews_Dispersion_Plot</br>
![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/Audience_Reviews_Dispersion_Plot.png)

<br>Critic_Reviews_Dispersion_Plot</br>
![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/Critic_Reviews_Dispersion_Plot.png)

<br>Dispersion plot tells us how each type of comment(word) distributes across the text. From the graph we know audience gives more compliment than critics, with they refer more to the cast.</br>

## LDA Topic Modeling: nice reviewers, no spoilers

<br>Audience Reviews Topic Modeling</br>
![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/Audience_Reviews_Topic_Modeling.png)

<br>Critic Reviews Topic Modeling</br>
![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/Critic_Reviews_Topic_Modeling.png)

<br>It is interesting that even we set the model to output five topics, it ends up with five identical models, which means that no matter critics or audience, they comment quite general words, and do not talk much about the specific story of the films. That's  good news for those who have not seen the films.</br>

## Word Cloud: what words do reviewers like to use?

![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/Audience_Word_Cloud.png)
![Alt text](https://raw.githubusercontent.com/XiaoxuanXia/NerdHerd_Final_Project/master/report_2016/Critic_Word_Cloud.png)

<br>Generally speaking, common trend towards the films of this year is positive. By the way, 'the Star Wars' really shines!</br>

