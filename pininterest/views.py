from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User
from pininterest.models import CommentReply, Follow, Post,Comment,Saved,ProfilePic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.decorators import action,api_view,permission_classes,authentication_classes,parser_classes
from pininterest.serializers import FollowSerializer, UserSerializer,PostSerializer,\
    CommentSerializer,SavedSerializer,PostCommentSerializer,\
    CommentReplySerializer,GetCommentReplySerializer,ProfilePicSerializer
from rest_framework import authentication,permissions
from datetime import timezone,timedelta,time,datetime,date
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
class UserCreateView(APIView):
    def post(self,request,*args, **kwargs):
        serializer= UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class PostView(ModelViewSet):
    serializer_class=PostSerializer
    queryset=Post.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data,context={"user":request.user,"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def list(self,request,*args, **kwargs):
        qs = Post.objects.exclude(user=request.user.id)
        serializer = PostSerializer(qs,many=True,context={"user":request.user,"request":request})
        return Response(data = serializer.data)
 

@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_my_posts(request,*args, **kwargs) :
    user = request.user
    qs = Post.objects.filter(user=user)
    serializer = PostSerializer(qs,many=True,context={"request":request})
    return Response(data=serializer.data)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def add_comment_view(request,*args, **kwargs):
    p_id = kwargs.get("post_id")
    p = Post.objects.get(id=p_id)
    usr = request.user
    serializer = PostCommentSerializer(data=request.data,context={"user":usr,"post":p,"request":request})
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data)
    else:
        return Response(data = serializer.errors)
        
@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def get_all_comments(request,*args, **kwargs):
    p_id = kwargs.get("post_id")
    post = Post.objects.get(id=p_id)
    qs = Comment.objects.filter(post = post)
    serializer = CommentSerializer(qs,many=True)
    return Response(data=serializer.data)

@api_view(['DELETE'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def remove_comment(request,*args, **kwargs):
    comment_id = kwargs.get("id")
    cmt = Comment.objects.get(id=comment_id)
    if cmt.user==request.user:
        cmt.delete()
        return Response(data="ok")
    else:
        return Response(data="you cannot delete this data")

# localhost:8000/postid/save
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def add_to_saved(request,*args, **kwargs):
    pid= kwargs.get("post_id")
    post = Post.objects.get(id=pid)
    serializer=SavedSerializer(data=request.data,context={"user":request.user,"post":post})
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data)
    else:
        return Response(data=serializer.errors)
        

@api_view(['DELETE'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def remove_from_saved(request,*args, **kwargs):
    saved_id = kwargs.get("id")
    saved_post = Saved.objects.get(id=saved_id)
    saved_post.delete()
    return Response(data='deleted')
    

# localhost:8000/savedposts
class SavedViewSet(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def list(self,request,*args, **kwargs):
        qs = Saved.objects.filter(user=request.user)
        serializer = SavedSerializer(qs,many=True,context={"request":request})
        return Response(data=serializer.data)
    
# localhost:8000/comments/id/add-reply/
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def add_reply_to_comment(request,*args, **kwargs):
    comment_id = kwargs.get("id")
    cmt = Comment.objects.get(id=comment_id)
    serializer = CommentReplySerializer(data=request.data,context={"user":request.user,"comment":cmt})
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data)
    else:
        return Response(data=serializer.errors)

# localhost:8000/comments/id/all-reply/
@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def get_reply_of_comment(request,*args, **kwargs):
    comment_id = kwargs.get("id")
    cmt = Comment.objects.get(id=comment_id)
    qs = CommentReply.objects.filter(comment=cmt)
    serializer = GetCommentReplySerializer(qs,many=True)
    return Response(data=serializer.data)


# localhost:8000/reply/id/remove-reply/
@api_view(['DELETE'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def remove_reply_of_comment(request,*args, **kwargs):
    reply_id = kwargs.get("id")
    reply=CommentReply.objects.get(id=reply_id)
    if reply.user==request.user:
        reply.delete()
        return Response(data="ok")
    else:
        return Response(data="you cannot delete this data")


@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def add_like_to_comment(request,*args, **kwargs):
    comment_id=kwargs.get("id")
    comment = Comment.objects.get(id=comment_id)
    user=request.user
    comment.like.add(user)
    comment.save()
    return Response(data='ok')



@api_view(["DELETE"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def remove_like_from_comment(request,*args, **kwargs):
    comment_id=kwargs.get("id")
    comment = Comment.objects.get(id=comment_id)
    user=request.user
    comment.like.remove(user)
    comment.save()
    return Response(data='ok')

@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def add_like_to_reply(request,*args, **kwargs):
    comment_reply_id=kwargs.get("id")
    comment_reply = CommentReply.objects.get(id=comment_reply_id)
    user=request.user
    comment_reply.like.add(user)
    comment_reply.save()
    return Response(data='ok')

@api_view(["DELETE"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def remove_like_from_reply(request,*args, **kwargs):
    comment_reply_id=kwargs.get("id")
    comment_reply = CommentReply.objects.get(id=comment_reply_id)
    user=request.user
    comment_reply.remove(user)
    comment_reply.save()
    return Response(data='ok')

@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def currentUser(request,*args, **kwargs):
    serializer=UserSerializer(request.user)
    return Response(data=serializer.data)
# localhost/changeprofilepic/

class ProfilePicView(ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    queryset=ProfilePic.objects.all()
    serializer_class=ProfilePicSerializer
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfilePicSerializer(data=request.data,context={"user":user,'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def update(self, request, *args, **kwargs):
        profilepic_id = kwargs.get("pk")
        instance = ProfilePic.objects.get(id=profilepic_id)
        serializer = ProfilePicSerializer(instance=instance,data=request.data,context={"user":request.user,'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = User.objects.get(id=user_id)
        try:
            qs = ProfilePic.objects.get(user = user)
            serializer = ProfilePicSerializer(qs,many=False,context={'request':request})
            return Response(data=serializer.data)
        except:
            return Response(data="no profilepicture")
@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def getTodayPosts(request,*args, **kwargs):
    today = date.today()
    yy = today.year
    dd = today.day
    mm = today.month
    fdate = f"{dd}/{mm}/{yy}"
    print(fdate)

@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_user_by_id(request,*args, **kwargs):
    user_id = kwargs.get("id")
    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user)
    return Response(data = serializer.data)

#localhost:8000/users/<int:user_id>/follow
class FollowView(ModelViewSet):
    serializer_class=FollowSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[ permissions.IsAuthenticatedOrReadOnly]
    queryset=Follow.objects.all()
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = FollowSerializer(data=request.data,context={
            'user':user
        })
    def list(self, request, *args, **kwargs):
        qs = Follow.objects.filter(followers=request.user)
        serializer = FollowSerializer(qs,many=True)
        return Response(data=serializer.data)
       
@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated]) 
def follow(request,*args, **kwargs):
    userid = kwargs.get("user_id")
    user = User.objects.get(id=userid)
    follower = request.user
    serializer = FollowSerializer(data=request.data,context={'user':user,'follower':follower})
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data)
    else:
        return Response(data=serializer.errors)
    
        

@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated]) 
def get_my_followers(request,*args, **kwargs):
    user = request.user
    qs = Follow.objects.filter(user = user)
    serializer = FollowSerializer(qs,many = True)
    return Response(data = serializer.data)

@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated]) 
def get_followers_by_id(request,*args, **kwargs):
    id = kwargs.get("user_id")
    user = User.objects.get(id=id)
    qs = Follow.objects.filter(user=user)
    serializer = FollowSerializer(qs,many = True)
    return Response(data = serializer.data) 