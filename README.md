# Webpage Text Extraction API

This project focuses on designing an API endpoint that extracts text content from a given URL, processes the extracted data, and saves it into a document format. The API utilizes libraries such as BeautifulSoup and requests for webpage parsing.

## Objective

The primary goal of this project is to create an API endpoint that accepts a URL as input, fetches the HTML content of the webpage, extracts relevant text data, filters and processes the data, and finally, saves the processed text into a document.

## Requirements

The project is developed using the following libraries:
- Python
- requests
- BeautifulSoup
- django
- regex

## Key Components and Features

- **URL Input**: Users can provide the URL of the webpage they want to extract text from.
- **Webpage Parsing**: HTML content of the provided URL is fetched and parsed using BeautifulSoup.
- **Text Extraction**: Relevant text data is extracted from various HTML elements, excluding structural elements.
- **Text Filtering**: Extracted text can be filtered to remove unwanted content.
- **Document Creation**: Extracted and filtered text is saved into formats like TXT.
- **API Interface**: The endpoint is exposed as a RESTful API.

## Approach

1. URL input is provided to the API endpoint.
2. The HTML content is fetched using the `requests` library.
3. BeautifulSoup is used to parse the HTML and extract text data from 'div' and 'class' elements.
4. Text data is processed to filter out unnecessary content.
5. Text summarization models can be used to generate abstractive product summaries if needed (tried using Hugging Face's transformers).
6. Created functions to validate the data and remove unnecessary text.

## Getting Started

1. Clone this repository to your local machine.
2. Create a virtual environment and activate it.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Run the API using the appropriate command.

## Usage

1. Start the API.
2. Send a POST request to the endpoint with the URL as input.
3. The API will fetch the webpage, extract, process, and save the text data.

## API Documentation

- **Endpoint**: `/extract-text`
- **Server URL**: http://127.0.0.1:8000/extract-data/
- **Method**: POST
- **Request Body Format**: JSON object with the following format:
    ```json
    {
        "webpage_url": "webpage_url",
        "min_count": min_count,
        "max_count": max_count,
        "output_filename": "output_filename"
    }
    ```
- **Response Format**: JSON object with the following format:
    ```json
    {
        "success": true,
        "message": "Output saved to a.txt",
        "file_path": "D:\\tenali\\tenali_API\\a.txt"
    }
    ```

## Challenges Faced

1. Scraping and text extraction in a specific format can't be generalized to all webpages as different webpages have different HTML formats.

2. Writing generalized functions to clean the extracted text is challenging due to the varying text content and its importance on different products.

## Improvements Can Be Done

1. If the product website is known beforehand, a more robust parser can be developed to extract text with higher accuracy.

2. NLP models capable of finding different entities such as product names and prices can be used to improve the quality of the extracted text.

## Unit Testing

1. Used Django unit testing to validate POST requests to the API.

## Examples of Tested URLs

- https://www.flipkart.com/q/best-laptops-under-rs-50000
- https://www.tractorjunction.com/all-brands/
- https://www.boat-lifestyle.com/products/boat-storm-smartwatch
- https://www.boat-lifestyle.com/collections/true-wireless-earbuds
- https://www.apple.com/in/shop/buy-iphone
- https://www.bookstation.in/?gclid=CjwKCAjwloynBhBbEiwAGY25dB2ilncCUEtgCwb9ETS57xcNUlJUb3RcZNi8dl-F-SEIxvSHCSyJsRoCAUwQAvD_BwE
