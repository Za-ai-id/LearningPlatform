from django.contrib import admin

from .models import Register, Profile, Question, Answer  # import your models

admin.site.register(Register)
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
# Register your models here.
