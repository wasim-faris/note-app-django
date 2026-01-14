from django.shortcuts import render,redirect,get_object_or_404
from .models import NoteApp
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
@login_required
@never_cache
def home(request):
     if request.method=="POST":
        notehead = request.POST.get("notehead")
        notecontent = request.POST.get("notecontent")

        NoteApp.objects.create(
            notehead = notehead,
            notecontent = notecontent,
            is_public=False,
            user = request.user
        )

        return redirect("home")

     allnotes = NoteApp.objects.filter(user=request.user,is_public=False)

     return render(request, "home.html", {"notes": allnotes})

def delete_note(request, id):
    delobj = NoteApp.objects.get(id=id)

    delobj.delete()

    return redirect("home")

def update(request, id):
    updatelement =  NoteApp.objects.get(id=id)

    if request.method == "POST":
        updatelement.notehead = request.POST.get("notehead")
        updatelement.notecontent = request.POST.get("notecontent")

        # --- ADD THESE LINES TO FIX THE PUBLIC TOGGLE ---
        if 'is_public' in request.POST:
            updatelement.is_public = True
        else:
            updatelement.is_public = False
        # ------------------------------------------------

        updatelement.save()
        return redirect("home")

    if request.method=="POST":
        updatehead = request.POST.get("notehead")
        updatecontent = request.POST.get("notecontent")


        updatelement.notehead = updatehead
        updatelement.notecontent = updatecontent

        updatelement.save()

        return redirect("home")
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
     username = request.POST.get('username')
     password = request.POST.get('password')

     user = authenticate(username=username, password=password)

     if user is not None:
         login(request, user)
         return redirect('home')
     else:
         return render(request, 'login.html', {"error": "Invalid credentials"})


    return render(request, 'login.html')
def signup(request):
    if request.method=="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')


        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {"error": "Username already taken"})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {"error": "email already taken"})

        if password != confirm_password:
            return render(request, 'signup.html', {"error": "Password doesnt match"})

        # if len(username)<6:
        #     return render(request, 'signup.html', {'error': 'Username must be greater than 6'})

        if len(password)<8:
            return render(request, 'signup.html', {'error': 'PassWord must be greter than 8'})


        User.objects.create_user(
            username = username,
            email=email,
            password=password,
        )

        return redirect('login')

    return render(request, 'signup.html')

def logout_page(request):
    logout(request)
    return redirect('login')

def public_view(request,token):
    note = get_object_or_404(NoteApp, share_token=token)
    return render(request, 'public.html', {"note": note})


def all_view(request):

    if request.method=='POST':


        NoteApp.objects.create(
            notehead = request.POST.get('notehead'),
            user = request.user,
            notecontent = request.POST.get('notecontent'),
            is_public = True
        )

        return redirect('all_view')

    publicnotes = NoteApp.objects.filter(is_public=True)
    return render(request, 'public_view.html', {
        "publicnote": publicnotes
    })
def public_del(request,id):
    delobj = NoteApp.objects.get(id=id)
    if request.user == delobj.user:
        delobj.delete()
        return redirect('all_view')
    else:
       messages.error(request, "only owner can delet this item")
       return redirect('all_view')

def public_update(request, id):
    updatepublic = NoteApp.objects.get(id=id)

    if request.user == updatepublic.user:

        if request.method=='POST':

            public_notehead = request.POST.get('notehead')
            public_notecontent = request.POST.get('notecontent')

            updatepublic.notehead = public_notehead
            updatepublic.notecontent = public_notecontent
            updatepublic.is_public = True
            updatepublic.save()

            return redirect('all_view')
    else:
        messages.error(request, "only owner can change this one")
        return redirect('all_view')
