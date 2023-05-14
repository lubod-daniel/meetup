from django import forms 
from .models import Meetup, myuser, Participant, Speaker
from django.contrib.auth.forms import UserCreationForm
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.forms import Textarea, TextInput

class MeetupForm(forms.ModelForm):
    class Meta:
        model=Meetup
        fields=['title', 'from_date',  'to_date', 'meetup_time', 'description', 'organizer_email',  'location_name', 'location_address', 'activate','image',]
        widgets = {
            'meetup_date' : DatePickerInput(
            attrs={
                    
                     "class":"form-control"
                }
            
            ),
            'from_date' : DatePickerInput(
            attrs={
                    
                     "class":"form-control"
                }
            
            ),
            'to_date' : DatePickerInput(
            attrs={
                    
                     "class":"form-control"
                }
            

            ),
            'meetup_time':TimePickerInput(
            attrs={
                    
                     "class":"form-control"
                }
            
            ),
            'location_address':Textarea(
                attrs={
                    "placeholder": "Enter location address",
                     "class":"form-control"
                }
            ),
            
            'description':Textarea(
                
                attrs={
                    "placeholder": "Enter meetup description",
                     "class":"form-control"
                }
            ), 
            'title':TextInput(
                attrs={
                   "placeholder": "Enter title",
                   "class":"form-control"
                }
            ),
            
            'organizer_email':TextInput(
                attrs={
                   "placeholder": "Enter your email",
                    "class":"form-control"
                }
            ),
            'location_name':TextInput(
                attrs={
                   "placeholder": "Enter location name",
                    "class":"form-control"
                }
            )
           
        }
        
class myuserregistrationform(UserCreationForm):
    class Meta:
        model=myuser
        fields=['name', 'username', 'email', 'password1', 'password2']
        
class participantform(forms.ModelForm):
    class Meta:
        model=Participant
        fields=['name', 'email']
        
class speakerform(forms.ModelForm):
    class Meta:
        model= Speaker
        fields=['name', 'email', 'phone', 'bio', 'image']
        
