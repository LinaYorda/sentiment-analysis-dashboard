from taipy.gui import Gui # Import State for newer Taipy versions
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from urllib.parse import urlparse
#from urllib.parse import urlpars
from dateutil import parser

data=pd.read_csv('data/articles_with_text_and_title_sentiment copy.csv')
specific_sources = ["welt.de", "bild.de", "sueddeutsche.de"]

def map_url_to_source(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    for source in specific_sources:
        if source in domain:
            return source
    return None

# Apply the function to extract source from URL
data['Source'] = data['URL'].apply(map_url_to_source)
print("Unique sources in data:", data['Source'].unique())

print("Unique sources in data:", data['Source'].unique())

# Debugging: Print a sample of URLs to check their structure
print("Sample URLs:")
print(data['URL'].sample(10).values)

# Check if the mapping function is working correctly for 'spiegel.de'
spiegel_sample_urls = data[data['URL'].str.contains("spiegel.de")]['URL'].values
print("Sample spiegel.de URLs:")
print(spiegel_sample_urls)

# Debugging: Check the result of the mapping function
spiegel_mapped_sources = data[data['Source'] == 'spiegel.de']['URL'].values
print("Mapped spiegel.de URLs:")
print(spiegel_mapped_sources)

data = data[data['Source'].notnull()]

print("Publish dates (head):")
print(data['PublishDate'].head())


print("Publish dates after conversion (head):")
print(data['PublishDate'].head())

data['PublishDate'] = pd.to_datetime(data['PublishDate'], errors='coerce')

data = data[data['PublishDate'].notna()]

print("spiegel.de data after date filtering:")
spiegel_data_after_date_filtering = data[data['Source'] == 'spiegel.de']
print(spiegel_data_after_date_filtering.head())

start_date = pd.Timestamp('2022-02-24')
end_date = pd.Timestamp('2023-02-24')
data = data[(data['PublishDate'] >= start_date) & (data['PublishDate'] <= end_date)]

# Debugging: Check "spiegel.de" data after full filtering
print("spiegel.de data after full filtering:")
spiegel_data_after_full_filtering = data[data['Source'] == 'spiegel.de']
print(spiegel_data_after_full_filtering.head())

data['Month'] = data['PublishDate'].dt.to_period('M').astype(str)


average_sentiment_scores = data.groupby(['Month', 'Source'])['TextSentimentScore'].mean().reset_index()
average_sentiment_scores.rename(columns={'TextSentimentScore': 'AverageTextSentimentScore'}, inplace=True)

article_counts = data.groupby(['Month', 'Source'])['URL'].count().reset_index()
article_counts.rename(columns={'URL': 'ArticleCount'}, inplace=True)

# Merge the calculated columns with the original data
data = pd.merge(data, average_sentiment_scores, on=['Month', 'Source'], how='left')
data = pd.merge(data, article_counts, on=['Month', 'Source'], how='left')



# Define the options for the dropdown selector
choice_button = ["All", "https://www.welt.de", "https://www.bild.de", "https://www.sueddeutsche.de"]
choice=""


#filtered_data = data[data['URL'].str.contains(choice)]
filtered_data = data if choice == "All" else data[data['URL'].str.contains(choice)]

print(filtered_data.head())



print("Sample data for spiegel.de before filtering:")
print(data[data['Source'] == 'spiegel.de'].head())


print(data.columns)
print(filtered_data.columns)

def toggle_table_dialog(state):
    print("Attempting to toggle show_table_dialog")
    if 'show_table_dialog' in state:
        state.show_table_dialog = not state.show_table_dialog
    else:
        state.show_table_dialog = True  # Safeguard to define if not exist
    print("Toggled state of dialog:", state.show_table_dialog)


# Function to handle initial app state
def on_start(state):
    print("Starting app.")   # Replace 'state' with 'app' for older Taipy versions
    state.show_table_dialog = False  # Initialize show_table_dialog as a property
    state.choice = choice_button[0]  # Set default if no previous selection
    state.filtered_data = data[data['URL'].str.contains(state.choice)]
    print(f"Filtered data on start for {state.choice}:\n{state.filtered_data}")

def update_choice(state, var_name, var_value):
    print(f"Updating choice to: {var_value}")
    state.choice = var_value
    #state.filtered_data = data[data['URL'].str.contains(state.choice)]
    state.filtered_data = data if var_value == "All" else data[data['URL'].str.contains(var_value)]

    #state.filtered_data = data[data['Source'] == state.choice]
    print(f"Filtered data updated for choice: {state.choice}")
    print(f"Filtered data updated for {state.choice}:\n{state.filtered_data}")
    print(data.columns)
    print(filtered_data.columns)

# Function to handle button click event to show the dialog


# Create the Taipy page
my_app_page = """
# <center> German Media Outlets during the first year of Russia-Ukraine war </center>

<|layout|columns= 6 6 |gap=1.9rem|

<|column_1|
## Choose a news source
<|{choice}|selector|lov={choice_button}|dropdown|on_change=update_choice|>


------------------------------

<|{show_table_dialog}|dialog|width=90vw|labels=Cancel|>
<center><|{filtered_data}|table|width=fit-content|height=65vh|></center>
|>

<|column_2|
**Chart 1:** Sentiment Scores by Text Sentiment
<|{filtered_data}|chart|type=bar|x=TextSentiment|y=TextSentimentScore|>



**Chart 2:** Sentiment Score of the Title of the Article
<|{filtered_data}|chart|type=pie|labels=TextSentiment|values=URL.count()|>


**Chart 3:** Relationship between Article Count and Sentiment Score
<|{filtered_data}|chart|mode=markers|x=ArticleCount|y=TextSentimentScore|size=ArticleCount|color=Source|>


**Chart 4:** Heatmap of Monthly Average Sentiment Scores
<|{filtered_data}|chart|type=heatmap|z=AverageTextSentimentScore|x=Month|y=Source|color=AverageTextSentimentScore|>
|>


|>
"""

if __name__ == '__main__':
    # Initialize and run the Taipy GUI
    gui = Gui(page=my_app_page)
    #gui.run(on_start=on_start, show_table_dialog=False, choice=choice_button[0], choice_button=choice_button, data=data)
    #gui.run(on_start=on_start)
    gui.run(on_start=on_start, toggle_table_dialog=toggle_table_dialog, update_choice=update_choice, dark_mode=False)
 
    