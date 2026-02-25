from django.contrib import admin
from .models import *

admin.site.register(ForumQuestion)
admin.site.register(ForumAnswer)
admin.site.register(QuestionTags)
# Register your models here.
