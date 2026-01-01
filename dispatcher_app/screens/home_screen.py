from kivy.uix.screenmanager import Screen
from version import APP_VERSION

class HomeScreen(Screen):
    """Home screen defined via ``dispatcher.kv`` template."""

    def go_quiz(self, *_):
        self.manager.current = 'quiz_intro'
    def go_airport(self, *_):
        self.manager.current = 'airport'
