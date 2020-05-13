import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from firebase_admin import credentials
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.label import Label
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
from helperFunctions.updateDB import *


Window.size = (1024,768)


class MessageBoard(Screen):
    data_messages = ListProperty([])
    
    def __init__(self,**kwargs):
        super(MessageBoard,self).__init__(**kwargs)
        self.populateMessages()
    
    def on_enter(self):
        self.populateMessages()
    
    def populateMessages(self):
        self.data_messages.clear()
        messages = getMessages(MyApp.currentGroup)
        for i in messages:
            self.data_messages.append(i)

class UserList(Screen):
     
    data_users = ListProperty([])
    
    def __init__(self,**kwargs):
        super(UserList,self).__init__(**kwargs)
        self.getUsers()
        

    def on_enter(self):
        self.getUsers()
    
    def getUsers(self):
        self.data_users.clear()
        members = getMembers(MyApp.currentGroup)
        for i in members:
            self.data_users.append(i)



class Login(Screen):
    def verifyLogin(self,user,password):
        user = str(self.ids.user.text)
        password = str(self.ids.password.text)
        p = SuccessPopup()
        if userExists(user):
            userDocument = getUserDocument(user)
            attemptedKey = pbkdf2_hmac("sha256",password.encode('utf-8'),userDocument['salt'],80000,32)
            success = attemptedKey == userDocument['key']
            if (not success):
                p.ids.textLabel.text = "Incorrect Password!"
                print("Incorrect password")
                p.open()
            else:
                p.ids.textLabel.text = "Success!"
                p.open()
                print('success')
                MyApp.loggedUser = user
                print(MyApp.loggedUser)
        else:
            p.ids.textLabel.text = "No account with that username!"
            p.open()
            print("An account with that user name does not exist")
            return False

class SuccessPopup(Popup):
    pass
class Register(Screen):

    #Verifies each field of the registration page before sending to the superuser for examination
    def register(self,username,realname,email,credentials,reference):
        username = str(self.ids.username.text)
        realname = str(self.ids.realname.text)
        email = str(self.ids.email.text)
        credentials = str(self.ids.credentials.text)
        reference = str(self.ids.reference.text)
        p = SuccessPopup()
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
                            createPotentialUser(username,realname,email,credentials,reference)
                            registerPotentialUser(username)
                        else:
                            print("Reference does not exist")
                            p.ids.textLabel.text = "Reference does not exist!"
                            p.open()
                    else:
                        print("Credentials field is empty")
                        p.ids.textLabel.text = "Credentials field is empty!"
                        p.open()
                else:
                    print("Name field is empty")
                    p.ids.textLabel.text = "Name field is empty!"
                    p.open()
            else:
                print("Username already exists")
                p.ids.textLabel.text = "Username already exists!"
                p.open()
        else:
            print("A username must be alphanumeric only")
            p.ids.textLabel.text = "A username must be alphanumeric only"
            p.open()

class GroupPage(Screen):
    pass
class Moderation(Screen):
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
        createGroup(MyApp.loggedUser,self.project_name.text)
        '''data = {
            u'info': self.project_info.text,
            u'name': self.project_name.text
        }

        db.collection(u'Project').document(self.project_name.text).set(data)'''

    def switch_screenback(self,*args):
        app = App.get_running_app()
        app.root.scr_mngr.current = "Projects"


    def clocked_switch(self):
        Clock.schedule_once(self.switch_screenback,.0)

class SelectableButton(Button):

    def on_release(self):
        app = App.get_running_app()
        MyApp.currentGroup = self.text
        print(MyApp.currentGroup)
        app.root.scr_mngr.current = "GroupPage"

class messageBoardLabel(Label):
    pass

class MyApp(App):
    
    loggedUser = ''
    currentGroup = 'grouptest'

    
    def build(self):
        return Builder.load_file('Final.kv')


MyApp().run()
