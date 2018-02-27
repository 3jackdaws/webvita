from django.db import models
from django.contrib.auth.models import User


class ResumeObject(models.Model):
    type = models.CharField(max_length=32)
    data = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Resume(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    theme = models.ForeignKey(ResumeObject, on_delete=models.CASCADE, null=True, related_name='theme_related')
    layout = models.ForeignKey(ResumeObject, on_delete=models.CASCADE, null=True, related_name='layout_related')
    script = models.ForeignKey(ResumeObject, on_delete=models.CASCADE, null=True, related_name='script_related')




