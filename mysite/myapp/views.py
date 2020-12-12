from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignupForm
from .models import Profile, photo
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
import math, random

from twilio.rest import Client
from django.contrib.auth.forms import authenticate, AuthenticationForm
from django.contrib import messages
import base64
from django.core.files.base import ContentFile


def homePage(request):
    return render(request, 'homePage.html')


def home(request):
    return render(request, 'home.html')


def UserLoginPage(request):
    return render(request, 'login.html')


def AuthUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        request.session['setusername'] = username
        password = request.POST.get('password')
        print(password)

        print('inside')
        userObj = Profile.objects.filter(username=username, password=password)
        print(userObj)
        first_condition = f"welcome {username}."
        second_condition = "Your account did not activated by Admin."
        third_condition = "You have entered wrong username or password."
        if userObj:
            print('inside object')
            for i in userObj:
                print(i)
                print(i.username)
                print(i.password)
                if i.username == username and i.password == password and i.Activate_Account == True:
                    return render(request, 'userDashBoard.html', {'first_condition': first_condition})
                elif i.username == username and i.password == password and i.Activate_Account == False:
                    return render(request, 'userDashBoard.html',
                                  {'second_condition': second_condition, 'username': i.first_name})
                else:
                    return HttpResponse(request, 'userDashBoard.html', {'third_condition': third_condition})
        else:
            return render(request, 'userDashBoard.html', {'third_condition': third_condition})


def forgotUserPass(request):
    return render(request, 'forgotUserPass.html')


def signup(request):
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]

    get = OTP

    msg_body = f'Hiii yasir here....your OTP is {get}'
    request.session['setotp'] = get
    a = request.session['setotp']

    def passotp():
        return a

    passotp()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            print('inside valid')
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            print(user.profile.first_name)
            user.profile.last_name = form.cleaned_data.get('last_name')
            print(user.profile.last_name)
            user.profile.email = form.cleaned_data.get('email')
            companyID = request.POST.get('CompanyID')
            print(companyID)
            user.profile.mobile = form.cleaned_data.get('mobile')
            user.profile.username = form.cleaned_data.get('username')
            username = request.POST.get('username')
            print(username)
            request.session['setusernamesession'] = username
            user.profile.password = form.cleaned_data.get('password1')
            user.save()

            user.is_active = False
            user.save()

            ################################################### CAPTURE AND PROCESS WEB-IMAGE ################
            print('webcam part')
            image = request.POST.get('index')
            print(image)
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr),
                               name=username + '.' + ext)  # You can save this as file instance.
            print("updating image,otp and company id feilds of Profile Model.")
            imageName = username + '.' + ext

            usero = Profile.objects.filter(username=username).update(otp=get)
            userc = Profile.objects.filter(username=username).update(CompanyID=companyID)
            userI = Profile.objects.filter(username=username).update(image=imageName)
            print(userc)
            print(usero)
            print(userI)
            ul = photo(image=data, username=username)
            ul.save()
            print("photo saved to database")
            #########################################Email verification link part ###############################
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user, 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # Sending activation link in terminal
            # user.email_user(subject, message)
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            #################################################### MOBILE OTP MODULE ############################

            account_sid = "ACb462a6df295393c8a57e9dbc2771a0a6"
            account_token = "f914d9d3fff1195f2d939ea42b333f3c"
            ##################################################### send mobile OTP ####################
            print('form saved but phone isnt')
            client = Client(account_sid, account_token)

            message = client.messages.create(
                to="+918806281949",
                from_='(351) 999-8961',
                body=msg_body)

            print(message.sid)
            print(message)

            print('mobile Otp has been sent')

            return redirect('http://127.0.0.1:8000/redirect/')

    # return render(request, 'acc_active_sent.html')

    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.profile.is_active = True
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('You have verified successfully !')
    else:
        return HttpResponse('Activation link is invalid!')


def temp(request):
    return render(request, 'verifyMobile.html')


def verifyUser(request):
    searchEmail = request.POST.get('email')
    request.session['setEmail'] = searchEmail
    verifyObject = Profile.objects.filter(email=searchEmail)
    otp = random.randint(0000, 9999)
    request.session['setOtp'] = otp
    wrongEmail = "Email not found"
    emailFound = "email found"
    if verifyObject:
        for i in verifyObject:
            if i.email == searchEmail:
                send_mail('Verify Your account with OTP :',
                          f'Your OTP is {otp}',
                          'yasirshaikhkhan4633@gmail.com',
                          [searchEmail],
                          fail_silently=False)

                return render(request, 'verifyUserOtp.html', {'emailFound': emailFound})
    else:
        return render(request, 'verifyUserOtp.html', {'wrongEmail': wrongEmail})


def verifyOtp(request):
    getotp = request.POST.get('getOtp')
    setotp = request.session['setOtp']
    print(setotp)
    print(getotp)
    ##messages.add_message(request, messages.INFO, 'Hello world.', fail_silently=False)
    msg = 'User verified'
    msg2 = 'authentication failed'
    if getotp == str(setotp):
        return render(request, 'newUserPassword.html', {'msg': msg})
    else:
        return render(request, 'newUserPassword.html', {'msg2': msg2})


def confirmPass(request):
    pass11 = request.POST.get('pass1')
    pass21 = request.POST.get('pass2')
    print('passwords are:')
    print(pass21)
    print(pass11)

    getSetEmail = request.session['setEmail']
    print(getSetEmail)

    passUpdated = "You password updated Successfully"
    updationFailed = "Please enter same password"

    if pass11 == pass21:
        Profile.objects.filter(email=getSetEmail).update(password=pass11)
        return render(request, 'newUserPassword.html', {'passUpdated': passUpdated})
    else:
        return render(request, 'newUserPassword.html', {'updationFailed': updationFailed})


def verifyMobile(request):
    getmobileotp = request.POST.get('getotp')
    print(getmobileotp)
    usero = Profile.objects.filter(otp=getmobileotp)
    first_condition = 'satisfied both conditions'
    second_condition = 'SORRY ! Please verify Your email first.'
    third_condition = 'You have entered Wrong OTP.'
    if usero:
        for i in usero:
            print('Inside the fetching part of OTP')
            if i.otp == getmobileotp and i.is_active == True:
                print('satisfied both conditions')
                return render(request, 'confirmRegistration.html', {'first_condition': first_condition})
            elif i.is_active == False:
                print("Email is not verified yet")
                return render(request, 'confirmRegistration.html', {'second_condition': second_condition})
            else:
                print("user has entered wrong OTP")
                return render(request, 'confirmRegistration.html', {'third_condition': third_condition})

    return render(request, 'confirmRegistration.html', {'third_condition': third_condition})


def editUprofile(request):
    getusername = request.session['setusername']
    print(getusername)
    userObject = Profile.objects.filter(username=getusername)

    return render(request, 'editProfile.html', {'userdata': userObject})


def updateUprofile(request):
    getusername = request.session['setusername']
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    mobile = request.POST.get('mobile')
    username = request.POST.get('username')

    userobj = Profile.objects.filter(username=getusername).update(first_name=fname, last_name=lname, email=email,
                                                                  mobile=mobile, username=username)
    print(userobj)
    return HttpResponse('success')


def loggingout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000')
