from django.db import models
from django.contrib.auth.models import User

class ResumeField(models.Model):
    name = models.CharField(max_length=32)
    markup = models.TextField(null=True)

class ResumeTheme(models.Model):
    name = models.CharField(max_length=64)
    styletext = models.TextField(null=True)
    owner = models.ForeignKey(User ,on_delete=models.CASCADE, null=True)

class ResumeLayout(models.Model):
    name = models.CharField(max_length=64)
    markup = models.TextField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class ResumeScript(models.Model):
    name = models.CharField(max_length=64)
    text = models.TextField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Resume(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    fields = models.ManyToManyField(ResumeField)
    theme = models.ForeignKey(ResumeTheme, on_delete=models.CASCADE, null=True)
    layout = models.ForeignKey(ResumeLayout, on_delete=models.CASCADE, null=True)
    scripts = models.ManyToManyField(ResumeScript)


    def get_html(self):
        return self.layout.markup if self.layout else None



