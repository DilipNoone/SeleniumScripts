#from django.conf.urls import url
from django.urls import path
from . import views
from gspapp.views import gsptrackerlist_view
from django.contrib.auth.decorators import login_required

app_name = 'gspapp'

urlpatterns = [
    path('', login_required(views.logon_view, login_url='/gspapp/login'), name='GSPTracker'),
    path('GSPTrackerList/', login_required(views.gsptrackerlist_view.as_view(), login_url='/gspapp/login'), name='GSPTrackerList'),
    path('GSPList/', login_required(views.gsplist_view, login_url='/gspapp/'), name='GSPList'),
    path('login/', views.login_view, name='login'),
    path('AddGSP/', views.addgsp_view, name='AddGSP'),
]
