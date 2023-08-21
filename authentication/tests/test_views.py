from django.test import TestCase
from django.test import Client
from django.urls import reverse

class MyViewTestCase(TestCase):
    def setUp(self):
        """
        Set up the test environment before running each test method.
        """
        self.client = Client()
        
    def test_valid_post_request(self):
        """
        Test a valid POST request to the 'extract_data' view.
        """
        post_data = {
            "webpage_url": "https://www.flipkart.com/q/best-laptops-under-rs-50000",
            "min_count": 10,
            "max_count": 30,
            "output_filename": "output.txt"
        }
        response = self.client.post(reverse('extract_data'), data=post_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "success": True,
            "message": "Output saved to output.txt",
            "file_path": "D:\\tenali\\tenali_API\\output.txt"
        })
    
    def test_invalid_request_method(self):
        """
        Test an invalid request method (GET) to the 'extract_data' view.
        """
        response = self.client.get(reverse('extract_data'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"error": "Invalid request method"})

    # You can add more test methods for other scenarios
    
    # You can include a tearDown method to clean up files or resources if necessary.
