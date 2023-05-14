from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Meetup, myuser
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from .forms import MeetupForm, myuserregistrationform, participantform, speakerform
from django.db.models import Q
from string import punctuation
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
def homepage(request):
    q=request.GET.get('search') if request.GET.get('search')!=None else ''
    meetups=Meetup.objects.filter(activate=True)
    meetups=meetups.filter(
        
        Q(title__icontains=q)|
        Q(description__icontains=q)|
        Q(from_date__icontains=q)|
        Q(to_date__icontains=q)
        )
    
    
    count=meetups.count
    return render(request, 'meetup/homepage.html', {'meetups': meetups, 'count': count })

def meetup_details(request, meetup_slug):
    
    try:
        selected_meetup=Meetup.objects.get(slug=meetup_slug)
       # speakers=selected_meetup.meetup_speaker.all
        if request.method=='GET':
           registration_form=participantform()
        else:
           registration_form=participantform(request.POST)
           if registration_form.is_valid():
               participant=registration_form.save()
               selected_meetup.participant.add(participant)
               return redirect('confirm-registration')

        return render(request, 'meetup/meetup-details.html', {'meetup':selected_meetup, 'meet_found':True, 'form':registration_form})
    
    except Exception as exc:
        return render(request, 'meetup/meetup-details.html', {'meet_found':True,})
 
        
def confirm_registration(request):
    return render(request, 'meetup/registartion-success.html')


class UpdateMeetup(LoginRequiredMixin, UpdateView):
    model=Meetup
    form_class = MeetupForm
    template_name='meetup/meetup-form.html'
    success_url=reverse_lazy('homepage')
    
class MeetupDelete(DeleteView):
    model=Meetup
    context_object_name='meetup'
    template_name='meetup/meetup-delete.html'
    success_url=reverse_lazy('homepage')
    
class CreateMeetup(LoginRequiredMixin, CreateView):
    model=Meetup
    form_class=MeetupForm
    template_name='meetup/meetup-create.html'
    success_url=reverse_lazy('homepage')
    def form_valid(self, form):
        form.instance.user=self.request.user
        for a in punctuation:
            form.instance.title=form.instance.title.replace(a, ' ')
        form.instance.slug=form.instance.title.replace(' ', '-')
        return super(CreateMeetup, self).form_valid(form)
    
def Loginpage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('homepage')
    #when submit botti=on is pressed
    if request.method=='POST':
        email=request.POST.get('email')
        email.lower()
        password=request.POST.get('password')
        try:
            user=myuser.object.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        user=authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(redirect, 'Username OR password does not exist')
    context={'page': page}
    
    return render(request, 'meetup/login.html', context)

def Register(request):
    page='register'
    form=myuserregistrationform()
    context={'form':form, 'page': page}
    
    if request.method=='POST':
        form=myuserregistrationform(request.POST, request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'An error occured during registration. please re-register.')
            
    return render(request, 'meetup/registration.html', context)  

@login_required(login_url='login')
def add_speakers(request, meetup_slug):
       # selected_meetup=Meetup.objects.get(slug=meetup_slug)
    try:
        selected_meetup=Meetup.objects.get(slug=meetup_slug)
        
        if request.method=='GET':
            add_speaker_form=speakerform()
        else:
           
            add_speaker_form= speakerform(request.POST, request.FILES)
            if add_speaker_form.is_valid():
                add_speaker_form.instance.user=request.user
                
                speaker=add_speaker_form.save(commit=False)
                add_speaker_form.instance.meetup_name=selected_meetup.title
                speaker=add_speaker_form.save()
                selected_meetup.meetup_speakers.add(speaker)
                return redirect('homepage')
              
        return render(request, 'meetup/add_speakers.html', {
         'meet_found':True,
         'meetup':selected_meetup,
         'page':False, 
         'form': add_speaker_form ,
         

          })    
   
    except Exception as exc:
        return render(request, 'meetups/add_speakers.html', {
         'meet_found':False,
         
     })

@login_required(login_url='login')   
def user_meetups(request, pk):
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    
    user_meetups=Meetup.objects.order_by('-create')
    user_meetups=Meetup.objects.filter(user=pk)

    meetups=user_meetups.filter(
        Q(title__icontains=q)
       
        ) 
    count=meetups.count()
    return render(request, 'meetup/user-meetups.html', {
        'meetups':meetups, 
        'count':count
        } )