from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout, authenticate
from .models import task
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required(login_url='/login/', redirect_field_name=None)
def index(request):

    if request.method == 'POST':
        
        name = request.POST.get('name')
        title = request.POST.get('title')
        bio = request.POST.get('bio')
        
        twodo = task.objects.create(
            user = request.user,
            name = name,
            title = title,
            bio = bio
        )
        
        twodo.save()
        messages.add_message(request, messages.SUCCESS, 'Todo is Added!')
        return redirect('/')

    else:

        todos = task.objects.filter(user = request.user)
        paginator = Paginator(todos, 1)
        page_number = request.GET.get('page')
        pagi = paginator.get_page(page_number)

        context = {

            'todos':pagi
        }
        
        return render(request, "index.html", context)

def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        mail = request.POST.get('email')
        pwrd = request.POST.get('password')

        if User.objects.filter(username = mail).exists():
            messages.add_message(request, messages.ERROR, 'Email already exists Please try to login')

        else:
            user = User.objects.create_user(username=mail, first_name = fname, last_name = lname, password =pwrd)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Account is created Please login')

    return render(request, "signup.html")

def userlogin(request):
    if request.method == 'POST':
        mail = request.POST.get('email')
        pswrd = request.POST.get('password')

        user = authenticate(request, username = mail, password = pswrd)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Welcome Please create Your Todos here.')
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Credentials')

    return render(request, "login.html")

def viewlogout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'You are Logged Out Please Login.')
    return redirect('/login/')

def recorddelete(request, id):
    todos = task.objects.filter(id = id)
    todos.delete()
    messages.add_message(request, messages.SUCCESS, 'Record is Deleted.')
 
    return redirect('/')

def recordupdate(request, id):
    if request.method == 'POST':

        todos = task.objects.filter(id = id).last()
        
        todos.name = request.POST.get('name')
        todos.title = request.POST.get('title')
        todos.bio = request.POST.get('bio')

        todos.save()
        messages.add_message(request, messages.SUCCESS, 'Record is Updated.')

        return redirect('/')

    else:

        dotos = task.objects.filter(id = id).last()
        context = {
            'dotos' : dotos
        }

        return render(request, "recordupdate.html", context)

def searchtodo(request):

    if request.method == 'POST':
        search_todo = request.POST.get('search')
    if search_todo:
        todos = task.objects.filter(Q(name__icontains = search_todo) | Q(title__icontains =
        search_todo), user = request.user)

        return render(request, "index.html", {'search': search_todo, 'todos':todos })