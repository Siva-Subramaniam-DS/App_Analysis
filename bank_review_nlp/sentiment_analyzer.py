from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import io
import base64
import matplotlib.pyplot as plt

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from nltk.stem import PorterStemmer



from textblob import TextBlob

class SentimentAnalyzer:
    def __init__(self):
        pass

    def get_sentiment(self, processed_text):
        analysis = TextBlob(processed_text)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    
    def get_feedbacks(self):
        driver = webdriver.Chrome() 
        driver.get("https://play.google.com/store/games?device=windows&pli=1")
        driver.find_element("xpath", "//i[text()='search']").click()
        sleep(2)
        driver.find_element("xpath", "//input[@aria-label='Search Google Play']").send_keys("standard chartered bank")
        sleep(2)
        driver.find_element("xpath", "//b[text()='standard chartered bank']").click()
        sleep(2)
       # driver.find_element("xpath", "//div[@class='g1rdde']/..//../..//img[1]").click()
       # Locate the image element using XPath
        image_element = driver.find_element(By.XPATH, "//div[@class='g1rdde']/..//../../../../..//a")

        # Use JavaScript to click the element
        driver.execute_script("arguments[0].click();", image_element)
        sleep(2)
        driver.find_element("xpath", "//h2[text()='Ratings and reviews']/../..//i[text()='arrow_forward']").click()
        sleep(2)
        name=driver.find_elements("xpath", "//div[@role='dialog']//div[@class='RHo1pe']/div[1]")
        
        print(len(name))
        
        feedbacks=[]
        for individual_text in name:
           # print("--------------")
           # print(individual_text.text)
            individual_feedback=individual_text.text
           # print("--------------")
            individual_text.size
            feedbacks.append(individual_feedback)
        
       # print(feedbacks)
        print(len(feedbacks))
        driver.quit()
        
        return feedbacks
        
        
    
    def preprocess_text(self,review_text):
        
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        val=[]
        i=0
        for individual_text in review_text:
        
            i=i+1
           
            #print("**************TEXT PREPROCESSING IN NLP*****************")
            #print(i)
            #print("**************ORIGINAL TEXT*****************")
            #print(individual_text)
            
            # Step :1 Convert to Lowercase: Ensure uniformity by converting all text to lowercase.
            text=individual_text.lower()
        
            #Step :2 Remove URLs: Remove any URLs present in the text.
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
            #Step :3 Remove User References and Hashtags: Clean up the text by removing user mentions (e.g., @username) and hashtags.
            # Remove user @ references and '#'
            text = re.sub(r'\@\w+|\#', '', text)
        
            #Step :4 Remove Punctuation and Numbers: Strip out punctuation and numbers.
            text = re.sub(r'[^\w\s]', '', text)
        
            #Step :5 Remove Extra Whitespace: Clean up any extra whitespace for better tokenization.
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            #print("PREPROSSED TEXT")
            #print(text)
            
            #print("**************TOKINIZER*****************")
               
        
            #Step :6 Tokenize Text: Break the text into individual words.
            # Tokenize text import (from nltk.tokenize import word_tokenize)
            tokens = word_tokenize(text)
            #print(tokens)
        
            #Step :7 Remove Stopwords: Remove common words that don't add significant meaning (e.g., "the", "is").
            # Remove stopwords (from nltk.corpus import stopwords) 
            filtered_tokens = [word for word in tokens if word not in stop_words]
            #print("**********************FILTERED TOKEN AFTER STOP WATCH**************")
           # print(filtered_tokens)
        
            # Stem words
            #print("**********************STEMMING**************")
            stemmer = PorterStemmer()
            stemmed_words = [stemmer.stem(word) for word in tokens]
           # print(stemmed_words)
        
            #Step :8 Lemmatize Tokens: Reduce words to their base or root form (e.g., "running" to "run").
             # Lemmatize tokens
            lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
           # print("**********************LEMMATIZE**************")
          #  print(lemmatized_tokens)
        
            #Step :9 Join Tokens Back to String: Combine the tokens back into a single string for each text entry.
            # Join tokens back to string
            processed_text = ' '.join(lemmatized_tokens)
            #print("**********************ORIGINAL TEXT AFTER PREPROCESSING**************")
            #print(processed_text)
            val.append(processed_text)

        return val

    def get_overall_feedback(self,feedbacks):
        
        positive_count=0
        negative_count=0
        neutral_count=0
        print(feedbacks)
        for ind in feedbacks:
            if(ind.lower()=="positive"):
                positive_count=positive_count+1
            elif(ind.lower()=="negative"):
                negative_count=negative_count+1
            else:
                neutral_count=neutral_count+1
            
            #print(ind.lower())
            sentiment_val=""
            if(positive_count>negative_count and positive_count>neutral_count):
                sentiment_val="positive"        
            elif(negative_count>positive_count and negative_count>neutral_count):
                sentiment_val="negative"    
            elif(positive_count>negative_count):
                sentiment_val="negative"    
            else:
                sentiment_val="neutral"    
                
        #print(positive_count)
        #print(negative_count)
        #print(neutral_count)
        #print(sentiment_val)
        keys = ['PositiveFeedbackCount', 'NegativeFeedbackCount', 'NeutralFeedbackCount','OverallFeedback']
        values = [positive_count, negative_count, neutral_count,sentiment_val]

        my_dict = {}
        
        for key, value in zip(keys, values):
            my_dict[key] = value
        
        #print(my_dict)
        return my_dict
        
    def draw_pie_chart(self,positive_count,negative_count,neutral_count):
            
            labels = 'Positive', 'Negative', 'Neutral'
            sizes = [positive_count, negative_count, neutral_count]
            colors = ['gold', 'lightcoral', 'lightskyblue']
            explode = (0.1, 0, 0)  # explode 1st slice (Positive)

            fig, ax = plt.subplots()
            ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', shadow=True, startangle=140)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            #plt.title('Sentiment Analysis of Comments')

           
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode('utf8')
                    
            
            return plot_url