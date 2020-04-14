import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

from kivy.lang import Builder

class LoginWidget(Widget):
    pass

class loginScreenApp(App):
    def build(self):
        return LoginWidget()

loginScreenApp().run()
