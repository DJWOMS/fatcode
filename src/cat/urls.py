from django.urls import path
from . import views

urlpatterns = [
    path('inventory/<int:id>/', views.CheckInventoryView.as_view()),
]