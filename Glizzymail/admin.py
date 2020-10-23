from django.contrib import admin
from .models import Tutorial, Inbox, Message
from tinymce.widgets import TinyMCE
from django.db import models
# Register your models here.

class TutorialAdmin(admin.ModelAdmin):
	
	fieldsets = [
		("Title/date", {"fields": ["tutorial_title", "tutorial_published"]}),
		("Content", {"fields":["tutorial_content"]})
		]
	formfield_overrides= {
	models.TextField: {'widget': TinyMCE()}
	}

class InboxAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Inbox, InboxAdmin)
admin.site.register(Message, MessageAdmin)