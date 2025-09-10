from django.urls import path
from . import views

app_name = 'prints'

urlpatterns = [
    path('', views.home, name='home'),
    path('prints/', views.print_list, name='print_list'),
    path('prints/<int:pk>/', views.print_detail, name='print_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('prints/<int:pk>/like/', views.like_print, name='like_print'),
    path('prints/<int:pk>/comment/', views.add_comment, name='add_comment'),
]
