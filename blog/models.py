from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    user= models.ForeignKey(User,related_name='user',on_delete=models.CASCADE,null=False,default=None)
    title = models.CharField(max_length = 200, null=False,default=None)
    content = models.TextField(null=False,default=None)
    last_modified = models.DateTimeField(auto_now_add = True, null=True)

    def __str__(self):
        return self.title