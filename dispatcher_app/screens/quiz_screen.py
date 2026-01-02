from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.utils import get_color_from_hex
import json
import os


class QuizScreen(Screen):
    """Quiz screen that loads questions and options dynamically."""
    
    question_text = StringProperty('')
    progress_text = StringProperty('')
    feedback_text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
        with open(file_path, 'r') as f:
            self.all_questions = json.load(f)
        self.questions = []
        self.current_index = 0
        self.option_buttons = []
        self.selected_index = None
        self.correct_count = 0
        self.answered = False

    def setup_quiz(self, questions):
        """Initialize quiz with a subset of questions."""
        self.questions = questions
        self.current_index = 0
        self.correct_count = 0
        self.option_buttons = []
        self.ids.options_box.clear_widgets()
        self.selected_index = None
        self.answered = False
        self._load_question()

    def _load_question(self):
        """Populate widgets with the current question."""
        q = self.questions[self.current_index]
        
        # Update progress
        self.progress_text = f'Question {self.current_index + 1} of {len(self.questions)}'
        
        # Update question text
        self.question_text = q['question']
        
        # Clear previous options
        self.ids.options_box.clear_widgets()
        self.option_buttons = []
        
        # Create option buttons with proper sizing
        for i, option in enumerate(q['options']):
            btn = Button(
                text=option,
                size_hint_y=None,
                height=80,
                font_size='16sp',
                text_size=(None, None),
                halign='left',
                valign='middle',
                padding=(15, 10),
                background_normal='',
                background_color=[0.9, 0.9, 0.9, 1]
            )
            btn.bind(size=self._update_button_text_size)
            btn.bind(on_press=lambda inst, idx=i: self.select_option(idx))
            self.option_buttons.append(btn)
            self.ids.options_box.add_widget(btn)
        
        self.feedback_text = ''
        self.selected_index = None
        self.ids.next_button.text = 'Finish Quiz' if self.current_index == len(self.questions) - 1 else 'Next Question'

    def _update_button_text_size(self, button, size):
        """Update button text_size to enable text wrapping."""
        button.text_size = (size[0] - 30, None)

    def select_option(self, index):
        """Handle option selection."""
        if self.answered:
            return
        self.selected_index = index
        self.feedback_text = ''
        for i, btn in enumerate(self.option_buttons):
            if i == index:
                btn.background_color = [0.4, 0.6, 1.0, 1]
            else:
                btn.background_color = [0.9, 0.9, 0.9, 1]

    def check_answer(self, *_):
        """Check if the selected answer is correct."""
        if self.selected_index is None:
            self.feedback_text = 'Please select an answer first!'
            return
        if self.answered:
            return
            
        correct_index = self.questions[self.current_index]['answer_index']
        
        if self.selected_index == correct_index:
            self.correct_count += 1
            self.feedback_text = '✓ Correct!'
            self.ids.feedback_label.color = [0.2, 0.7, 0.2, 1]
        else:
            self.feedback_text = '✗ Incorrect'
            self.ids.feedback_label.color = [0.9, 0.2, 0.2, 1]
        
        # Highlight correct answer
        for i, btn in enumerate(self.option_buttons):
            if i == correct_index:
                btn.background_color = [0.4, 0.8, 0.4, 1]
            elif i == self.selected_index and i != correct_index:
                btn.background_color = [0.9, 0.4, 0.4, 1]
        
        self.answered = True

    def next_question(self, *_):
        """Move to the next question or show results."""
        if not self.answered:
            self.check_answer()
            return
            
        self.current_index += 1
        if self.current_index < len(self.questions):
            self.answered = False
            self._load_question()
        else:
            result = self.manager.get_screen('quiz_result')
            result.set_result(self.correct_count, len(self.questions))
            self.manager.current = 'quiz_result'

    def go_home(self, *_):
        """Return to home screen."""
        self.manager.current = 'home'
