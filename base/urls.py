from django.urls import path
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete,CustomLogin,Register,TaskReorder
from django.contrib.auth.views import LogoutView


urlpatterns = [
    
    path('login/',CustomLogin.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page = 'login'),name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('',TaskList.as_view(),name='task'),
    path('detail/<int:pk>/', TaskDetail.as_view(),name='detail'),
    path('create/',TaskCreate.as_view(),name='create-list'),
    path('update/<int:pk>/',TaskUpdate.as_view(),name='update-list'),
    path('delete/<int:pk>/',TaskDelete.as_view(),name='delete-list'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),

    
]


