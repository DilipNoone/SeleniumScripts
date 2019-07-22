from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import LoginForm,AddGSPForm
from .forms import GSPSearchForm
from .models import GSP
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic.list import ListView
from django.contrib.auth import authenticate,login,logout

# Create your views here.


def login_view(request):
    logout(request)
    page_title = "GSPTracker"
    loginpage_heading = "Google Security Patch Tracker"

    #   If this is a post request we need to process the form data

    username = password = ''
    redirect_to = request.GET.get('next', '/gspapp/')
    print("redirect_to:", redirect_to)
    form = LoginForm()

    if request.POST:
        print("check if request is POST")
        form = LoginForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        print("username:", username)
        print("password:", password)

        user = authenticate(request, username=username, password=password)
        
        print("request.user object:", request.user)

        if user is not None:
            print("logged in user is not None and user is active:")
            login(request, user)

            remember_me = request.POST.get('remember_me', False)

            if remember_me == "on":
                ONE_MONTH = 30 * 24 * 60 * 60
                expiry = getattr(settings, "KEEP_LOGGED_DURATION", ONE_MONTH)
                request.session.set_expiry(expiry)
            else:
                request.session.set_expiry(0)

            return HttpResponseRedirect(redirect_to)

    context = {'form': form, 'page_title': page_title, 'loginpage_heading': loginpage_heading}
    return render(request, 'login.html', context)


#@login_required(login_url='/gspapp/')
def logon_view(request, id=None):
    print("Inside logon_view:")

    if request.method == 'POST':
        form = LoginForm(request.POST)
        print("when request method is POST inside logon_view request:")

        if form.is_valid():
            print("checked whether requested form is valid or not:")
            form.save()
            return HttpResponseRedirect('/gspapp/')
    else:
        print("when request method is GET:")
        form = GSPSearchForm(request.GET)
        context = {'form': form}
        return render(request, 'GSPTracker.html', context)


@login_required(login_url='/gspapp/')
def addgsp_view(request, id = None):

    print("Inside Add Google Security Patch:")
    print("id Inside addgsp_view:", id)

    """
        This method is used to add Google Security Patch if it is GET request and edit or modify the existing
        Google security patch from GSP ListView if it is POST request.           
    """

    if id:
        action = 'edit'
        '''
            Calling get() on a given model Manager ,but it raises Http404 instead of the model Does not Exist exception.
        '''
        model = get_object_or_404(GSP, pk=id)

    else:
        action = 'add'
        model = GSP()

    message = ""

    if request.method == 'POST':
        form = AddGSPForm(request.POST, instance=model)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/gspapp/addgsp')
    else:
        form = AddGSPForm(instance=model)

    context = {'form': form, 'Message': message, 'action': action}
    return render(request, 'AddGSP.html', context)


def gsptrackerlist_view(ListView):

    """
        This view is used to display the added Google security Patches using ListView
    """

    print("Inside GSP Tracker List View:")
    model = GSP
    paginate_by = 10






def gsplist_view(request):
    pass


def applygsp_view(request):
    pass

def gspreview_view(request):
    pass