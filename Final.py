import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from firebase_admin import credentials
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


Window.size = (1024,768)

class screen1(Screen):
    pass
class screen2(Screen):
    pass
class screen3(Screen):
    pass

class MyLayout(FloatLayout):

    scr_mngr = ScreenManager()

    def change_screen(self, screen, *args):
        self.scr_mngr.current = screen
        doc_ref = db.collection(u'Project').document(u'pAKCeGKWGqm1B2MmLMuT')

        try:
            doc = doc_ref.get()
            print(u'Document data: {}'.format(doc.to_dict()))
        except google.cloud.exceptions.NotFound:
            print(u'No such document!')


class MyApp(App):

    def build(self):
        return Builder.load_file('Final.kv')


MyApp().run()