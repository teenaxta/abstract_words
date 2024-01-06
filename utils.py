import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas as pd
import os

def get_paper_titles_and_urls(url: str) -> (list, list):
    """Get paper titles and urls given a link of the cvf conference page

    Args:
        url (str): url of the page

    Returns:
        list, list: list of titles, list of page urls 
    """
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all elements with the specified class containing titles
    titles = soup.find_all(class_='ptitle')

    paper_titles = []
    paper_links = []
    # Extract and print the titles
    for title in titles:
        paper_titles.append(title.get_text(strip=True))
        paper_links.append(title.find('a')['href'])  # Extract the href attribute value from the anchor tag

    return paper_titles, paper_links  
    
    

def get_paper_abstract(url: str) -> str:
    """Get the abstract of a paper

    Args:
        url (str): url of the paper page without openaccess.thecvf.com

    Returns:
        str: abstract scrapped from the page
    """

    url = 'https://openaccess.thecvf.com/' + url

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all elements with the specified class containing titles
    abstract = soup.find_all(id='abstract')
    abstract = abstract[0].text.replace('\n', '')

    return abstract

def get_word_count(text: str) -> list:
    """Get word count in text without stopwords 

    Args:
        text (str): any text

    Returns:
        list: a dictionary with word and their count
    """
    
    # nltk.download('punkt')
    # nltk.download('stopwords')

    stop_words = set(stopwords.words('english'))
    unique_words = [word.lower() for word in text if word.lower() not in stop_words and word.strip()]  # Filter out stopwords and get unique words

    word_counter = dict(Counter(unique_words))

    return word_counter

def compare_and_add_dicts(dict1: dict, dict2: dict) -> dict:
    """Compare and add dictionaries

    Args:
        dict1 (dict): 
        dict2 (dict): 

    Returns:
        dict: final dictionary after comparison and addition
    """
    
    for key, value in dict2.items():
        if key in dict1:
            dict1[key] += value
        else:
            dict1[key] = value

    return dict1

def get_conference_name(url: str) -> str:
    # Find the index of the last occurrence of '/'
    last_slash_index = url.rfind('/')

    # Get the substring after the last '/'
    substring = url[last_slash_index + 1:]

    # Find the index of '?' in the substring
    question_mark_index = substring.find('?')

    # Extract the part before '?' if '?' exists, otherwise, consider the whole substring
    if question_mark_index != -1:
        extracted_text = substring[:question_mark_index]
    else:
        extracted_text = substring

    # Extract 'ICCV' from the extracted text by iterating through characters
    result = ''
    for char in extracted_text:
        if char.isalpha():
            result += char
        else:
            break  # Stop when a non-alphabetic character is encountered
    return result

def merge_dataframes(df1, df2):

    # Merge dataframes to combine common fruits
    merged = pd.merge(df1, df2, on='Fruit', how='outer', suffixes=('_df1', '_df2'))

    # Replace NaN values with 0 for Count columns and add them together
    merged['Count'] = merged['Count_df1'].fillna(0) + merged['Count_df2'].fillna(0)

    # Drop unnecessary columns and reset index
    final_result = merged.drop(['Count_df1', 'Count_df2'], axis=1).reset_index(drop=True)

    return final_result

def make_csv_from_dict(dict1: dict, csv_path: str) -> None:
    dict1 = {
        'Words':list(dict1.keys()),
        'Counts':list(dict1.values())
    }
    
    if os.path.exists(csv_path):
        df1 = pd.read_csv(csv_path)
        df2 = pd.DataFrame(dict1)
        
        df1 = utils.merge_dataframes(title_df1, title_df2)        
    else:
        df1 = pd.DataFrame(dict1)

    df1.to_csv(csv_path, index=False)
        