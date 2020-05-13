'''import firebase_admin
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
from kivy.clock import Clock'''
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
from kivy.uix.spinner import Spinner
