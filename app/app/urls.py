from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from users.views import TokenObtainPairView

urlpatterns_ = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("auth/jwt/create/", TokenObtainPairView.as_view(), name="jwt-create"),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("djoser.urls")),
    path("", include("tasks.urls")),
]

urlpatterns = [path("api/", include(urlpatterns_))]
