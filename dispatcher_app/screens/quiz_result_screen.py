from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class QuizResultScreen(Screen):
    """Displays the quiz result summary."""
    
    title_text = StringProperty('Quiz Complete!')
    result_text = StringProperty('')

    def set_result(self, correct, total):
        """Set the quiz results with formatted text."""
        percentage = (correct / total * 100) if total > 0 else 0
        
        # Determine emoji and message based on performance
        if percentage >= 90:
            emoji = '🌟'
            message = 'Excellent!'
        elif percentage >= 75:
            emoji = '👍'
            message = 'Great job!'
        elif percentage >= 60:
            emoji = '👌'
            message = 'Good work!'
        elif percentage >= 50:
            emoji = '📚'
            message = 'Keep practicing!'
        else:
            emoji = '💪'
            message = 'Keep trying!'
        
        self.title_text = f'{emoji} Quiz Complete!'
        self.result_text = f'''
{message}

You answered {correct} out of {total} questions correctly

Score: {percentage:.1f}%
'''

    def go_home(self, *_):
        """Return to home screen."""
        self.manager.current = 'home'
