import requests

def extract_data_from_webpage(webpage_url, min_count, max_count, output_filename):
    """
    Extracts data from a specified webpage and saves it to a file.

    Args:
        webpage_url (str): The URL of the webpage from which to extract data.
        min_count (int): The minimum count of data to extract.
        max_count (int): The maximum count of data to extract.
        output_filename (str): The name of the file to which the extracted data will be saved.

    Returns:
        str: A message indicating the status of the extraction process.
    """
    url = "http://127.0.0.1:8000/extract-data/"  # Replace with your server URL
    data = {
        "webpage_url": webpage_url,
        "min_count": min_count,
        "max_count": max_count,
        "output_filename": output_filename
    }

    response = requests.post(url, data=data)

    return response.text

if __name__ == "__main__":
    webpage_url = "https://www.flipkart.com/q/best-laptops-under-rs-50000"
    min_count = 10
    max_count = 30
    output_filename = "output.txt"

    extraction_result = extract_data_from_webpage(webpage_url, min_count, max_count, output_filename)
    print("Extraction Result:", extraction_result)
