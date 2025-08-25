from kivy.uix.textinput import TextInput
import os

class CodeArea(TextInput):
    def __init__(self, **kwargs):
        super(CodeArea, self).__init__(**kwargs)

    def apply_code_modifications(self):
        text = self.get_input_text()
        
        self.apply_syntax_highlighting()

    def get_input_text(self):
        """Obtains Input Text"""
        return self.text
        
    def apply_syntax_highlighting(self):
        """Uses Markdown to Apply Syntax Hightlighting"""
        print("Changed!")