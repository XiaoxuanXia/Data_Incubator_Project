
# coding: utf-8

# In[20]:


def Movie_Regression(path):
    import pandas as pd
    from pandas import DataFrame

    #Constructing the DataFrame
    MovieData = pd.read_csv(path)
    
    def Movie_dataframe(Movie_data):
        df = DataFrame(Movie_data,columns=['Name','Critic Rating','Critic Numbers','User Rating','User Numbers','Box Office'])
        df = df[(df['Critic Rating']!='-') & (df['Critic Numbers']!='-') & (df['User Rating']!='-') & (df['User Numbers']!='-')]
        df['Critic Rating'] = pd.to_numeric(df['Critic Rating'])
        df['User Rating'] = pd.to_numeric(df['User Rating'])
        df['Critic Numbers'] = pd.to_numeric(df['Critic Numbers'])
        df['User Numbers'] = pd.to_numeric(df['User Numbers'])
        df['Box Office'] = df['Box Office'].apply(lambda x: x.strip('$').replace(',','')).apply(pd.to_numeric)
        df['UserRating*UserNumbers'] = pd.Series(df['User Rating'] * df['User Numbers'], name='UserRating*UserNumbers')
        df['CriticRating*CriticNumbers'] = pd.Series(df['Critic Rating'] * df['Critic Numbers'], name='CriticRating*CriticNumbers')
        return df
   
    df = Movie_dataframe(MovieData)

    #examine the independece
    import matplotlib.pyplot as plt
    from sklearn import linear_model
    import statsmodels.api as sm

    plt.scatter(df['Critic Numbers'], df['Critic Rating'], color='red')
    plt.title('Critic Rating VS Critic Numbers', fontsize=14)
    plt.xlabel('Critic Numbers', fontsize=14)
    plt.ylabel('Critic Rating(%)', fontsize=14)
    plt.grid(False)
    print (plt.show())

    plt.scatter(df['User Numbers'], df['User Rating'], color='red')
    plt.title('User Rating VS User Numbers', fontsize=14)
    plt.xlabel('User Numbers', fontsize=14)
    plt.ylabel('User Rating', fontsize=14)
    plt.grid(False)
    print (plt.show())

    #Model Fitting
    from sklearn import linear_model
    import statsmodels.api as sm

    def Model_Fitting(df):
        #Model 1 
        X1 = df[['Critic Rating','Critic Numbers']]
        Y1 = df['Box Office']
        regr1 = linear_model.LinearRegression()
        regr1.fit(X1, Y1)

        X1 = sm.add_constant(X1) # adding a constant 
        model1 = sm.OLS(Y1, X1).fit()
        model1_R = sm.OLS(Y1, X1).fit().rsquared

        #Model 2 
        X2 = df[['User Rating','User Numbers']]
        Y2 = df['Box Office']
        regr2 = linear_model.LinearRegression()
        regr2.fit(X2, Y2)

        X2 = sm.add_constant(X2) # adding a constant 
        model2 = sm.OLS(Y2, X2).fit()
        model2_R = sm.OLS(Y2, X2).fit().rsquared

        #Model 3 
        X3 = df[['User Rating','User Numbers','UserRating*UserNumbers']]
        Y3 = df['Box Office']
        regr3 = linear_model.LinearRegression()
        regr3.fit(X3, Y3)

        X3 = sm.add_constant(X3) # adding a constant 
        model3 = sm.OLS(Y3, X3).fit()
        model3_R = sm.OLS(Y3, X3).fit().rsquared

        #Model 4 
        X4 = df[['Critic Rating','Critic Numbers','CriticRating*CriticNumbers']]
        Y4 = df['Box Office']
        regr4 = linear_model.LinearRegression()
        regr4.fit(X4, Y4)

        X4 = sm.add_constant(X4) # adding a constant 
        model4 = sm.OLS(Y4, X4).fit()
        model4_R = sm.OLS(Y4, X4).fit().rsquared

        #Model 5
        X5 = df[['Critic Rating','Critic Numbers','User Rating','User Numbers','UserRating*UserNumbers','CriticRating*CriticNumbers']]
        Y5 = df['Box Office']
        regr5 = linear_model.LinearRegression()
        regr5.fit(X5, Y5)

        #with statsmodels
        X5 = sm.add_constant(X5) # adding a constant 
        model5 = sm.OLS(Y5, X5).fit()
        model5_R = sm.OLS(Y5, X5).fit().rsquared
        
        Model = [(model1,model1_R),(model2,model2_R),(model3,model3_R),(model4,model4_R),(model5,model5_R)]
        
        return Model
    
    model_fitting = Model_Fitting(df)
    
    #Model Selection
    explaination = '''Model 1 takes variable : 'Critic Rating','Critic Numbers' \n
    Model 2 takes variable : 'User Rating','User Numbers' \n
    Model 3 takes variable : 'User Rating','User Numbers','UserRating*UserNumbers' \n
    Model 4 takes variable : 'Critic Rating','Critic Numbers','CriticRating*CriticNumbers' \n
    Model 5 takes variable : 'Critic Rating','Critic Numbers','User Rating','User Numbers','UserRating*UserNumbers','CriticRating*CriticNumbers' \n
    '''
    def Find_Best_Model(Best_Model):
        Max_R = max(Best_Model,key= lambda x:x[1])
        for number, item in enumerate(Best_Model):
            if item == Max_R:
                key = number
        print (explaination,'The Best Model is: Model',key+1,'\n\n',model_fitting[key][0].summary())
        return model_fitting[key][0]

    best_model = Find_Best_Model(model_fitting)

    #Residual Plotting
    fig = plt.figure(figsize=(16, 15))
    fig = sm.graphics.plot_ccpr_grid(best_model, fig=fig)

