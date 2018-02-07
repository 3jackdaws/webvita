from django.db import models
from django.contrib.auth.models import User
import json

class Skill(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User ,on_delete=models.CASCADE)

class Education(models.Model):
    school = models.CharField(max_length=75)
    degree = models.CharField(max_length=75)
    date = models.CharField(max_length=32)
    owner = models.ForeignKey(User ,on_delete=models.CASCADE)

    def to_json(self):
        return json.dumps({
            'school':self.school,
            'degree':self.degree,
            'date':self.date
        })

class ResumeField(models.Model):
    name = models.CharField(max_length=32)
    markup = models.TextField(default='')

class ResumeTheme(models.Model):
    name = models.CharField(max_length=64)
    styletext = models.TextField(default='')
    owner = models.ForeignKey(User ,on_delete=models.CASCADE, null=True)

class ResumeLayout(models.Model):
    name = models.CharField(max_length=64)
    markup = models.TextField(default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class ResumeScript(models.Model):
    name = models.CharField(max_length=64)
    text = models.TextField(default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Resume(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    fields = models.ManyToManyField(ResumeField)
    theme = models.ForeignKey(ResumeTheme, on_delete=models.CASCADE, null=True)
    layout = models.ForeignKey(ResumeLayout, on_delete=models.CASCADE, null=True)
    script = models.ForeignKey(ResumeScript, on_delete=models.CASCADE, null=True)


    def get_html(self):
        return self.layout.markup if self.layout else None



