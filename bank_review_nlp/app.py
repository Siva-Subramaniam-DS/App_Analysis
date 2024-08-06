from flask import Flask, request, jsonify, render_template
from sentiment_analyzer import SentimentAnalyzer


app = Flask(__name__)

sentiment_analyzer = SentimentAnalyzer()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        #posted_text = request.form.get('posted_text')
        feedbacks=sentiment_analyzer.get_feedbacks()
        #feedbacks=["this is bad app","I never used such worst app","I never used good app","Neutral"]
        preprocessed_text=sentiment_analyzer.preprocess_text(feedbacks)
        print(preprocessed_text)
        sentiment_val=[]
        for individual_text in preprocessed_text:
            sentiment = sentiment_analyzer.get_sentiment(individual_text) 
            sentiment_val.append(sentiment)
        analysis_result=sentiment_analyzer.get_overall_feedback(sentiment_val)
        
        positive_count=analysis_result["PositiveFeedbackCount"]
        negative_count=analysis_result["NegativeFeedbackCount"]
        neutral_count=analysis_result["NeutralFeedbackCount"]
        img = ""
        
        if analysis_result["OverallFeedback"] == "positive":
            img = '<img src="static/images/positive.png" style="wdith:230px;height:230px;padding-bottom:30px;padding-left:50px" />'
        elif analysis_result["OverallFeedback"] == "negative":
            img = '<img src="static/images/negative.png" style="wdith:230px;height:230px;padding-bottom:30px;padding-left:50px"/>'
        else:
            img = '<img src="static/images/neutral.png" style="wdith:230px;height:230px;padding-bottom:30px;padding-left:50px"/>'
            
        plot_url =sentiment_analyzer.draw_pie_chart(positive_count,negative_count,neutral_count)
            
        

    return render_template('result.html', prediction=img,plot=plot_url,positive=positive_count,negative=negative_count,neutral=neutral_count)


if __name__ == '__main__':
    app.run(debug=True)
