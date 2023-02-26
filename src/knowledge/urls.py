from django.urls import path

from src.knowledge import views

urlpatterns = [
    path('category/', views.CategoryView.as_view({"get": "list"}), name='category-list'),
    path('article/', views.ArticleView.as_view({"get": "list"}), name="article-list"),
    path('article/<int:pk>/', views.ArticleView.as_view({"get": "retrieve"}), name="article-detail"),
    path('article/<int:pk>/comment/', views.CommentsView.as_view(
        {"get": "list", "post": "create"}
        ), name="article_comment"),
    path('article/<int:pk>/comment/<int:comment_pk>/', views.CommentsView.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
            ), name="comment_detail"),
    path('article/<int:pk>/like/', views.LikeDislikeView.as_view(
            {"get": "list", "post": "create"}
        ), name="article_like"),
    path('article/<int:pk>/like/<int:like_pk>/', views.LikeDislikeView.as_view({"put": "update"}), name="like_update"),
    path('tag/', views.TagListView.as_view(), name="tag-list"),
    path('letters/', views.GlossaryLetterListView.as_view(), name='glossary-letter'),
    path('glossary/', views.GlossaryArticleListView.as_view(), name='glossary-list'),
]
