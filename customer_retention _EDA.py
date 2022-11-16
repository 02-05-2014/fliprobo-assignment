#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import scipy.stats as s
import matplotlib.pyplot as plt
#sns.set(style = 'whitegrid')
import warnings
warnings.filterwarnings('ignore')


# In[ ]:





# In[ ]:





# In[2]:


data = pd.read_excel(r"C:\Users\ASUS\Downloads\Customer_retention_dataset-\customer_retention_dataset.xlsx")
data.head()


# In[3]:


data.info()


# In[4]:


data.isnull().sum()


# As we can see there is no nulls in the dataset

# In[5]:


data.dtypes


# All the columns have object type except  pincode for which is of int type

# # Pre-processing the columns names
# 

# In[6]:


from string import digits

#Removing tab spaces
data.columns = data.columns.str.replace('\t','')

#Removing digits
remove_digits = str.maketrans('', '', digits)
data.columns = data.columns.str.translate(remove_digits)

#Removing leading and trailling spaces
data.columns = data.columns.str.strip()


# In[7]:


#Setting option to show max rows and max columns
pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows", None)


# In[8]:


data.head()


# In[9]:


data.isnull().sum().any()


# In[10]:


data.nunique()


# All the columns are of categorical types. There are no identifier or constant columns
# 
# 

# # EDA

# In[11]:


personal_info=['Gender of respondent','How old are you?','Which city do you shop online from?',
               'What is the Pin Code of where you shop online from?','Since How Long You are Shopping Online ?',
                   'How many times you have made an online purchase in the past  year?']


# In[12]:


for i in personal_info:
    if i!='What is the Pin Code of where you shop online from?':
        plt.figure(figsize=(8,6))
        data[i].value_counts().plot.pie(autopct='%1.1f%%')
        centre=plt.Circle((0,0),0.7,fc='white')
        fig=plt.gcf()
        fig.gca().add_artist(centre)
        plt.xlabel(i)
        plt.ylabel('')
        plt.figure()


# There is double the number of women than men who have taken this survey. -Most of the people are in their 30's followed by 20's, teenagers and senior citizen are the least in number. -Most of the people belong from delhi, noida and banglore, ambiguity can also be seen as noida has two categories (noida and grater noida) which need to be handled -Most of the people shopping online have been shopping from a long time. -Majority of people shop online 10 times a year, amiguity can also be seen for range 42 times and above which needs to be handled

# # Analysis on the basis of Various following factors
# 

# # Intention of Repeat purchase:
# 

# In[13]:


#Resolving ambiguity of column 
#Changing 42 times and above to 41 times and above
data['How many times you have made an online purchase in the past  year?'].replace('42 times and above','41 times and above',
                                                                                inplace=True)


# In[14]:


plt.figure(figsize=(15,8))
sns.lineplot(data['How many times you have made an online purchase in the past  year?'],
              data['From the following, tick any (or all) of the online retailers you have shopped from;'])


# Heavy shoppers who shop more than 41 times a year shop from all the online brands, some of the people who shop for 32-40 and less than 10 times a year seem to exclude myntra. People shop from Amazon and flipkart whatever be the case.

# In[15]:


dict={'31-40 times':35,'41 times and above':45,'Less than 10 times':5,'11-20 times':15,'21-30 times':25}
data['Average times made an online purchase']=data['How many times you have made an online purchase in the past  year?'].replace(dict)


# In[27]:


plt.figure(figsize=(20,8))
sns.violinplot(data['From the following, tick any (or all) of the online retailers you have shopped from;'],
               data['Average times made an online purchase'],hue=data['You feel gratification shopping on your favorite e-tailer'])
plt.xticks(rotation=45)


# Almost all the people who have shopped from amazon, flipkart and paytm are satisfied. People who shop from a more number of online brands dosent seem to be satisfied.

# In[16]:


plt.figure(figsize=(20,8))
sns.violinplot(data['From the following, tick any (or all) of the online retailers you have shopped from;'],
               data['Average times made an online purchase'],hue=data['Gaining access to loyalty programs is a benefit of shopping online'])
plt.xticks(rotation=45)


# People shopping from amazon and paytm are getting benefits from the loyalty points, flipkart and sanpdeal also seem to give such benefits but people who shop from almost everywhere disagree with this statement too

# # Online Retailing:
# 

# In[17]:


plt.figure(figsize=(10,8))
sns.countplot(data['Since How Long You are Shopping Online ?'],hue=data['How old are you?'])


# Highest number of people have been shopping online for above 4 years except for the age group below 20 years and above 50 years. People who are shopping online for 1-2 years does not include teenagers and elder people.

# # Converting Years to numbers for better analysis
# 

# In[18]:


data['Since How Long You are Shopping Online ?'].unique()


# In[19]:


dict={'Above 4 years':4.5,'3-4 years':3.5,'2-3 years':2.5,'1-2 years':1.5,'Less than 1 year':0.5}
data['Average years of shopping online']=data['Since How Long You are Shopping Online ?'].replace(dict)


# In[20]:


data['Which city do you shop online from?'].unique()


# In[21]:


#Changing Greater noida to noida
data['Which city do you shop online from?'].replace({'Greater Noida':'Noida'},inplace=True)


# In[22]:


plt.figure(figsize=(15,8))
sns.lineplot(data['Which city do you shop online from?'],data['Average years of shopping online'],hue=data['Gender of respondent'])


# In lines, we can see that density of female customers is more than male. Men living in banglore and ghaziabad shop have shopped online for less than 1 year. Highest number of men shopping online belong from delhi and noida, while men from moradabad have been shopping online for the longest. Women from meerut and noida have shopped the longest.

# In[23]:


plt.figure(figsize=(10,8))
sns.countplot(data['Since How Long You are Shopping Online ?'],
              hue=data['After first visit, how do you reach the online retail store?'])


# Even though people who are shopping online for more than 3 years donot use the application rather use search engine and direct url's in large number which indicates that online brands should update all their platforms rather than just application.

# # Brand image
# 

# In[24]:


performance=['Easy to use website or application',
       'Visual appealing web-page layout', 'Wild variety of product on offer',
       'Complete, relevant description information of products',
       'Fast loading website speed of website and application',
       'Reliability of the website or application',
       'Quickness to complete purchase',
       'Availability of several payment options', 'Speedy order delivery',
       'Privacy of customers’ information',
       'Security of customer financial information',
       'Perceived Trustworthiness',
       'Presence of online assistance through multi-channel']


# In[25]:


for i in performance:
        plt.figure(figsize=(8,6))
        data[i].value_counts().plot.pie(autopct='%1.1f%%')
        centre=plt.Circle((0,0),0.7,fc='white')
        fig=plt.gcf()
        fig.gca().add_artist(centre)
        plt.xlabel(i)
        plt.ylabel('')
        plt.figure()


# Amazon, Flipkart have been had the highest votes for having all the positive points and have maintained a very good brand image followed by paytm and the myntra.

# In[26]:


plt.figure(figsize=(12,10))
sns.stripplot(data['Why did you abandon the “Bag”, “Shopping Cart”?'],
              data['From the following, tick any (or all) of the online retailers you have shopped from;'])


# We can clearly see that most of the time people abandon the bag is because they get a better alternative offer or promo code not applicable. There is also lack of trust seen in amazon, flipkart and paytm by some people.

# # Loyalty
# 

# Loyal customers are those who keep using the same brand even if it is not good as other brands

# In[27]:


#Collecting all the negative remarks about a brand
bad=['Longer time to get logged in (promotion, sales period)',
       'Longer time in displaying graphics and photos (promotion, sales period)',
       'Late declaration of price (promotion, sales period)',
       'Longer page loading time (promotion, sales period)',
       'Limited mode of payment on most products (promotion, sales period)',
       'Longer delivery period', 'Change in website/Application design',
       'Frequent disruption when moving from one page to another']


# In[28]:


for i in bad:
        plt.figure(figsize=(15,6))
        sns.countplot(data[i],hue=data['Which of the Indian online retailer would you recommend to a friend?'])
        plt.xticks(rotation=45)
        plt.figure()


# Customers seem to be more loyal to amazon, flipkart and paytm as even though many of them have given negative remarks about them still they would recommend these platforms to their friend

# 
# 
# 
# 
# 
# *******************************************************************************************************************************
# 
# Conclusion:
# 
# The results of this study suggest following outputs which might be useful for online websites to extend their business
# 
# The cost of the product, the reliability of the online company and the return policies all play an equally important role in deciding the buying behaviour of online customers. The cost is an important factor as it was the basic criteria used by online retailers to attract customers. The reliability of the online company is also important, as it is even required in offline retail. It is important because customers are paying online, so they need to be sure of security of the online transaction. The return policies are important because in online retail customer does not get to feel the product. Thus, he wants to be sure that it will be possible to return the product if he does not like it in real. Whereas, the logistics factor, which included Cash on delivery option, One day delivery and the quality of packaging plays a secondary role in this process though these are Must-be-quality. This is so because these all does not interfere with the real product and people believe that this is the basic value that online websites provide.
# All the websites were not equally preferred by online customers. Amazon was the most preferred followed by Flipkart. This can be explained easily by previous result that we got. These two companies are most trusted in the industry and hence, have a huge reliability. Also, the sellers listed on these websites are generally from Tier 1 cities as compared to Snapdeal and PayTM which have more sellers from tier 2 and 3 cities. Also, these websites have the most lenient return policies as compared to others and also the time required to process a return is low for these.

# In[ ]:




