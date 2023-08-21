from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os

from scrapping import store_data  # Make sure to import the correct module

@csrf_exempt
def extract_data(request):
    """
    Extracts data from a specified webpage URL, processes it, and stores the output.

    This view function handles a POST request containing the following parameters:
    - webpage_url (str): The URL of the webpage to extract data from.
    - min_count (int, optional): The minimum count of data elements to extract (default: 10).
    - max_count (int, optional): The maximum count of data elements to extract (default: 30).
    - output_filename (str): The filename to save the extracted data.

    Args:
        request (HttpRequest): The HTTP request object containing the POST parameters.

    Returns:
        JsonResponse: A JSON response containing the status of the extraction process.
            - If successful:
                - success (bool): True
                - message (str): A success message
                - file_path (str): Absolute path to the saved output file
            - If unsuccessful:
                - success (bool): False
                - message (str): A failure message
                - file_path (None)

    Notes:
        - This view function is CSRF exempt.
        - The 'store_data' function must be defined in the 'scrapping' module.

    Example POST data:
    {
        "webpage_url": "https://example.com",
        "min_count": 5,
        "max_count": 20,
        "output_filename": "output_data.json"
    }
    """

    if request.method == "POST":
        data = request.POST
        webpage_url = data.get('webpage_url')
        min_count = int(data.get('min_count', 10))
        max_count = int(data.get('max_count', 30))
        output_filename = data.get("output_filename")
        
        success = store_data(output_filename, webpage_url, min_count, max_count)

        if success:
            response_data = {
                "success": success,
                "message": "Output saved to " + output_filename,
                "file_path": os.path.abspath(output_filename)
            }
        else:
            response_data = {
                "success": success,
                "message": "Request failed",
                "file_path": None
            }
        return JsonResponse(response_data)

    else:
        return JsonResponse({"error": "Invalid request method"})
