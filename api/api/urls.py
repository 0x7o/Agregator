from django.urls import path, include

urlpatterns = [path("endpoints/", include("endpoints.urls"))]
