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
from Projects import SelectableButton,SelectableRecycleGridLayout
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty, StringProperty,BooleanProperty,ListProperty
from kivy.uix.popup import Popup


cred = credentials.Certificate("CS322-FinalProject\serviceAccountKey.json")
eff = firebase_admin.initialize_app(cred)
db = firestore.client()


Window.size = (1024,768)

class screen1(Screen):
    pass
class screen2(Screen):
    pass
class Projects(Screen):
    
    data_projects = ListProperty([])
    
    def __init__(self,**kwargs):
        super(Projects,self).__init__(**kwargs)
        self.getProjects()

    def newProject(self):
        self.Project = newEntry()
        print('popup')
        self.Project.open()

    def getProjects(self):
        docs = db.collection(u'Project').stream()
        for doc in docs:
            temp = doc.to_dict()
            print(temp)
            self.data_projects.append(temp['name'])


        
        
    

class MyLayout(FloatLayout):

    scr_mngr = ScreenManager()

    def change_screen(self, screen, *args):
        self.scr_mngr.current = screen

class newEntry(Popup):
    
    project_name = ObjectProperty(None)
    project_info = ObjectProperty(None)
    
    def submit(self):

        data = {
            u'info': self.project_info.text,
            u'name': self.project_name.text
        }
        db.collection(u'Project').document().set(data)
        Projects.getProjects()
        Popup.dismiss(self)

class MyApp(App):
    
    def build(self):
        return Builder.load_file('Final.kv')


MyApp().run()