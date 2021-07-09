
from django.shortcuts import render, redirect
from .models import Beat, Like
from apps.login_project_app.models import Usuario
from .utils import login_required
from django.core.exceptions import PermissionDenied
import bcrypt
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request, 'main.html')

def home(request):
    if 'id' not in request.session:
        return redirect('/auth/login')

    if request.method == 'GET':
        word = request.GET.get('query',None)
        if word:    
            beats = Beat.objects.filter(Q(name__icontains=word)|Q(uploaded_by__first_name__icontains=word))
        else:
            beats = Beat.objects.all()

        user = Usuario.objects.get(id=request.session['id'])
        context = {
            'beats' : beats,
            'user':user
        }
        return render(request, 'home.html', context)

@login_required
def upload_beat(request):
    user = Usuario.objects.get(id=request.session['id'])
    if request.method == 'GET':
        word = request.GET.get('query',None)
        if word:    
            beats = Beat.objects.filter(Q(name__icontains=word)|Q(uploaded_by__first_name__icontains=word))
            return render(request, 'home.html', {'beats':beats,'user':user})
        else:
            return render(request, 'upload_beat.html', {'user':user})
    elif request.method =='POST':
        name = request.POST['name']
        price = request.POST['price']
        category = request.POST['category']
        uploaded_by = user
        newBeat=Beat.objects.create(name=name, price=price, category=category, uploaded_by=user)
        newBeat.save()
    
    return redirect('/home')

@login_required
def delete(request, beat_id):
    beat = Beat.objects.get(id=beat_id)
    if beat.uploaded_by_id != request.session['id']:
        raise PermissionDenied
    beat.delete()
    return redirect('/home')

@login_required
def edit(request, beat_id):
    beat = Beat.objects.get(id=beat_id)
    if beat.uploaded_by_id != request.session['id']:
        raise PermissionDenied
    if request.method == 'GET':
        context = {
            'beat':beat
        }
        return render(request, 'edit_beat.html', context)
    elif request.method == 'POST':
        beat.name = request.POST['name']
        beat.price = request.POST['price']
        beat.category = request.POST['category']
        beat.category = request.POST['category']
        beat.category = request.POST['category']
        beat.save()
        return redirect('/home')

@login_required
def edit_user(request, user_id):
    user_to_edit = Usuario.objects.get(id=request.session['id'])
    if user_to_edit:
        if request.method == 'GET':
            context = {
                'user':user_to_edit
            }
            return render(request, 'edit_user.html', context)
        elif request.method=='POST':
            user_to_edit.first_name = request.POST['first_name']
            user_to_edit.last_name = request.POST['last_name']
            user_to_edit.email = request.POST['email']
            user_to_edit.save()
        return redirect('/home')


@login_required
def edit_password(request, user_id):
    user_to_edit=Usuario.objects.get(id=request.session['id'])
    if user_to_edit:
        if request.method=='GET':
            context = {
                'user':user_to_edit
            }
            return render(request, 'edit_password.html', context)
        elif request.method=='POST':
            password = request.POST['password']
            print('changing password.......')
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user_to_edit.password=pw_hash
            user_to_edit.save()
            return redirect('/home')
        

def view_details(request, beat_id):
    beat = Beat.objects.get(id=beat_id)
    if request.method=='GET':
        context = {
            'beat':beat,
            'user':Usuario.objects.get(id=request.session['id'])
        }
        return render(request, 'beat_details.html', context)

@login_required
def like(request, beat_id):
    beat=Beat.objects.get(id=beat_id)
    user=Usuario.objects.get(id=request.session['id'])
    like = Like.objects.create(beat=beat, user=user)
    return redirect('/home')

@login_required
def unlike(request, beat_id):
    user = Usuario.objects.get(id = request.session["id"])
    beat = Beat.objects.get(id = beat_id)
    like = Like.objects.get(beat = beat,user = user)
    like.delete()
    return redirect('/home')


def hip_hop(request):
    titulo = 'Hip Hop'
    user=Usuario.objects.get(id=request.session['id'])
    beats = Beat.objects.filter(category='Hip-Hop')
    if request.method == 'GET':
        context = {
            'beats':beats,
            'titulo':titulo,
            'user':user
        }
        return render(request, 'by_genre.html', context)
    

def ryb(request):
    titulo = 'R&B'
    user=Usuario.objects.get(id=request.session['id'])
    beats = Beat.objects.filter(category='R&B')
    if request.method == 'GET':
        word = request.GET.get('query',None)
        if word:    
            beats = Beat.objects.filter(Q(name__icontains=word)|Q(uploaded_by__first_name__icontains=word))
            return render(request, 'home.html', {'beats':beats, 'user':user})
        else:
            context = {
                'beats':beats,
                'titulo':titulo,
                'user':user
            }
            return render(request, 'by_genre.html', context)

def sample(request):
    titulo = 'Sample'
    user=Usuario.objects.get(id=request.session['id'])
    beats = Beat.objects.filter(category='Sample')
    if request.method == 'GET':
        context = {
            'beats':beats,
            'titulo':titulo,
            'user':user

        }
        return render(request, 'by_genre.html', context)

def profile(request, user_id):
    user_online = Usuario.objects.get(id=request.session['id'])
    user = Usuario.objects.get(id=user_id)
    beats = Beat.objects.filter(uploaded_by=user)
    if request.method=='GET':        
        word = request.GET.get('query',None)
        if word:    
            beats = Beat.objects.filter(Q(name__icontains=word)|Q(uploaded_by__first_name__icontains=word))
            return render(request, 'home.html', {'beats':beats, 'user':user})
        else:
            context = {
                'user':user,
                'beats': beats,
                'user_online':user_online 
            }
            return render(request,'profile.html', context)
