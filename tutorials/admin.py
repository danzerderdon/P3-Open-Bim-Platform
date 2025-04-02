from django.contrib import admin
from .models import *

admin.site.register(Program)
admin.site.register(Tutorial)
admin.site.register(TutorialSection)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserProgress)
