from kivy.uix.screenmanager import Screen

class QuizResultScreen(Screen):
    """Displays the quiz result summary."""

    def set_result(self, correct, total):
        self.ids.result_label.text = f"You answered {correct} of {total} questions correctly"

    def go_home(self, *_):
        self.manager.current = 'home'
