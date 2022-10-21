#!/usr/bin/env python
# coding: utf-8

# # Part I - Visualising Football Trends 
# ## by Andy Swan
# 
# ## Introduction
# I will be analysing the FIFA 21 players dataset set, and will be creating graphs and plots to visualise trends betweens the different variables.
# 
# 
# 
# ## Preliminary Wrangling
# 

# In[43]:


# import all packages and set plots to be embedded inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

get_ipython().run_line_magic('matplotlib', 'inline')


# > Load in your dataset and describe its properties through the questions below. Try and motivate your exploration goals through this section.
# 

# In[44]:


df = pd.read_csv('players_21.csv')


# ### What is the structure of your dataset?
# The dataset has 18944 rows and 106 columns. However, I will be removing the columns that a unnecessary for my analysis, as well as the rows with null entries. The majority of the variables within the dataset are numerical, but there is also categorical variables such as position, Nationality and preferred foot.
# 
# 
# ### What is/are the main feature(s) of interest in your dataset?
# I am interested to see what factors affect a players positon, salary and market value. What nations contain to best players in terms of market value and FIFA overall rating. As well as, what abilities the best players in the world possess. 
# 
# Age, Height, Weight, Preferred Foot, Overall, Position, Wage, Market Value and Nationality
# 
# 
# ### What features in the dataset do you think will help support your investigation into your feature(s) of interest?
# I believe that players age and position will affect what their market value and salary is. I would also think the physical factors such as height, weight and preferred foot will play a factor into players positions.
# 

# ## Data Cleaning 
# 
# 

# Removing the unnecessary columns for my analysis
# 

# In[45]:


df.info()


# In[ ]:





# In[46]:


df.drop(df.columns[80:106],axis=1, inplace = True)


# In[47]:


df.drop(['player_url','real_face','release_clause_eur','player_tags','team_position','loaned_from','joined','contract_valid_until','nation_position','nation_jersey_number', 'league_rank','player_traits'], axis = 1, inplace = True)


# In[48]:


df.info()


# In[49]:


df.isnull().sum()


# In[50]:


df.drop(['defending_marking','pace','shooting','passing','defending','dribbling','physic','gk_diving','gk_handling','gk_speed','gk_positioning','gk_reflexes','gk_kicking'], axis = 1, inplace = True)

#dropping theses columns as some they're only for outfield players and the others are only for GK's which leaves a lot of null values. \
#The dataset has columns that evaluate the same things for both outfields players and GK's, with no null values.


# In[51]:


df.dropna(inplace = True)


# In[52]:


df.info()


# In[53]:


df


# #### Split up the player_positions column to only take the first position. 
# After researching, I found that the first position listed is the players main position.
# 

# In[54]:


df['position'] = df['player_positions'].apply(lambda x: x.split(",")[0])

# Using x.split to split the listed positions per comma and only take the first value.


# In[55]:


df.drop('player_positions', axis = 1, inplace = True)

#Dropping the column with multiple positions listed


# In[56]:


df.info()


# #### Converting to the correct data type

# In[57]:


df['team_jersey_number'] = df['team_jersey_number'].astype(int)


# In[58]:


df.describe()


# ### Observations
# We can see that the average age is 25.2, with the top 25% being older than 28. There appears to be a significant outlier with an age of 53. We can also see there is a huge gap from the 75% wage to the maximum, this could be due to the top 25% of players all playing in the top leagues in europe, and the bottom 75% all playing in the lower leagues. However, this could also be due to the ages of the players.  

# ## Univariate Exploration
# 
# 

# In[59]:


sb.countplot(data = df, x = 'position', order = df['position'].value_counts().index, palette=['royalblue'])
plt.title('Number of players per position');


# According to our data, CB is the most played position.

# In[60]:


nationality_10 = df['nationality'].value_counts()[0:10]
plt.title('Top 10 countries with the most players')
plt.xlabel('Countries')
plt.ylabel('Count')
nationality_10.plot.bar();


# Most players on FIFA 21 are English. This could be due to there being more English leagues in the game than any other nations.    

# In[61]:


sb.countplot(data = df, x = 'preferred_foot')
plt.title('Number of left and right footed players')
plt.xlabel('Preferred Foot')
plt.ylabel('Count');


# The majority of players are right footed.

# In[62]:


sb.histplot(df['age'], binwidth = 1, kde = True)
plt.title('Histogram of players age')
plt.xlabel('Age');


# This distribution shows as slightly skewed to the right. Ther majority of the players are in their 20's.
# 

# In[63]:


df.age.value_counts();


# In[64]:


sb.histplot(df['weight_kg'], binwidth = 2, kde = True);
plt.title('Histogram of players weight')
plt.xlabel('Weight (kg)');


# The distribution for the weight of players appears normally distributed, with the majority within 74-76kg.

# In[65]:


sb.histplot(df['height_cm'], binwidth = 2, kde = True);
plt.title('Histogram of players height')
plt.xlabel('Height (cm)');


# Height also appears normally distributed.

# In[66]:


df.describe()


# ### Discuss the distribution(s) of your variable(s) of interest. Were there any unusual points? Did you need to perform any transformations?
# Both distributions for height and weight were both normally distributed. This is to be expected as if one is normally distributed, so should the other due to all players being professional footballers, being in good shaped.
# The distribution for height was slightly right skewed, which confirms what we saw with df.describe where the mean was greater the median for age.
# 
# When looking at the number of players playing certain positions, we could see that CB in the most popular. This is likely due to the fact that there is at least 2 CB's in the starting 11 of a football team.
# Most players are English, and most players are right-footed.
# 
# ### Of the features you investigated, were there any unusual distributions? Did you perform any operations on the data to tidy, adjust, or change the form of the data? If so, why did you do this?
# My data originally listed all the positions a player has played before, whereas I only wanted one positon per player. Therefore, I had to split up the positions and create a new column only containing the players primary position.
# 

# ## Bivariate Exploration
# 

# In[67]:


sb.regplot(data = df, x = 'wage_eur', y = 'value_eur', scatter_kws = {'alpha': 0.3})
plt.title('  Scatter plot comparing wage against market value')
plt.xlabel('Wage (€)')
plt.ylabel('Market Value (€)');
# Scatterplot between wage and value


# Shows a fairly strong, positive correlation

# In[86]:


sb.regplot(data = df, x = 'weight_kg', y = 'height_cm', scatter_kws = {'alpha': 0.3})
plt.title('Scatter plot comparing players weight against height')
plt.xlabel('Weight (kg)')
plt.ylabel('Height (cm)');
#Scatterplot of weight against height


# shows a weakly positive correlation 

# In[69]:


sb.regplot(data = df, x = 'age', y = 'movement_sprint_speed', scatter_kws = {'alpha': 0.1})
plt.title('Scatter plot comparing players age against sprint speed')
plt.xlabel('Age')
plt.ylabel('Sprint Speed');

#scatterplot of age against sprint speed


# No real correlation between the two, very slightly negative

# In[ ]:





# In[ ]:





# In[70]:


plt.figure(figsize = (12,7))
sb.violinplot(data = df, x = 'preferred_foot', y = 'weak_foot', inner = 'quartile');
plt.title('Violin plot comparing weak foot ratings depending on a players preferred foot')
plt.xlabel('Preferred Foot')
plt.ylabel('Weak Foot Rating');

#Violin plot comparing the weakfoot ratings of left and right footed players.  


# 2 very similar violin plots, with the majority of both right and left footed players have a weak foot rating of 3

# In[71]:


plt.figure(figsize=(12,7))
sb.countplot(data = df, x = 'position', hue = 'preferred_foot')
plt.title('Bar chart comparing the number of players playing a certain position depending on their preferred foot')
plt.xlabel('Position')
plt.ylabel('Count');

#bar chart showing the preferred foot of players based on their positions


# Most positions have more right footed players, but both LB and LWB have more left footed players than right footed players.

# In[72]:


plt.figure(figsize = (16,7))
sb.violinplot(data = df, x = 'position', y = 'age', inner = 'quartile', palette=['royalblue']);
plt.title('Violin plot comparing players age depending on a players position')
plt.xlabel('Position')
plt.ylabel('Age');

#Violin plot showing how the players ages range depending on what position they play.


# The violin plot shows that Strikers have the largest age range, and the on average GK's and CB's are the oldest.

# In[ ]:





# In[73]:


def func(x_axis,y_axis):
    df_50 = df.groupby(x_axis, as_index=False).apply(lambda x: x.nlargest(50, y_axis))
    return((df_50.groupby(x_axis)[y_axis].sum().sort_values(ascending = False).head(10)).plot.bar())

# creating a function to take the 50 highest rated value of certain variables.


# In[74]:


plt.figure(figsize = (8,8))
func('position', 'value_eur')
plt.title('Bar chart of the top 10 positions with the highest total market value')
plt.xlabel('Position')
plt.ylabel('Market Value');


# We can see that the most valued position is striker. 

# In[75]:


##join all these 3 plots as a subplot
plt.figure(figsize = (10,32))
plt.subplot(3,1,1)
func('nationality','overall')
plt.title('Bar chart of the top 10 nationalities with the highest total FIFA rating')
plt.xlabel('Country')
plt.ylabel('FIFA Rating')
plt.subplot(3,1,2)
func('nationality','wage_eur')
plt.title('Bar chart of the top 10 nationalities with the highest total wage')
plt.xlabel('Country')
plt.ylabel('Wage (€)')
plt.subplot(3,1,3)
func('nationality','value_eur')
plt.title('Bar chart of the top 10 nationalities with the highest total market value')
plt.xlabel('Country')
plt.ylabel('Market Value (€)');

#plotting bar charts for the top 10 nations whos top 50 players have the highest FIFA overall rating, wage and value.


# Here we can see that the nation with the 50 highest overall ratings and wage is Spain. French players have the highest total market value.

# ### Talk about some of the relationships you observed in this part of the investigation. How did the feature(s) of interest vary with other features in the dataset?
# Firsty, I observed a fairly strong positive correlation between players wage and market.  
# There was a fairly weak positive correlation between players weight and height, which is a little surprising as the majority of football players have similar body compositions.
# When comparing age against sprint speed, we see a very, very weak negative correlation.
# 
# For the violin plot comparing left and right footed players weak foot ability, we saw two very similar patterns with the majority of having a weak foot rating of 3. 
# 
# When comparing player positions against preferred foot, we could see that both left sided defensive positions have more left footed players than right, whereas all other positions favour right footed players.
# 
# I then created 3 subplots, which compared the nations with the top 50 players with the highest FIFA overall rating, wage, and market value. The 10 nations for all 3 graphs were the same, and the highest nation for each category was Spain, Spain and France, respectively.
# 
# 
# 
# 
# 
# ### Did you observe any interesting relationships between the other features (not the main feature(s) of interest)?
# 
# When plotting a violin plot for position and age, we can see that GK's and CB's are the oldest, and strikers have the largest range as there is a 53 year old striker. 

# ## Multivariate Exploration
# 
# > Create plots of three or more variables to investigate your data even
# further. Make sure that your investigations are justified, and follow from
# your work in the previous sections.

# In[76]:


df.describe()


# In[91]:


# scatter plot with colour bar against value, wage and age 
plt.scatter(data = df, x = 'value_eur', y = 'wage_eur', c = 'age')
plt.colorbar()
plt.xlim(1800000, 50000000)
plt.ylim(8000, 200000)
plt.title('Scatter plot of Wage against Market Value with relation to Age')
plt.xlabel('Market Value (€)')
plt.ylabel('Wage (€)');


# We can see that generally, the younger players are the lower their market value and wage is. 

# In[92]:


# scatterplot with colouyr bar against speed, accel, and age
plt.scatter(data = df, x = 'movement_sprint_speed', y = 'movement_acceleration', c = 'age')
plt.colorbar()
plt.xlim(40, 100)
plt.ylim(40, 100)
plt.title('Scatter plot of Sprint Speed against Acceleration with relation to Age')
plt.xlabel('Sprint Speed')
plt.ylabel('Acceleration');


# We can see the the older the player is lower their sprint speed and acceleration. The younger players dominate the middle values of the graph.

# In[101]:


stats = ['movement_sprint_speed', 'attacking_finishing','skill_dribbling','skill_long_passing','defending_standing_tackle','wage_eur','value_eur']

graph = sb.PairGrid(data = df, vars = stats)
graph.map_offdiag(plt.scatter, alpha = 0.1)
graph.map_diag(plt.hist);


# In[95]:


sb.heatmap(df[stats].corr(), annot = True, cmap = 'vlag_r', fmt = '.2f', center = 0)
plt.title('Heat map of the correlation of multiple variables important to a footballer'); 


# We can see that the most valued skill is long passing, and that finishing and dribbling has the strongest correlation out of all the skills.

# In[100]:


phys_stats = ['movement_sprint_speed', 'movement_acceleration','movement_agility','movement_reactions','movement_balance','age']

graph = sb.PairGrid(data = df, vars = phys_stats)
graph.map_offdiag(plt.scatter, alpha = 0.1)
graph.map_diag(plt.hist);


# In[97]:


sb.heatmap(df[phys_stats].corr(), annot = True, cmap = 'vlag_r', fmt = '.2f', center = 0)
plt.title('Heat map of the correlation of movement stats and age of footballer'); 


# We can see the all the movement stats are slightly negatively with age, except reactions. 

# ### Talk about some of the relationships you observed in this part of the investigation. Were there features that strengthened each other in terms of looking at your feature(s) of interest?
# 
# When comparing market value against wage with relation to age we could see that generally the younger the player the lower their market value and wage.
# When comparing sprint speed and acceleration with relation to age we could see that the slowest player are generally older, whilst the younger players tend to dominate the mid to higher speed and acceleration stats.
# 
# The first matrix and heat plot was to compare how transferrable all the main football skills are, and what skills are valued most when compared against market value and wage. We can see that the most valued skill is long passing, and that finishing and dribbling has the strongest correlation out of all the skills.
# 
# The second matrix and heat plot comparing age against movement stat, except reactions, has a slight negative correleation to age. These stats compared against each other are all strongly positively correlated also.
# 
# ### Were there any interesting or surprising interactions between features?
# 
# I was surprised to see the finishing wasn't seen as the most valuable skill as we saw earlier that attackers strikers were the most valuable position.

# ## Conclusions
# 
# Through my analysis, we can see that experience matters in relation to market value and salary as older players generally earn more and and have a higher market value than younger players.
# France, Brazil, Spain, England and Germany are the top 5 countries whose players have the highest market value and salary. 
# Striker is the most valuable position, but the skill which has the strongest correlation to both player salary and market value is long passing.

# 
# > Remove all Tips mentioned above, before you convert this notebook to PDF/HTML
# 
# 
# > At the end of your report, make sure that you export the notebook as an
# html file from the `File > Download as... > HTML or PDF` menu. Make sure you keep
# track of where the exported file goes, so you can put it in the same folder
# as this notebook for project submission. Also, make sure you remove all of
# the quote-formatted guide notes like this one before you finish your report!
# 
# 

# In[ ]:





# In[ ]:





# In[ ]:




