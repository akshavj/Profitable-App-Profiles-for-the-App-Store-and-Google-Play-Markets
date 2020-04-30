#!/usr/bin/env python
# coding: utf-8

# ## Profitable App Profiles for the App Store and Google Play Markets
# Our aim in this project is to find mobile app profiles that are profitable for the App Store and Google Play markets. We're working as data analysts for a company that builds Android and iOS mobile apps, and our job is to enable our team of developers to make data-driven decisions with respect to the kind of apps they build.
# 
# At our company, we only build apps that are free to download and install, and our main source of revenue consists of in-app ads. This means that our revenue for any given app is mostly influenced by the number of users that use our app. Our goal for this project is to analyze data to help our developers understand what kinds of apps are likely to attract more users.

# ## Opening and Exploring the Data
# As of September 2018, there were approximately 2 million iOS apps available on the App Store, and 2.1 million Android apps on Google Play.
# 
# Collecting data for over four million apps requires a significant amount of time and money, so we'll try to analyze a sample of data instead. To avoid spending resources with collecting new data ourselves, we should first try to see whether we can find any relevant existing data at no cost. Luckily, these are two data sets that seem suitable for our purpose:
# 
# - [A data set](https://www.kaggle.com/lava18/google-play-store-apps) containing data about approximately ten thousand Android apps from Google Play.
# - [A data set](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps) containing data about approximately seven thousand iOS apps from the App Store.

# In[3]:


opened_file = open('AppleStore.csv',encoding="utf8")
opened_file
from csv import reader
read_file = reader(opened_file)
ios = read_file
ios = list(ios)
ios_header = ios[0]
ios = ios[1:]

## Importing Android dataset
opened_file = open('googleplaystore.csv', encoding="utf8")
opened_file
from csv import reader
read_file = reader(opened_file)
android = read_file
android = list(android)
android_header = android[0]
android = android[1:]


# To make them easier to explore, we created a function named explore_data() that we can repeatedly use to print rows in a readable way.

# In[4]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[5]:


print(android_header)
print('\n')
explore_data(android, 0, 3, True)


# In[9]:


print(ios_header)
print('\n')
explore_data(ios, 0, 3, True)


# ## Deleting Wrong Data
# The Google Play data set has a dedicated discussion section, and we can see that [one of the discussions outlines](https://www.kaggle.com/lava18/google-play-store-apps/discussion/66015) an error for row 10472. Let's print this row and compare it against the header and another row that is correct.

# In[20]:


print(android[10472])  ## Wrong row
print('\n')
print(android_header) ## Header
print('\n')
print(android[0]) ## Correct row


# The row 10472 corresponds to the app _Life Made WI-Fi Touchscreen Photo Frame_ , and we can see that the rating is 19. This is clearly off because the maximum rating for a Google Play app is 5. As a consequence, we'll delete this row.

# In[21]:


print(len(android)) ## Length of the dataset
del android[10472] ## Deleting this row
print(len(android)) ## Length of the dataset after deleting the row 10472


# ## Removing Duplicate Entries
# 
# If we explore the Google Play data set long enough, we'll find that some apps have more than one entry. For instance, the application Instagram has four entries:

# In[25]:


for app in android:
    name = app[0]
    if name == 'Instagram':
        print(app)


# In total, there are **1,181 cases** where an app occurs more than once:

# In[26]:


duplicate_apps = []
unique_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
        
print('Number of duplicate apps:', len(duplicate_apps))
print('\n')
print('Examples of duplicate apps:', duplicate_apps[:12])


# We don't want to count certain apps more than once when we analyze data, so we need to remove the duplicate entries and keep only one entry per app. One thing we could do is remove the duplicate rows randomly, but we could probably find a better way.
# 
# If you examine the rows we printed two cells above for the Instagram app, the main difference happens on the fourth position of each row, which corresponds to the number of reviews. The different numbers show that the data was collected at different times. We can use this to build a criterion for keeping rows. We won't remove rows randomly, but rather we'll keep the rows that have the highest number of reviews because the higher the number of reviews, the more reliable the ratings.
# 
# To do that, we will:
# 
# - Create a dictionary where each key is a unique app name, and the value is the highest number of reviews of that app
# - Use the dictionary to create a new data set, which will have only one entry per app (and we only select the apps with the highest number of reviews)

# In[29]:


print('Expected number of unique rows:', len(android) - 1181)


# Let's build the dictionary:

# In[30]:


reviews_max = {}
for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


# In a previous code cell, we found that there are 1,181 cases where an app occurs more than once, so the length of our dictionary (of unique apps) should be equal to the difference between the length of our data set and 1,181.

# In[31]:


print('Expected length:',len(android) - 1181)
print('Actual length:', len(reviews_max))


# In[33]:


android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if reviews_max[name] == n_reviews and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


# Let's explore the new dataset and confirm the number of rows is 9569

# In[37]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[38]:


explore_data (android_clean, 0, 3, True)


# ## Removing Non English Apps:
# In the previous step, we managed to remove the duplicate app entries in the Google Play data set. Remember we use English for the apps we develop at our company, and we'd like to analyze only the apps that are directed toward an English-speaking audience. However, if we explore the data long enough, we'll find that both data sets have apps with names that suggest they are not directed toward an English-speaking audience.

# In[48]:


## Non-English Apps in IOS
print(ios[813][1])
print(ios[6731][1])
print('\n')
## Non-English Apps in Android
print(android_clean[4412][0])
print(android_clean[7940][0])


# We're not interested in keeping these kind of apps, so we'll remove them. One way to go about this is to remove each app whose name contains a symbol that is not commonly used in English text — English text usually includes letters from the English alphabet, numbers composed of digits from 0 to 9, punctuation marks (., !, ?, ;, etc.), and other symbols (+, *, /, etc.).
# 
# All these characters that are specific to English texts are encoded using the ASCII standard. Each ASCII character has a corresponding number between 0 and 127 associated with it, and we can take advantage of that to build a function that checks an app name and tells us whether it contains non-ASCII characters.
# 
# We built this function below, and we use the built-in ord() function to find out the corresponding encoding number of each character.

# In[55]:


def is_english(string):
    for character in string:
        if ord(character) > 127:
            return False
    return True

print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# The function seems to work fine, but some English app names use emojis or other symbols (™, — (em dash), – (en dash), etc.) that fall outside of the ASCII range. Because of this, we'll remove useful apps if we use the function in its current form.

# In[56]:


print(ord('™'))
print(ord('😜'))


# To minimize the impact of data loss, we'll only remove an app if its name has more than three non-ASCII characters:

# In[58]:


def is_english(string):
    non_ascii = 0
    
    for charecter in string:
        if ord(charecter) > 127:
            non_ascii += 1
            
    if non_ascii > 3:
        return False
    else:
        return True

print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))
        


# In[60]:


android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in ios:
    name = app[1]
    if is_english(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# In[61]:


print('Previous count of android apps:',len(android_clean))
print('After cleaning non english apps:', len(android_english))
print('\n')
print('Previous count of ios apps:', len(ios))
print('After cleaning non english apps:', len(ios_english))


# ## Isolating the Free Apps:
# As we mentioned in the introduction, we only build apps that are free to download and install, and our main source of revenue consists of in-app ads. Our data sets contain both free and non-free apps, and we'll need to isolate only the free apps for our analysis. Below, we isolate the free apps for both our data sets.

# In[65]:


android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)

for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)

print('Android apps:', len(android_final))
print('IOS apps:',len(ios_final))


# We're left with 8864 Android apps and 3222 iOS apps, which should be enough for our analysis.

# ## Part one
# As we mentioned in the introduction, our aim is to determine the kinds of apps that are likely to attract more users because our revenue is highly influenced by the number of people using our apps.
# 
# To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:
# 
# 1. Build a minimal Android version of the app, and add it to Google Play.
# 2. If the app has a good response from users, we develop it further.
# 3. If the app is profitable after six months, we build an iOS version of the app and add it to the App Store.
# 
# Because our end goal is to add the app on both the App Store and Google Play, we need to find app profiles that are successful on both markets. For instance, a profile that might work well for both markets might be a productivity app that makes use of gamification.
# 
# Let's begin the analysis by getting a sense of the most common genres for each market. For this, we'll build a frequency table for the prime_genre column of the App Store data set, and the Genres and Category columns of the Google Play data set.

# ## Part Two
# We'll build two functions we can use to analyze the frequency tables:
# 
# 1. One function to generate frequency tables that show percentages
# 2. Another function that we can use to display the percentages in a descending order

# In[67]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
            
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage
    
    return table_percentages

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
    


# In[69]:


display_table(ios_final,-5) # Prime_genre


# We can see that among the free English apps, more than a half (58.16%) are games. Entertainment apps are close to 8%, followed by photo and video apps, which are close to 5%. Only 3.66% of the apps are designed for education, followed by social networking apps which amount for 3.29% of the apps in our data set.
# 
# The general impression is that App Store (at least the part containing free English apps) is dominated by apps that are designed for fun (games, entertainment, photo and video, social networking, sports, music, etc.), while apps with practical purposes (education, shopping, utilities, productivity, lifestyle, etc.) are more rare. However, the fact that fun apps are the most numerous doesn't also imply that they also have the greatest number of users — the demand might not be the same as the offer.
# 
# Let's continue by examining the Genres and Category columns of the Google Play data set (two columns which seem to be related).

# In[71]:


display_table(android_final, 1) # Category


# There are not that many apps designed for fun, and it seems that a good number of apps are designed for practical purposes (family, tools, business, lifestyle, productivity, etc.). However, if we investigate this further, we can see that the family category (which accounts for almost 19% of the apps) means mostly games for kids.
# 
# ![image.png](attachment:image.png)

# In[72]:


display_table(android_final, -4) # Genre


# The difference between the Genres and the Category columns is not crystal clear, but one thing we can notice is that the Genres column is much more granular. We're only looking for the bigger picture at the moment, so we'll only work with the Category column moving forward.
# 
# Up to this point, we found that the App Store is dominated by apps designed for fun, while Google Play shows a more balanced landscape of both practical and for-fun apps. Now we'd like to get an idea about the kind of apps that have most users.

# ## Most Popular Apps by Genre on the App Store
# One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play data set, we can find this information in the Installs column, but for the App Store data set this information is missing. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the rating_count_tot app.
# 
# Below, we calculate the average number of user ratings per app genre on the App Store:

# In[80]:


genres_ios = freq_table(ios_final, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:            
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)


# On average, **navigation apps** have the highest number of user reviews, but this figure is heavily influenced by Waze and Google Maps, which have close to half a million user reviews together:

# In[81]:


for app in ios_final:
    if app[-5] == 'Navigation':
        print(app[1],':',app[5])


# The same pattern applies to social networking apps, where the average number is heavily influenced by a few giants like Facebook, Pinterest, Skype, etc. Same applies to music apps, where a few big players like Pandora, Spotify, and Shazam heavily influence the average number.
# 
# Our aim is to find popular genres, but navigation, social networking or music apps might seem more popular than they really are. The average number of ratings seem to be skewed by very few apps which have hundreds of thousands of user ratings, while the other apps may struggle to get past the 10,000 threshold. We could get a better picture by removing these extremely popular apps for each genre and then rework the averages, but we'll leave this level of detail for later.
# 
# Reference apps have 74,942 user ratings on average, but it's actually the Bible and Dictionary.com which skew up the average rating:

# In[82]:


for app in ios_final:
    if app[-5] == 'Reference':
        print(app[1],':',app[5])


# However, this niche seems to show some potential. One thing we could do is take another popular book and turn it into an app where we could add different features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes about the book, etc. On top of that, we could also embed a dictionary within the app, so users don't need to exit our app to look up words in an external app.
# 
# This idea seems to fit well with the fact that the App Store is dominated by for-fun apps. This suggests the market might be a bit saturated with for-fun apps, which means a practical app might have more of a chance to stand out among the huge number of apps on the App Store.
# 
# Other genres that seem popular include weather, book, food and drink, or finance. The book genre seem to overlap a bit with the app idea we described above, but the other genres don't seem too interesting to us:
# 
# - Weather apps — people generally don't spend too much time in-app, and the chances of making profit from in-app adds are low. Also, getting reliable live weather data may require us to connect our apps to non-free APIs.
# 
# - Food and drink — examples here include Starbucks, Dunkin' Donuts, McDonald's, etc. So making a popular food and drink app requires actual cooking and a delivery service, which is outside the scope of our company.
# 
# - Finance apps — these apps involve banking, paying bills, money transfer, etc. Building a finance app requires domain knowledge, and we don't want to hire a finance expert just to build an app.
# 
# Now let's analyze the Google Play market a bit.

# ## Most Popular Apps by Genre on Google Play
# For the Google Play market, we actually have data about the number of installs, so we should be able to get a clearer picture about genre popularity. However, the install numbers don't seem precise enough — we can see that most values are open-ended (100+, 1,000+, 5,000+, etc.):

# In[83]:


display_table(android_final, 5)


# One problem with this data is that is not precise. For instance, we don't know whether an app with 100,000+ installs has 100,000 installs, 200,000, or 350,000. However, we don't need very precise data for our purposes — we only want to get an idea which app genres attract the most users, and we don't need perfect precision with respect to the number of users.
# 
# We're going to leave the numbers as they are, which means that we'll consider that an app with 100,000+ installs has 100,000 installs, and an app with 1,000,000+ installs has 1,000,000 installs, and so on.
# 
# To perform computations, however, we'll need to convert each install number to float — this means that we need to remove the commas and the plus characters, otherwise the conversion will fail and raise an error.

# In[84]:


categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:
            n_installs = app[5]
            n_installs = n_installs.replace(',','')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# On average, communication apps have the most installs: 38,456,119. This number is heavily skewed up by a few apps that have over one billion installs (WhatsApp, Facebook Messenger, Skype, Google Chrome, Gmail, and Hangouts), and a few others with over 100 and 500 million installs:

# In[86]:


for app in android_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+' or app[5] == '500,000,000+' or app[5] == '100,000,000+'):
        print(app[0],':',app[5])


# If we removed all the communication apps that have over 100 million installs, the average would be reduced roughly ten times:

# In[87]:


under_100_m = []

for app in android_final:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 100000000):
        under_100_m.append(float(n_installs))
sum(under_100_m) / len(under_100_m)


# We see the same pattern for the video players category, which is the runner-up with 24,727,872 installs. The market is dominated by apps like Youtube, Google Play Movies & TV, or MX Player. The pattern is repeated for social apps (where we have giants like Facebook, Instagram, Google+, etc.), photography apps (Google Photos and other popular photo editors), or productivity apps (Microsoft Word, Dropbox, Google Calendar, Evernote, etc.).
# 
# Again, the main concern is that these app genres might seem more popular than they really are. Moreover, these niches seem to be dominated by a few giants who are hard to compete against.
# 
# The game genre seems pretty popular, but previously we found out this part of the market seems a bit saturated, so we'd like to come up with a different app recommendation if possible.
# 
# The books and reference genre looks fairly popular as well, with an average number of installs of 8,767,811. It's interesting to explore this in more depth, since we found this genre has some potential to work well on the App Store, and our aim is to recommend an app genre that shows potential for being profitable on both the App Store and Google Play.
# 
# Let's take a look at some of the apps from this genre and their number of installs:

# In[88]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0],':',app[5])


# The book and reference genre includes a variety of apps: software for processing and reading ebooks, various collections of libraries, dictionaries, tutorials on programming or languages, etc. It seems there's still a small number of extremely popular apps that skew the average:

# In[89]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# However, it looks like there are only a few very popular apps, so this market still shows potential. Let's try to get some app ideas based on the kind of apps that are somewhere in the middle in terms of popularity (between 1,000,000 and 100,000,000 downloads):

# In[90]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])


# This niche seems to be dominated by software for processing and reading ebooks, as well as various collections of libraries and dictionaries, so it's probably not a good idea to build similar apps since there'll be some significant competition.
# 
# We also notice there are quite a few apps built around the book Quran, which suggests that building an app around a popular book can be profitable. It seems that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets.
# 
# However, it looks like the market is already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.
# 
# ## Conclusions
# In this project, we analyzed data about the App Store and Google Play mobile apps with the goal of recommending an app profile that can be profitable for both markets.
# 
# We concluded that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets. The markets are already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.
