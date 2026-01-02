from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.graphics import Color, RoundedRectangle


class QuizScreen(Screen):
    """Screen to display quiz questions and handle user responses."""
    
    question_text = StringProperty('Loading question...')
    progress_text = StringProperty('Question 1 of 10')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions = []
        self.current_index = 0
        self.user_answers = []
        self.selected_option = None

    def setup_quiz(self, questions):
        """Initialize the quiz with a list of questions."""
        self.questions = questions
        self.current_index = 0
        self.user_answers = []
        self.selected_option = None
        self.show_question()

    def show_question(self):
        """Display the current question and its options."""
        if self.current_index >= len(self.questions):
            self.finish_quiz()
            return

        q = self.questions[self.current_index]
        self.question_text = f"[b]{q['question']}[/b]"
        self.progress_text = f"Question {self.current_index + 1} of {len(self.questions)}"
        
        # Clear previous options
        options_box = self.ids.options_box
        options_box.clear_widgets()
        
        # Create option buttons with better styling
        for i, option in enumerate(q['options']):
            btn = Button(
                text=option,
                font_size='16sp',
                text_size=(None, None),
                halign='left',
                valign='middle',
                padding=[20, 15]
            )
            btn.bind(size=btn.setter('text_size'))
            btn.bind(on_press=lambda b, idx=i: self.select_option(idx, b))
            
            # Add rounded background
            with btn.canvas.before:
                Color(1, 1, 1, 1)
                btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[10])
            btn.bind(pos=self._update_rect, size=self._update_rect)
            
            options_box.add_widget(btn)

    def _update_rect(self, instance, value):
        """Update button background rectangle."""
        if hasattr(instance, 'rect'):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

    def select_option(self, index, button):
        """Handle option selection."""
        self.selected_option = index
        
        # Reset all buttons to white
        for btn in self.ids.options_box.children:
            with btn.canvas.before:
                Color(1, 1, 1, 1)
                btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[10])
        
        # Highlight selected button
        with button.canvas.before:
            Color(0.8, 0.9, 1, 1)  # Light blue
            button.rect = RoundedRectangle(pos=button.pos, size=button.size, radius=[10])

    def next_question(self):
        """Move to the next question or finish the quiz."""
        if self.selected_option is None:
            return
        
        # Store the user's answer
        self.user_answers.append(self.selected_option)
        
        # Check if answer is correct and provide visual feedback
        correct_idx = self.questions[self.current_index]['answer_index']
        buttons = list(self.ids.options_box.children)
        buttons.reverse()  # Reverse because children are in reverse order
        
        # Show correct answer in green, wrong in red
        for i, btn in enumerate(buttons):
            if i == correct_idx:
                with btn.canvas.before:
                    Color(0.2, 0.8, 0.3, 1)  # Green
                    btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[10])
            elif i == self.selected_option and i != correct_idx:
                with btn.canvas.before:
                    Color(0.9, 0.3, 0.3, 1)  # Red
                    btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[10])
        
        # Wait a moment then move to next question
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self._advance_question(), 1.5)

    def _advance_question(self):
        """Advance to the next question."""
        self.selected_option = None
        self.current_index += 1
        self.show_question()

    def quit_quiz(self):
        """Quit the quiz and return to intro screen."""
        self.manager.current = 'quiz_intro'

    def finish_quiz(self):
        """Calculate results and show the result screen."""
        correct_count = sum(
            1 for i, ans in enumerate(self.user_answers)
            if ans == self.questions[i]['answer_index']
        )
        
        result_screen = self.manager.get_screen('result')
        result_screen.show_results(self.questions, self.user_answers, correct_count)
        self.manager.current = 'result'
