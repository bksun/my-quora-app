from django.contrib import admin

# Register your models here.
from myquora.models import Author, Question, Answer, Comment

admin.site.register(Author)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)