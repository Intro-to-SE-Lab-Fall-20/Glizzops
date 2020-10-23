from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


 #Create your models here.
class Tutorial(models.Model):
	tutorial_title = models.CharField(max_length=200)
	tutorial_content = models.TextField()
	tutorial_published = models.DateTimeField("date published", default=datetime.now())

	def __str__(self):
		return self.tutorial_title

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Inbox(TimestampMixin):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_inboxes')
    guess = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guess_inboxes')

    def __str__(self):
        return self.owner.username + ' - ' + self.guess.username

    class Meta:
        verbose_name_plural = 'inboxes'


class Message(TimestampMixin):
    inbox = models.ForeignKey(Inbox, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:25]

    def save(self, *args, **kwargs):
        self.inbox.save()
        super(Message, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created_at']
