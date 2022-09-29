from django.urls import path
from . import views

urlpatterns = [
    path('card/', views.CardView.as_view({'post': 'create'})),
    path('card/<int:pk>/', views.CardView.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
    )),
    path('column/', views.ColumnView.as_view({'post': 'create'})),
    path('column/<int:pk>/', views.ColumnView.as_view({'put': 'update', 'delete': 'destroy'})),
    path('label/', views.LabelView.as_view({'post': 'create'})),
    path('label/<int:board_id>/', views.LabelView.as_view({'get': 'list', 'delete': 'destroy'})),
    path('<int:project_id>/', views.BoardView.as_view({'get': 'retrieve', 'post': 'create'})),
]
