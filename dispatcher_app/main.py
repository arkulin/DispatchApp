from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from screens.quiz_intro_screen import QuizIntroScreen
from screens.quiz_screen import QuizScreen
from screens.quiz_result_screen import QuizResultScreen
import os


class DispatcherApp(App):
    """Main application class for the Dispatcher Quiz App."""

    def build(self):
        """Build and return the root widget."""
        # Load the KV file
        kv_file = os.path.join(os.path.dirname(__file__), 'dispatcher.kv')
        Builder.load_file(kv_file)
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(QuizIntroScreen(name='quiz_intro'))
        sm.add_widget(QuizScreen(name='quiz'))
        sm.add_widget(QuizResultScreen(name='result'))
        
        return sm


if __name__ == '__main__':
    DispatcherApp().run()
