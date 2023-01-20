from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    post_img = models.ImageField(upload_to="post_images",)
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500)
    destination_link = models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
        return self.post_title
    class Meta:
        ordering=['-created_date']


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="userforcomment")
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment = models.CharField(max_length=400)
    created_date = models.DateTimeField(auto_now_add=True)
    like=models.ManyToManyField(User,blank=True,related_name="likeforcomment")
    def __str__(self):
        return self.comment
    class Meta:
        ordering=['-created_date']
        
class CommentReply(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="userforreply")
    reply = models.CharField(max_length=300)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    like=models.ManyToManyField(User,blank=True,related_name="likeforreply")
    created_date=models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.reply
    class Meta:
        ordering=['-created_date']

class Saved(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.post
    class Meta:
        ordering=['-created_date']
    

class ProfilePic(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profilepics")
    created_date=models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    followers = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name="followers")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.followers} followed {self.user}'
    