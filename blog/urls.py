from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView, BlogListView

app_name = BlogConfig.name

urlpatterns = [
    path('view/<int:pk>/', BlogDetailView.as_view(), name='view'),
    path('', BlogListView.as_view(), name='list'),
    path('create/', BlogCreateView.as_view(), name='create'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete')

]