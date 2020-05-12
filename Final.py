import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from firebase_admin import credentials
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from Projects import SelectableRecycleGridLayout
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty, StringProperty,BooleanProperty,ListProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock
import re
from backports.pbkdf2 import pbkdf2_hmac
from helperFunctions.registrationStuff import *
from helperFunctions.emailsender import sendMail





Window.size = (1024,768)

class Login(Screen):
    pass
class Register(Screen):

    #Verifies each field of the registration page before sending to the superuser for examination
    def register(self,username,realname,email,credentials,reference):
        username = str(self.ids.username.text)
        realname = str(self.ids.realname.text)
        email = str(self.ids.email.text)
        credentials = str(self.ids.credentials.text)
        reference = str(self.ids.reference.text)
        print(type(username))
        if usernameValid(username):
            if (not userExists(username)):
                if (realname.strip()):
                    if (credentials.strip()):
                        if (userExists(reference)):
                            sendMail('pamjje40@gmail.com', 'Registration document', 
                            '''Hello Super User. 
                            {value} is their username. 
                            {value1} is their realname. 
                            {value2} is their email. 
                            {value3} is their credentials. 
                            {value4} is their reference '''.format(value = username, value1 = realname, value2 = email,
                            value3 = credentials, value4 = reference))
                        else:
                            print("Reference does not exist")
                    else:
                        print("Credentials field is empty")
                else:
                    print("Name field is empty")
            else:
                print("Username already exists")
        else:
            print("A username must be alphanumeric only")
class GroupPage(Screen):
    pass
class Projects(Screen):
    
    data_projects = ListProperty([])
    
    def __init__(self,**kwargs):
        super(Projects,self).__init__(**kwargs)
        self.getProjects()

    def on_enter(self):
        self.getProjects()

    def getProjects(self):
        self.data_projects.clear()
        docs = db.collection(u'Project').stream()
        for doc in docs:
            temp = doc.to_dict()
            self.data_projects.append(temp['name'])

class MyLayout(FloatLayout):

    scr_mngr = ScreenManager()

    def change_screen(self, screen, *args):
        self.scr_mngr.current = screen

class newEntry(Screen):
    
    project_name = ObjectProperty(None)
    project_info = ObjectProperty(None)
    
    def submit(self):

        data = {
            u'info': self.project_info.text,
            u'name': self.project_name.text
        }
        db.collection(u'Project').document().set(data)
        

    def switch_screenback(self,*args):
        app = App.get_running_app()
        app.root.scr_mngr.current = "Projects"
        

    def clocked_switch(self):
        Clock.schedule_once(self.switch_screenback,.0)

class SelectableButton(Button):

    def on_release(self):
        app = App.get_running_app()
        app.root.scr_mngr.current = "GroupPage"

class MyApp(App):
    
    def build(self):
        return Builder.load_file('Final.kv')


MyApp().run()