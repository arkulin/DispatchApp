from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
import json
import os


class QuizScreen(Screen):
    """Quiz screen that loads questions and options dynamically."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
        with open(file_path, 'r') as f:
            # File contains a dictionary of modules; keep for reference
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
        self.ids.question_label.text = q['question']
        self.ids.options_box.clear_widgets()
        self.option_buttons = []
        for i, option in enumerate(q['options']):
            btn = Button(text=option)
            btn.bind(on_press=lambda inst, idx=i: self.select_option(idx))
            self.option_buttons.append(btn)
            self.ids.options_box.add_widget(btn)
        self.ids.quiz_result.text = ''
        self.selected_index = None
        self.ids.next_button.text = 'Complete quiz' if self.current_index == len(self.questions) - 1 else 'Next'

    def select_option(self, index):
        self.selected_index = index
        self.ids.quiz_result.text = ''
        for i, btn in enumerate(self.option_buttons):
            if i == index:
                btn.background_color = get_color_from_hex('#90caf9')
            else:
                btn.background_color = [1, 1, 1, 1]

    def check_answer(self, *_):
        if self.selected_index is None or self.answered:
            return
        correct_index = self.questions[self.current_index]['answer_index']
        if self.selected_index == correct_index:
            self.correct_count += 1
            self.ids.quiz_result.text = 'correct'
        else:
            self.ids.quiz_result.text = 'Wrong'
        for i, btn in enumerate(self.option_buttons):
            if i == correct_index:
                btn.background_color = get_color_from_hex('#a5d6a7')
        self.answered = True

    def next_question(self, *_):
        if not self.answered:
            self.check_answer()
        self.current_index += 1
        if self.current_index < len(self.questions):
            self.answered = False
            self._load_question()
        else:
            result = self.manager.get_screen('quiz_result')
            result.set_result(self.correct_count, len(self.questions))
            self.manager.current = 'quiz_result'

    def go_home(self, *_):
        self.manager.current = 'home'

