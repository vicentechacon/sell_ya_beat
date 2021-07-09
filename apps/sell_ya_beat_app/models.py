from django.db import models
# Create your models here.

class Beat(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey('login_project_app.Usuario', on_delete=models.CASCADE, related_name='beats')
    users_who_liked = models.ManyToManyField('login_project_app.Usuario', through='Like')


    def __str__(self):
        return f'{self.name}: ${self.price}'


class Like(models.Model):
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('login_project_app.Usuario', on_delete=models.CASCADE, related_name='likes')