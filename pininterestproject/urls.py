"""pininterestproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from pininterest import views
from rest_framework.authtoken import views as authview
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("posts",views.PostView,basename="follow")
router.register('savedposts',views.SavedViewSet,basename='saved')
router.register('profilepic',views.ProfilePicView,basename='profilepicchange')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.UserCreateView.as_view()),
    path('token/',authview.obtain_auth_token),
    path('posts/<int:post_id>/add-comment/',views.add_comment_view),
    path('posts/<int:post_id>/comments/',views.get_all_comments),
    path('posts/<int:post_id>/save/',views.add_to_saved),
    path('savedposts/<int:id>/remove/',views.remove_from_saved),
    path('myposts/',views.get_my_posts),
    path("comments/<int:id>/add-reply/",views.add_reply_to_comment),
    path("comments/<int:id>/all-reply/",views.get_reply_of_comment),
    path("comments/<int:id>/remove/",views.remove_comment),
    path("reply/<int:id>/remove-reply/",views.remove_reply_of_comment),
    path("comments/<int:id>/add-like/",views.add_like_to_comment),
    path("comments/<int:id>/remove-like/",views.remove_like_from_comment),
    path("currentuser/",views.currentUser),
    path("reply/<int:id>/add-like/",views.add_like_to_reply),
    path("reply/<int:id>/remove-like/",views.remove_like_from_reply),
    path('user/<int:id>/',views.get_user_by_id),
    path('user/<int:user_id>/follow/',views.follow),
    path('my_followers/',views.get_my_followers),
    path('user/<int:user_id>/followers/',views.get_followers_by_id),
    path('',include(router.urls))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
