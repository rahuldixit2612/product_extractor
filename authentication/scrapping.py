import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re

def get_beautiful_soup_obj(url):
    """
    Creates a BeautifulSoup object from the HTML content of a given URL.
    
    Args:
        url (str): The URL to scrape.
        
    Returns:
        BeautifulSoup: A BeautifulSoup object representing the parsed HTML content.
    """
    response = requests.get(url)
    soup = None

    if response.status_code == 200:
        response_data = response.content
        soup = BeautifulSoup(response_data, 'html.parser')

    return soup

def get_div_only_classes_with_count_range(soup, min_count, max_count):
    """
    Extracts div elements with classes, filters them based on occurrence count,
    and returns a dictionary with class names, counts, and associated data.
    
    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML content.
        min_count (int): Minimum count of class occurrences to consider.
        max_count (int): Maximum count of class occurrences to consider.
        
    Returns:
        dict: A dictionary containing class names, counts, and associated data.
    """
    class_count_dict = defaultdict(lambda: {'count': 0, 'data': []})
    div_elements_with_classes = soup.find_all('div', class_=True)

    for element in div_elements_with_classes:
        classes = element.get('class')
        text = element.get_text()

        for class_name in classes:
            class_info = class_count_dict[class_name]
            class_info['count'] += 1
            
            if min_count <= class_info['count'] <= max_count:
                class_info['data'].append(text)
    
    div_only_classes_with_count_range = {
        class_name: {
            'count': class_info['count'],
            'data': class_info['data']
        }
        for class_name, class_info in class_count_dict.items()
        if min_count <= class_info['count'] <= max_count
    }

    return div_only_classes_with_count_range

def is_valid_data(data):
    """
    Checks if the provided data meets certain validity conditions.
    
    Args:
        data (str): The data to be validated.
        
    Returns:
        bool: True if the data is valid; False otherwise.
    """
    if len(data) < 20:
        return False
    
    # Check if data is vertical
    if all(line.strip() == "" for line in data.split('\n')):
        return False
    
    # Check if data contains only numbers and names
    data_words = re.findall(r'\b(?:\d+|[A-Za-z]+)\b', data)
    if len(data_words) == 0 or len(data_words) == len(data.split()):
        return False
    
    return True

def extract_data(url, min_count, max_count):
    """
    Extracts and filters data from the given URL's HTML content.
    
    Args:
        url (str): The URL to scrape.
        min_count (int): Minimum count of class occurrences to consider.
        max_count (int): Maximum count of class occurrences to consider.
        
    Returns:
        tuple: A tuple containing extracted data (list of strings) and the webpage title (str).
    """
    soup = get_beautiful_soup_obj(url)
    title = soup.title.string.strip() if soup.title else "No Title Found"
    div_only_classes_with_count_range = get_div_only_classes_with_count_range(soup, min_count, max_count)
    
    extracted_data = []
    for class_name, class_info in div_only_classes_with_count_range.items():
        filtered_data_list = [data for data in class_info['data'] if is_valid_data(data)]
        filtered_count = len(filtered_data_list)
        
        if filtered_count > 1:
            extracted_data.extend(filtered_data_list)
    
    return extracted_data, title

def store_data(output_filename, url, min_count, max_count):
    """
    Stores the extracted and filtered data along with the webpage title in a text file.
    
    Args:
        output_filename (str): The name of the output text file.
        url (str): The URL to scrape.
        min_count (int): Minimum count of class occurrences to consider.
        max_count (int): Maximum count of class occurrences to consider.
        
    Returns:
        bool: True if data was written successfully; False otherwise.
    """
    extracted_data, title = extract_data(url, min_count, max_count)
    success = False

    try:
        with open(output_filename, "w", encoding="utf-8") as output_file:
            output_file.write(f"Title - {title}\n\n")
            output_file.write("-" * 100 + "\n") 
            
            for data in extracted_data:
                output_file.write(f"*  {data}\n")
                output_file.write("-" * 100 + "\n")
            
            success = True
            print("Data written successfully!")
    except Exception as e:
        print(f"Exception occurred: {e}")
    
    return success