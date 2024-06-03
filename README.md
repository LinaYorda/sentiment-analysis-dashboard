# Sentiment Analysis Dashboard on German Media Outlets(24.02.2022 - 24.02.2023)

This project analyzes the sentiment of articles from German news outlets during the first year of the Russia-Ukraine war. The application allows users to select different news sources and visualize sentiment scores through various charts. A table with articles from the following media websites is included: Der Spiegel, Die Welt, Bild, and Süddeutsche Zeitung. [Taipy](https://taipy.io) is used for building the interactive dashboard. 


![Demo](giphy.gif)



## Source

For this project, I used the library created by Lukas Trippe that scrapes the data from six different German news outlets. Here is the link for the Python library: [newspaper-scraper](https://pypi.org/project/newspaper-scraper/).


## Sentiment Analysis 

The BERT model used in this project is the "oliverguhr/german-sentiment-bert", a pre-trained model fine-tuned specifically for sentiment analysis on German texts. 

The "oliverguhr/german-sentiment-bert" model is further fine-tuned on a specific dataset for sentiment analysis. Fine-tuning involves training the model on labeled data where each text is associated with a sentiment label (e.g., positive, negative, neutral). This process adjusts the model’s weights to optimize its performance on the sentiment analysis task.

For each input text, the model outputs a sentiment label (e.g., "positive", "negative", "neutral") and a confidence score indicating the model's certainty about its prediction. Below it the code, I used:

```python

sentiment_pipeline = pipeline("sentiment-analysis", model="oliverguhr/german-sentiment-bert")

# Function to analyze sentiment
def analyze_sentiment(text):
    try:
        result = sentiment_pipeline(text[:512])  # BERT models typically have a max token limit, so truncating long texts
        return result[0]['label'], result[0]['score']
    except:
        return "Error", 0.0

cleaned_articles['TextSentiment'], cleaned_articles['TextSentimentScore'] = zip(*cleaned_articles['Text'].map(analyze_sentiment))
cleaned_articles['TitleSentiment'], cleaned_articles['TitleSentimentScore'] = zip(*cleaned_articles['Title'].map(analyze_sentiment))
```


## How to Use This Repository

You can run the application locally by following the installation steps above. Once the application is running, you can interact with the Taipy dashboard to explore sentiment analysis data from various German media outlets.

### Modifying the Code

Feel free to modify the code according to your needs. The main parts of the application include:

* Visualization: The Taipy dashboard provides interactive visualizations.
* Customization: You can add more visualizations or change the existing ones based on your requirements.

To make changes, simply edit the Python files and restart the application to see your changes in effect.


## Installation

To run this sentiment analysis project locally and visualize the results through the Taipy dashboard, follow these steps:


### Prerequisites

- Python 3.7+
- `pip` (Python package installer)


### Clone the Repository

```bash
git clone https://github.com/LinaYorda/sentiment-analysis-dashboard.git
cd sentiment-analysis-dashboard
```

### Create and Activate a Virtual Environment

 ```bash
python -m venv venv
source venv/bin/activate  
 ```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start the Application

```bash
python main.py
```

This will start the Taipy dashboard. Open your web browser and navigate to the address provided in the terminal (usually http://localhost:5000)



### Features

- Sentiment analysis of article texts and titles.
- Visualizations include bar charts, pie charts, scatter plots, and heatmaps.
- Interactive selection of news sources.