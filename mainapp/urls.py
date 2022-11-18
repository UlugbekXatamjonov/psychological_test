from django.urls import path

from .views import ContactListView, ContactDetailView, PostListView, PostDetailView

app_name = 'mainapp'

urlpatterns = [
    path('post/<int:pk>/<slug:slug>/', PostDetailView.as_view()),
    path('post/', PostListView.as_view()),
	
	path('contact/<int:pk>/<slug:slug>/', ContactDetailView.as_view()),
    path('contact/', ContactListView.as_view()),
]

