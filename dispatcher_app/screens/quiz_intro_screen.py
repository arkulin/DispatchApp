from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ListProperty, StringProperty
import sys
import os
import random

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from services.data_manager import DataManager
except ImportError:
    # Fallback if import fails
    import json
    class DataManager:
        def __init__(self):
            file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
            with open(file_path, 'r') as f:
                self.local_questions = json.load(f)
        def get_categories(self):
            return list(self.local_questions.keys())
        def get_questions(self, category):
            return self.local_questions.get(category, [])


class QuizIntroScreen(Screen):
    """Intro screen allowing the user to choose how many questions to take."""

    total_questions = NumericProperty(0)
    module_names = ListProperty()
    selected_module = StringProperty('')
    summary_text = StringProperty('📚 Select a Module')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = DataManager()
        self.module_questions = {}
        self._load_modules()

    def _load_modules(self):
        """Load available modules/categories."""
        try:
            self.module_names = self.data_manager.get_categories()
            if self.module_names:
                self.selected_module = self.module_names[0]
                questions = self.data_manager.get_questions(self.selected_module)
                self.module_questions[self.selected_module] = questions
                self.total_questions = len(questions)
        except Exception as e:
            print(f'Error loading modules: {e}')
            self.summary_text = 'Error loading questions'

    def start_quiz(self, *_):
        """Start the quiz with selected number of questions."""
        num_str = self.ids.num_input.text
        if not num_str:
            return
        num = int(num_str)
        if num <= 0:
            return
        
        # Load questions for selected module if not already loaded
        if self.selected_module not in self.module_questions:
            questions = self.data_manager.get_questions(self.selected_module)
            self.module_questions[self.selected_module] = questions
        
        questions = self.module_questions[self.selected_module]
        num = min(num, len(questions))
        
        # Randomize the order of questions for each quiz run
        selected = random.sample(questions, num)
        quiz_screen = self.manager.get_screen('quiz')
        quiz_screen.setup_quiz(selected)
        self.manager.current = 'quiz'

    def on_module_select(self, module):
        """Handle module selection change."""
        self.selected_module = module
        
        # Load questions for this module if not already loaded
        if module not in self.module_questions:
            questions = self.data_manager.get_questions(module)
            self.module_questions[module] = questions
        
        self.total_questions = len(self.module_questions[module])

    def go_home(self, *_):
        """Return to home screen."""
        self.manager.current = 'home'
