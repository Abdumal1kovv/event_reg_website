from django.contrib import admin

# Register your models here.

from .models import User, Event, Submission

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Submission)