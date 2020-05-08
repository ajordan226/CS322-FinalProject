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


cred = credentials.Certificate("serviceAccountKey.json")
eff = firebase_admin.initialize_app(cred)
db = firestore.client()


Window.size = (1024,768)

class screen1(Screen):
    pass
class screen2(Screen):
    pass
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