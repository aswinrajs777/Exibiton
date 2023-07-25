from django.shortcuts import render
import pyrebase
from django.contrib import auth

config = {

'apiKey': "AIzaSyDfStYg1oybMuNWma1-4KGJynjrPwIfyhU",
  'authDomain': "exhibiton-ce35a.firebaseapp.com",
  'databaseURL': "https://exhibiton-ce35a-default-rtdb.firebaseio.com",
  'projectId': "exhibiton-ce35a",
  'storageBucket': "exhibiton-ce35a.appspot.com",
  'messagingSenderId': "241695038706",
  'appId': "1:241695038706:web:91fe325c99c663f7f4c46b",
  'measurementId': "G-Z9LMLY6ZK8"
  }


firebase = pyrebase.initialize_app(config)
database=firebase.database()
authe = firebase.auth()

def singIn(request):

    return render(request, "signIn.html")

def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message = "invalid cerediantials"
        return render(request,"signIn.html",{"msg":message})
    print(user)

    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "welcome.html",{"e":email})

def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')


def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        uid = user['localId']
        data = {"name": name, "status": "1"}
        database.child("users").child(uid).child("details").set(data)
        authe.send_email_verification(user['idToken'])

    except:
        message = "week Password"
        return render(request, "signIn.html", {"messg": message})


    return render(request, "signIn.html",{"messg": "have you verified"})
def welcome(request):

    return render(request,'welcome.html')

def create(request):

    return render(request,'upload.html')

def post_create(request):


    import time
    from datetime import datetime, timezone
    import pytz

    tz= pytz.timezone('Asia/Kolkata')
    time_now= datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis))
    work = request.POST.get('work')
    progress =request.POST.get('progress')
    url = request.POST.get('url')
    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    data = {
        "work":work,
        'progress':progress,
        'url':url
    }
    database.child('users').child(a).child('reports').child(millis).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,'welcome.html', {'e':name})