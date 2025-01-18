from django.shortcuts import render , redirect,HttpResponse
from django.contrib import messages
from django.db.models import Q 
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm,MyUserCreationForm

# rooms =[
#     {'id':1, 'name':'lets learn python!!', 'description': 'This is Room A'},
#     {'id':2, 'name':'design with me' , 'description': 'This is Room B'},
#     {'id':3, 'name':'MERN stack with me' ,'description': 'This is Room C'},
#     {'id':4, 'name':'Frontend developers', 'description': 'This is Room D'},
# ]

# Create your views here.

def loginpage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")
            
        user = authenticate(request,email=email,password =password)   
    
        if user is not None:
            login(request,user)
            messages.success(request, f" 🎉Welcome back, {user.username}! 🌟")
            return redirect('home')
        else:
            messages.error(request, "❌ Invalid Username or Password")
        
    context={'page': page}
    return render(request, 'base/login_register.html',context)




def logoutUser(request):
    logout(request)           # it will delete that token
    return redirect("home")



def registerPage(request):
    form = MyUserCreationForm()
    context ={"form": form}
    
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username =user.username.lower()
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request, 'An error occured during registeration')
    return render(request, 'base/login_register.html',context)



def home(request):
    q =request.GET.get('q') if request.GET.get('q') != None else ''     # check if the rquest method has something if not it will have none but filter method still wont work 
    rooms = Room.objects.filter(                                        # rooms = Room.objects.filter() w/o parameter just like all method it will get all the rooms
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
        )                       
    
    topics = Topic.objects.all()[0:5]
    rooms_count = rooms.count()   # this method is faster than len()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    
    context ={'rooms':rooms, 'topics': topics,'room_count':rooms_count, 'room_messages':room_messages}
    return render(request, "base/home.html" ,context )



def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body"),
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    
    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request,'base/room.html' ,context )





def userprofile(request,pk):
    user= User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    
    context ={'user':user,'rooms':rooms, 'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)




@login_required(login_url='/login')
def createroom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic,created =Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get("description"),
        )
        return redirect('home')
        
    context={'form': form, 'topics':topics}
    return render(request, 'base/room_form.html' , context)




@login_required(login_url='/login')
def updatedRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)  #before submit this this form is prefilled
    topics = Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse("you are not allowed here!!")
    
    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)   # if we did just request.POST it will create a new room 
        if form.is_valid():                           # so we need to tell which room to be update thats why we passed instance
            form.save()
            messages.success(request,"Room details updated.")
        return redirect("home")
    context ={'form': form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html' ,context)



@login_required(login_url='/login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("you cannot edit other's room!!")
    
    if request.method == 'POST':
        room.delete()
        messages.success(request,"room deleted successfully")
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})




@login_required(login_url='/login')
def deleteMessage(request,pk):
    message =Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse("you cannot edit other's message!!")
    
    room_id = message.room.id
    
    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=room_id)
    return render(request, 'base/delete.html', {'obj': message})



@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)
    
    if request.method == "POST":
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_profile", pk=user.pk)
    context ={"form":form}
    return render(request, 'base/update_user.html' ,context)



def topicsPage(request):
    q =request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics':topics}
    return render(request, 'base/topics.html', context)


def activityPage(request):
    room_messages = Message.objects.all()
    context={'room_messages':room_messages}
    return render(request, "base/activity.html", context)

