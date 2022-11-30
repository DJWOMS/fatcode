from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryView.as_view({"get": "list"}), name="categories"),
    path('reports/', views.ReportView.as_view({"get": "list", "post": "create"}), name="reports"),
    path('reports/<int:pk>/', views.ReportView.as_view({"get": "retrieve"}), name="reports-detail")
]
