from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<str:tag>', views.tag_view, name='tag'),
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('post/<int:id>', views.post_view, name='post'),
    path('delete/<int:id>', views.delete_post, name='delete'),
    path('edit/<int:id>', views.edit_post, name='edit'),
    path('like/', views.PostLikeToggle, name='PostLikeToggle'),
    path('notifications/', views.check_notifications, name='check_notifications'),
    path('notification/delete/<int:id>', views.delete_notification, name='delete_notification'),
    path('block-user/<int:id>', views.block_user, name='block_user'),
    path('blacklist/', views.check_blacklist, name='check_blacklist'),
    path('blacklist/remove/<int:id>', views.remove_from_blacklist, name='remove_from_blacklist'),
]
