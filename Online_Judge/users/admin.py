from django.contrib import admin
from django.contrib.admin.decorators import register

# Register your models here.
from .models import *

class QuestionAdmin(admin.ModelAdmin):
    filter_horizontal = ("tags", )

admin.site.register(Tag)
admin.site.register(Output)
admin.site.register(Submission)
admin.site.register(Testcase)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Contest)