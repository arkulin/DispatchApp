"""
Data Manager that handles both API and local JSON data
"""
import json
import os
from services.api_service import APIService
from config import API_ENABLED


class DataManager:
    """Manages data loading from API or local files."""
    
    def __init__(self):
        self.api_service = APIService() if API_ENABLED else None
        self.local_questions = self._load_local_questions()
    
    def _load_local_questions(self):
        """Load questions from local JSON file as fallback."""
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f'Error loading local questions: {e}')
            return {}
    
    def get_categories(self):
        """Get list of available categories."""
        if self.api_service and API_ENABLED:
            categories = self.api_service.get_categories()
            if categories:
                return [cat['name'] for cat in categories]
        
        # Fallback to local data
        return list(self.local_questions.keys())
    
    def get_questions(self, category):
        """Get questions for a specific category."""
        if self.api_service and API_ENABLED:
            questions = self.api_service.get_questions_by_category(category)
            if questions:
                return self._convert_api_format(questions)
        
        # Fallback to local data
        return self.local_questions.get(category, [])
    
    def _convert_api_format(self, api_questions):
        """Convert API question format to app format."""
        converted = []
        for q in api_questions:
            converted.append({
                'question': q['question_text'],
                'options': q['options'],
                'answer_index': q['correct_answer'],
                'explanation': q.get('explanation', '')
            })
        return converted
