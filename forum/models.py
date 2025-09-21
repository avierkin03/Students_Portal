from django.db import models

# Create your models here.
class Form(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class FormField(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    message = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class FormSubmite(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="submitions")
    submite_date = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return self.form.title