from django.urls import path
from . import views

urlpatterns = [
    path("articles/", views.ArticleViewSet.as_view({"get": "list"})),
    path("articles/create/", views.ArticleCreateView.as_view()),
    path("articles/search/<str:query>/", views.SearchArticle.as_view()),
    path("articles/<str:friendly_url>/", views.ArticleDetailView.as_view()),
]
