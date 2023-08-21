import os
from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse

class MyViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_post_request(self):
        """
        Test the view for a valid POST request.
        """
        response = self.client.post(reverse('extract_data'))
        
        # Assert that the response status code is 200 (OK).
        self.assertEqual(response.status_code, 200)
        
        # Assert the JSON response content matches the expected values.
        self.assertEqual(response.json(), {
            "message": "Output saved to output.txt",
            "file_path": os.path.abspath("output.txt")
        })
    
    def test_invalid_request_method(self):
        """
        Test the view for an invalid request method (GET instead of POST).
        """
        response = self.client.get(reverse('extract_data'))
        
        # Assert that the response status code is 405 (Method Not Allowed).
        self.assertEqual(response.status_code, 405)
        
        # Assert the JSON response content matches the expected error message.
        self.assertEqual(response.json(), {"error": "Invalid request method"})

   