from pininterest.models import Follow, Post,Comment,Saved,CommentReply,ProfilePic
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields=["id","username","first_name","last_name","email","password"]
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
    image_url = serializers.SerializerMethodField("get_image_url")
    class Meta:
        model = Post
        fields = ['id','user','post_title','post_img','created_date','description','destination_link',"image_url"]
    def create(self, validated_data):
        usr=self.context.get("user")
        return Post.objects.create(**validated_data,user=usr)
    def get_image_url(self,obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.post_img.url)
    

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
    post = serializers.CharField(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"
    def create(self, validated_data):
        usr=self.context.get("user")
        p = self.context.get("post")
        return Comment.objects.create(**validated_data,user=usr,post=p)

class PostCommentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
    post = serializers.CharField(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"
    def create(self, validated_data):
        usr=self.context.get("user")
        p = self.context.get("post")
        return Comment.objects.create(**validated_data,user=usr,post=p)

class SavedSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    post = PostSerializer(many=False,read_only=True)
    class Meta:
        model = Saved
        fields='__all__'
    def create(self, validated_data):
        usr = self.context.get("user")
        p = self.context.get("post")
        try:
            qs = Saved.objects.get(post=p)
            return 0
        except:
            return Saved.objects.create(**validated_data,user=usr,post=p)


class CommentReplySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    comment=serializers.CharField(read_only=True)
    class Meta:
        model = CommentReply
        fields=['id','comment','user','created_date','reply']
    def create(self, validated_data):
        user = self.context.get("user")
        comment = self.context.get("comment")
        return CommentReply.objects.create(**validated_data,user=user,comment=comment)

class GetCommentReplySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    comment=serializers.CharField(read_only=True)
    class Meta:
        model = CommentReply
        fields=['id','comment','user','created_date','reply','like']
    def create(self, validated_data):
        user = self.context.get("user")
        comment = self.context.get("comment")
        return CommentReply.objects.create(**validated_data,user=user,comment=comment)

class ProfilePicSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    image_url = serializers.SerializerMethodField("get_image_url")
    class Meta:
        model = ProfilePic
        fields=['id','user','profile_pic','created_date','image_url']
    def create(self, validated_data):
        user = self.context.get("user")
        return ProfilePic.objects.create(**validated_data,user=user)
    def get_image_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.profile_pic.url) 
        
class FollowSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers = UserSerializer(read_only=True)
    class Meta:
        model = Follow
        fields="__all__"
    def create(self, validated_data):
        usr = self.context.get("user")
        follower = self.context.get("follower")
        return Follow.objects.create(**validated_data,user=usr,followers=follower)
            
            
