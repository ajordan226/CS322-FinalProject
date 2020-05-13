from imports import *

Window.size = (1024,768)

class VoteScreen(Screen):
    
    data_voteinfo = ListProperty([])

    def __init__(self,**kwargs):
        super(VoteScreen,self).__init__(**kwargs)
        self.getVotes()

    def on_enter(self):
        self.getVotes()
    
    def voteNow(self):
        pass

    def getVotes(self):
        self.data_voteinfo.clear()
        docs = db.collection(u'Project').document(MyApp.currentGroup).collection('polls').document(MyApp.polltype).get().to_dict()
        for voter in docs.keys():
           self.data_voteinfo.append([voter,docs[voter]])
        print(self.data_voteinfo)

class PollScreen(Screen):
    data_polls = ListProperty([])

    def __init__(self,**kwargs):
        super(PollScreen,self).__init__(**kwargs)
        self.getPolls()

    def on_enter(self):
        self.getPolls()


    def getPolls(self):
        self.data_polls.clear()
        docs = db.collection(u'Project').document(MyApp.currentGroup).collection('polls').stream()
        for doc in docs:
           self.data_polls.append(doc.id)
        print(self.data_polls)

class InviteManager(Screen):

    def acceptInv(self):
        acceptInvite(MyApp.loggedUser, MyApp.currentGroup, self.ids.acceptInvite.text)

    def invUser(self):
        if isMember(MyApp.loggedUser, MyApp.currentGroup):
            inviteUser(MyApp.loggedUser, self.ids.inviteUser.text, MyApp.currentGroup)

    def addWhite(self):
        addWhiteList(MyApp.loggedUser, self.ids.addToWhitebox.text)

    def addBlack(self):
        addBlackList(MyApp.loggedUser, self.ids.addToBlackbox.text)


    def acceptInv(self):
        acceptInvite(MyApp.loggedUser, MyApp.currentGroup, self.ids.acceptInvite.text)

    def invUser(self):
        if isMember(MyApp.loggedUser, MyApp.currentGroup):
            inviteUser(MyApp.loggedUser, self.ids.inviteUser.text, MyApp.currentGroup)

    def addWhite(self):
        addWhiteList(MyApp.loggedUser, self.ids.addToWhitebox.text)

    def addBlack(self):
        addBlackList(MyApp.loggedUser, self.ids.addToBlackbox.text)

class GroupUserPage(Screen):

    def on_enter(self):
        self.ids.Reputation.text = "Reputation Score: " + str(MyApp.currentRep)

    def voteKick(self):
        startGroupPoll(MyApp.currentGroup,'votekick',MyApp.groupUserPage)
    
    def warning(self):
        startGroupPoll(MyApp.currentGroup,'warning',MyApp.groupUserPage)

    def compliment(self):
        pass

class MessageBoard(Screen):
    data_messages = ListProperty([])


    def __init__(self,**kwargs):
        super(MessageBoard,self).__init__(**kwargs)

    def on_enter(self):
        self.data_messages.clear()
        self.populateMessages()

    def populateMessages(self):
        self.data_messages.clear()
        docs = db.collection(u'Project').document(MyApp.currentGroup).collection("forum").order_by('msgNumber').stream()
        for doc in docs:
            temp = doc.to_dict()
            self.data_messages.append(temp['msg'])
        print(self.data_messages)
    
    def post(self):
        addMessage(MyApp.loggedUser,MyApp.currentGroup,self.ids.message.text)
        self.populateMessages()


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

    def on_enter(self):
        self.ids.groupPageName.text = MyApp.currentGroup
        self.ids.groupDescription.text = getGroupDescription(MyApp.currentGroup)


class Moderation(Screen):
    pass
class ChangePassword(Screen):
    def __init__(self,**kwargs):
        super(ChangePassword,self).__init__(**kwargs)

    def changePassw(self):
        userDocument = getUserDocument(MyApp.loggedUser)
        if not passwordValid(self.ids.NewPassword.text):
            print("Password must be mixed case at least 6 characters, be mixed case, and have a number")
        elif self.ids.NewPassword.text != self.ids.ConfirmPassword.text:
            print("Passwords do not match")
        else:
            newPassHash = hash(self.ids.NewPassword.text)
            db.collection(u'User').document(MyApp.loggedUser).update({'key' : newPassHash['key'], 'salt' : newPassHash['salt']})
            print('changed')

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
        createGroup(MyApp.loggedUser,self.project_name.text,self.project_info.text)
        
    def switch_screenback(self,*args):
        app = App.get_running_app()
        app.root.scr_mngr.current = "Projects"

    def clocked_switch(self):
        Clock.schedule_once(self.switch_screenback,.0)

class SelectableButton(Button):

    def on_release(self):
        app = App.get_running_app()
        app.root.scr_mngr.current = "GroupPage"

    def on_press(self):
        MyApp.currentGroup = self.text
        print(MyApp.currentGroup)

class pollButton(Button):

    def on_release(self):
        app=App.get_running_app()
        app.root.scr_mngr.current = "VoteScreen"
    
    def on_press(self):
        MyApp.polltype = self.text

class userSelectableButton(Button):

    def on_release(self):
        app = App.get_running_app()
        MyApp.groupUserPage = self.text
        print(MyApp.groupUserPage)
        app.root.scr_mngr.current = "GroupUserPage"

    def on_press(self):
        user = self.text
        userDoc = getUserDocument(user)
        MyApp.currentRep = userDoc['reputation']
        print(MyApp.currentGroup)

class messageBoardLabel(Label):
    pass

class MyApp(App):

    loggedUser = ''
    currentGroup = 'testingAgain'
    groupUserPage = ''
    currentRep = 0
    polltype = 'votekickpoll'
    checking = ['hi','to','you']


    def build(self):
        return Builder.load_file('Final.kv')


MyApp().run()
