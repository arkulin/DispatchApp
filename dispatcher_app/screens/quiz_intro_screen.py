from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ListProperty, StringProperty
import json
import os
import random


class QuizIntroScreen(Screen):
    """Intro screen allowing the user to choose how many questions to take."""

    total_questions = NumericProperty(0)
    module_names = ListProperty()
    selected_module = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
        with open(file_path, 'r') as f:
            self.module_questions = json.load(f)
        self.module_names = list(self.module_questions.keys())
        if self.module_names:
            self.selected_module = self.module_names[0]
            self.total_questions = len(self.module_questions[self.selected_module])

    def start_quiz(self, *_):
        num_str = self.ids.num_input.text
        if not num_str:
            return
        num = int(num_str)
        if num <= 0:
            return
        questions = self.module_questions[self.selected_module]
        num = min(num, len(questions))
        # Randomize the order of questions for each quiz run
        selected = random.sample(questions, num)
        quiz_screen = self.manager.get_screen('quiz')
        quiz_screen.setup_quiz(selected)
        self.manager.current = 'quiz'

    def on_module_select(self, module):
        self.selected_module = module
        self.total_questions = len(self.module_questions[module])

    def go_home(self, *_):
        self.manager.current = 'quiz_intro'
