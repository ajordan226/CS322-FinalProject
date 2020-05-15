# CS322-FinalProject
Spring 2020 CSC 32200 Final Project. This system will facilitate active teaming of people with similar interest and skill-set to forge groups for a certain do-good project.

# To run:
1) make sure python 3.8 is installed, include pip installation
2) In terminal : python -m pip install --upgrade pip wheel setuptools virtualenv
3) In terminal : python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
4) In terminal : python -m pip install kivy_deps.gstreamer==0.1.*
5) In terminal : python -m pip install kivy==1.11.1
6) In terminal : pyhton -m pip install backports.pbkdf2
7) Choose an empty folder destination and type: git clone https://github.com/ajordan226/CS322-FinalProject.git
8) Log into the email in emailsender.py and enable access from insecure applications in the security settings, otherwise google will block the SMTP requests the application makes causing it to crash. Google disables this feature when not in use for security purposes. 
9) Run final.py
10) to request access to firestore Database please email pjohnso002@citymail.cuny.edu to request permissions
