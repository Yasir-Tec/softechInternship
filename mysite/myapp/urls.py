from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [

    path('', views.homePage, name='homepage'),
    path('regpage/', views.signup, name='signup'),
    path('regpage/verifyMobile/', views.verifyMobile),
    path('userLoginPage/', views.UserLoginPage, name="user Login Page"),
    path('userLoginPage/forgotUserPass/', views.forgotUserPass, name="forgot user password"),
    path('userLoginPage/forgotUserPass/verifyUser/', views.verifyUser, name="verify user"),
    path('userLoginPage/forgotUserPass/verifyUser/verifyOtp/', views.verifyOtp, name="verify user"),
    path('userLoginPage/forgotUserPass/verifyUser/verifyOtp/updatePass/', views.confirmPass,
         name="confirm new password"),
    path('userLoginPage/UserLogin/', views.AuthUser, name="Authenticate the  user "),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),

    path('redirect/', views.temp),
    path('redirect/verifyMobile/', views.verifyMobile),

    path('userLoginPage/UserLogin/editProfile/', views.editUprofile),
    path('userLoginPage/UserLogin/editProfile/updated/', views.updateUprofile),
    path('userLoginPage/UserLogin/userLogout/', views.loggingout),

]
