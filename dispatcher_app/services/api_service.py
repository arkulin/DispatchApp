"""
API Service for communicating with the backend server
"""
import json
try:
    from urllib import request, error
except ImportError:
    import urllib2 as request
    import urllib2 as error

from config import API_BASE_URL


class APIService:
    """Handles all API communications with the backend."""
    
    def __init__(self):
        self.base_url = API_BASE_URL
    
    def get_categories(self):
        """Fetch all question categories from the API."""
        try:
            url = f'{self.base_url}/api/v1/categories'
            req = request.Request(url)
            response = request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode('utf-8'))
            return data
        except Exception as e:
            print(f'API Error fetching categories: {e}')
            return None
    
    def get_questions_by_category(self, category_name):
        """Fetch questions for a specific category."""
        try:
            # URL encode the category name
            encoded_category = category_name.replace(' ', '%20')
            url = f'{self.base_url}/api/v1/questions/by-category/{encoded_category}'
            req = request.Request(url)
            response = request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode('utf-8'))
            return data
        except Exception as e:
            print(f'API Error fetching questions: {e}')
            return None
