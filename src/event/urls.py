from django.urls import path

from src.event import views


urlpatterns = [
    path('', views.EventView.as_view({"get": "list", "post": "create"}), name='event'),
    path('<int:pk>/', views.EventView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
         name='detail_event'),
]