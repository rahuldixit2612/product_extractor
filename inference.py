import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re

def get_div_only_classes_with_count_range(url, min_count, max_count):
    response = requests.get(url)

    if response.status_code == 200:
        response_data = response.content
        soup = BeautifulSoup(response_data, 'html.parser')

        title = soup.title.string.strip() if soup.title else "No Title Found"
        information = [("Title", title)]

        class_count_dict = defaultdict(lambda: {'count': 0, 'data': []})
        div_elements_with_classes = soup.find_all('div', class_=True)
        
        for element in div_elements_with_classes:
            classes = element.get('class')
            text = element.get_text()

            for class_name in classes:
                class_info = class_count_dict[class_name]
                class_info['count'] += 1
                if class_info['count'] >= min_count and class_info['count'] <= max_count:
                    class_info['data'].append(text)
        
        div_only_classes_with_count_range = {
            class_name: {
                'count': class_info['count'],
                'data': class_info['data']
            } for class_name, class_info in class_count_dict.items()
            if min_count <= class_info['count'] <= max_count
        }
        
        return information, div_only_classes_with_count_range

def is_valid_data(data):
    if len(data) < 20:
        return False
    
    if all(line.strip() == "" for line in data.split('\n')):
        return False
    
    data_words = re.findall(r'\b(?:\d+|[A-Za-z]+)\b', data)
    if len(data_words) == 0 or len(data_words) == len(data.split()):
        return False
    
    return True
