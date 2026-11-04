from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from reviews.views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("api/", include("api.urls")),
    path("quiz/", include("reviews.urls")),
    path("", include("cards.urls")),
]