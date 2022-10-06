from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.ProductView.as_view()),
    path('get_hint/', views.HintView.as_view()),
    path('inventory/<int:id>/', views.InventoryView.as_view({"post": "create", "get": "list"})),
]