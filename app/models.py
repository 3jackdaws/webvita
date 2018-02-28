from django.db import models
from django.contrib.auth.models import User
import random
linkchars = [x for x in 'ABCDEFGHJKLMNPQRSTUVWXYZ0123456789']

def gensharelink():
    sharelink = ''
    for _ in range(8):
        sharelink += random.choice(linkchars)
    return sharelink


class ResumeObject(models.Model):
    type = models.CharField(max_length=32)
    data = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Resume(models.Model):
    name = models.CharField(max_length=64)
    sharelink = models.CharField(max_length=32, default=gensharelink)
    vanity = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    theme = models.ForeignKey(ResumeObject, on_delete=models.CASCADE, null=True, related_name='theme_related')
    layout = models.ForeignKey(ResumeObject, on_delete=models.CASCADE, null=True, related_name='layout_related')
    script = models.ForeignKey(ResumeObject, on_delete=models.CASCADE, null=True, related_name='script_related')


