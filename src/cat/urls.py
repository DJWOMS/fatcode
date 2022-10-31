from django.urls import path

from . import views

urlpatterns = [
    path('product/', views.ProductView.as_view()),
    path('get_hint/', views.HintView.as_view()),
    path('inventory/<int:pk>/', views.InventoryView.as_view({"post": "create", "get": "list", 'patch': 'update'})),
    path('phrases/', views.PhraseView.as_view()),
    path('cats/', views.CatView.as_view({"get": "list"})),
    path('cats/<int:pk>/', views.CatView.as_view({"get": "retrieve"})),
    path('your_cat/', views.CatUserView.as_view()),
    path('your_cat/<int:pk>', views.UpdateCatUserView.as_view()),
]
