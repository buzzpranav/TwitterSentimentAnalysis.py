'''
This code is used to take input of a query, such as bitcoin, 
and then analyzes a specified amount of tweets by the user.
It then uses matplotlib to plot a pie chart based on the sentiment of the tweets
'''
#time module is imported for time related commands
import time
#tweepy module is import for API connection and taking tweets from twitter
import tweepy
#csv module is imported to output the tweets to results.csv for verification
import csv
#re module is imported for string related commands such as cleaning the tweets of links for more accurate analysis
import re
#matplotlib.pyplot module is imported to create a pie chart
import matplotlib.pyplot as plt
#textblob module is imported for the sentiment analysis
from textblob import TextBlob

#creates a class called SentimentAnalysis for project execution
class SentimentAnalysis:
 
    #initiates 2 lists for the tweet texts
    def __init__(self):
        self.tweets = []
        self.tweetText = []

    #creates the function for authentication and analysation
    def TweetDataStream(self):
        
        #The accesstoken and consumer information is stores here. A Public Key and Secret is used below.
        consumerKey = "xxxxxxx" 
        consumerSecret = "xxxxxxx" 
        accessToken = "xxxxxxx" 
        accessTokenSecret = "xxxxxxx"
        
        while (consumerKey == "xxxxxxx") or (consumerSecret == "xxxxxxx") or (accessToken == "xxxxxxx") or (accessTokenSecret == "xxxxxxx"):
            print("Invalid Twitter API credentials. Please add your credentials on line 31 of analyzer.py and restart the program")
            time.sleep(10)

        #uses tweepy to use the above AccessToken information to connect to twitter 
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        #takes an input of what to search about, and how many tweets to analyze
        searchTerm = input("Enter Keyword/Tag to search about: ")
        NoOfTerms = int(input("Enter how many tweets to search: "))

        #tweepy searches for all related tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en", result_type='popular').items(NoOfTerms)

        #sets the sentiment polarity to 0 before analyzing
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0
        total_impact = 0
        i = 0
        
        #uses the tweets taken by tweepy to start analysing with textblob
        for tweet in self.tweets:
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity
            impact = tweet.favorite_count
            
            print(str(i) + " out of " + str(NoOfTerms) + " Tweets Analyzed..." )
            i = i + 1
            if i == NoOfTerms:
                print("Analysis Complete") 
            
            total_impact += impact
            #if the sentiment is 0, a tally is added to neutral
            if (analysis.sentiment.polarity == 0):
                neutral += (1 + int(impact))
            #if the sentiment is 0-0.3, a tally is added to wpostive (weak positive)
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += (1 + int(impact))
            #if the sentiment is 0.3-0.6, a tally is added to postive
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += (1 + int(impact))
            #if the sentiment is 0.6-1, a tally is added to spostive (strong positive)
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += (1 + int(impact))
            #if the sentiment is -0.3 to 0, a tally is added to wnegative (weak negative)
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += (1 + int(impact))
            #if the sentiment is -0.6 to -0.3, a tally is added to negative
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += (1 + int(impact))
            #if the sentiment is -1 to -0.6, a tally is added to snegative (strong negative)
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += (1 + int(impact))
            #print(snegative, negative, wnegative, neutral, wpositive, positive, spositive)
            

        #uses previous sentiment and number of tweets to get a percentage of each
        positive = self.percentage(positive, total_impact)
        wpositive = self.percentage(wpositive, total_impact)
        spositive = self.percentage(spositive, total_impact)
        negative = self.percentage(negative, total_impact)
        wnegative = self.percentage(wnegative, total_impact)
        snegative = self.percentage(snegative, total_impact)
        neutral = self.percentage(neutral, total_impact)

        polarity = polarity / total_impact

        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")

        #uses the previous percentages to set polarity
        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 0.3):
            print("Weakly Positive")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")

        #outputs detailed text report
        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")
        if float(neutral) > 30:
            print("High neutrality rate could be caused by Unbiased News Sources")
        #outputs detailed pie chart report
        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)

    #cleans the tweet ok special charectars
    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    #creates a funcitom to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    #all information for the pie chart
    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('sentiment.png')
        plt.show()


if __name__== "__main__":
    
    sa = SentimentAnalysis()
    sa.TweetDataStream()
