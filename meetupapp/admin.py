from django.contrib import admin
from .models import *

# Register your models here.
class MeetupAdmin (admin.ModelAdmin):
   list_display=('title', 'slug', 'from_date', 'to_date', )
   list_filter=('title',)
   prepopulated_fields={'slug':('title',)}
admin.site.register(myuser)
admin.site.register(Speaker)
admin.site.register(Participant)
admin.site.register(Meetup, MeetupAdmin )