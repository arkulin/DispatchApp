from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

# Import screens
from screens.home_screen import HomeScreen
from screens.quiz_intro_screen import QuizIntroScreen
from screens.quiz_screen import QuizScreen
from screens.quiz_result_screen import QuizResultScreen
from screens.airport_screen import AirportScreen

# Load the kv file
Builder.load_file('dispatcher.kv')

class DispatcherApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(QuizIntroScreen(name='quiz_intro'))
        sm.add_widget(QuizScreen(name='quiz'))
        sm.add_widget(QuizResultScreen(name='quiz_result'))
        sm.add_widget(AirportScreen(name='airport'))
        sm.current = 'home'
        return sm

if __name__ == '__main__':
    DispatcherApp().run()
