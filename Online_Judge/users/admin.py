from django.contrib import admin
from django.contrib.admin.decorators import register

# Register your models here.
from .models import *

class QuestionAdmin(admin.ModelAdmin):
    filter_horizontal = ("tags", )

admin.site.register(userdata)
admin.site.register(Contest)
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Testcase)
admin.site.register(Submission)