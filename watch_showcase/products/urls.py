from django.urls import path
from . import views
urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('watches/', views.WatchListView.as_view(), name='watch_list'),
    path('watches/<int:pk>/', views.WatchDetailView.as_view(), name='watch_detail'),
    path('search/', views.search_watches, name='search_watches'),
    # Watch group URLs
    path('groups/', views.WatchGroupListView.as_view(), name='group_list'),
    path('groups/create/', views.create_group, name='group_create'),
    path('groups/<slug:slug>/', views.WatchGroupDetailView.as_view(), name='group_detail'),
    path('groups/<slug:slug>/join/', views.join_group, name='join_group'),
    path('groups/<slug:slug>/leave/', views.leave_group, name='leave_group'),
    # Group categories
    path('groups/types/brand/', views.brand_groups, name='brand_groups'),
    path('groups/types/specialized/', views.specialized_groups, name='specialized_groups'),
    # Discussion URLs
    path('discussions/<int:pk>/', views.discussion_detail, name='discussion_detail'),
    path('discussions/create/<slug:group_slug>/', views.create_discussion, name='create_discussion'),
    path('discussions/<int:pk>/edit/', views.edit_discussion, name='edit_discussion'),
    path('discussions/<int:pk>/delete/', views.delete_discussion, name='delete_discussion'),
    # Comment URLs
    path('comments/add/<int:discussion_id>/', views.add_comment, name='add_comment'),
    path('comments/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    # Admin view
    path('feedback-report/', views.feedback_report, name='feedback_report'),
]