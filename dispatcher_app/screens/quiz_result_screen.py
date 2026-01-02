from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class QuizResultScreen(Screen):
    """Screen to display quiz results with detailed feedback."""
    
    result_text = StringProperty('')

    def show_results(self, questions, user_answers, correct_count):
        """Display the quiz results with motivational message."""
        total = len(questions)
        percentage = (correct_count / total) * 100 if total > 0 else 0
        
        # Motivational message based on performance
        if percentage >= 90:
            emoji = '🌟'
            message = 'Excellent! Outstanding performance!'
        elif percentage >= 75:
            emoji = '👍'
            message = 'Great job! You did very well!'
        elif percentage >= 60:
            emoji = '👌'
            message = 'Good work! Keep it up!'
        elif percentage >= 50:
            emoji = '📚'
            message = 'Not bad! A bit more practice will help!'
        else:
            emoji = '💪'
            message = 'Keep practicing! You can do better!'
        
        # Build result text
        result = f"[size=32sp]{emoji}[/size]\n\n"
        result += f"[size=24sp][b]{message}[/b][/size]\n\n"
        result += f"[size=20sp]Score: {correct_count}/{total} ({percentage:.1f}%)[/size]\n\n"
        result += "[size=18sp]━━━━━━━━━━━━━━━━━━━━[/size]\n\n"
        
        # Show detailed results for each question
        for i, q in enumerate(questions):
            user_ans = user_answers[i] if i < len(user_answers) else None
            correct_ans = q['answer_index']
            is_correct = user_ans == correct_ans
            
            result += f"[b]Q{i+1}:[/b] {q['question']}\n"
            
            if is_correct:
                result += f"[color=2d8a3d]✓ Correct![/color]\n"
            else:
                result += f"[color=c62828]✗ Incorrect[/color]\n"
                if user_ans is not None and user_ans < len(q['options']):
                    result += f"Your answer: {q['options'][user_ans]}\n"
                result += f"Correct answer: {q['options'][correct_ans]}\n"
            
            # Show explanation if available
            if 'explanation' in q and q['explanation']:
                result += f"[i]{q['explanation']}[/i]\n"
            
            result += "\n"
        
        self.result_text = result

    def go_home(self):
        """Return to the quiz intro screen."""
        self.manager.current = 'quiz_intro'
