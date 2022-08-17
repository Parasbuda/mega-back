from django.urls import path, include

urlpatterns = [
    path("core-app/", include("core.urls")),
    path("user-app/", include("user.urls")),
]
