from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from heritagehub.heritagehubapp.views import (
    FamillyViewSet,
    PersonViewSet,
    EventViewSet,
    MarriageViewSet,
    RelationViewSet,
    UserViewSet,
    LogoutView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title='ESTIAM API',
        default_version='V1'
    ),
    public=True,
)

router = routers.DefaultRouter()
router.register(r'famillies', FamillyViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'events', EventViewSet)
router.register(r'marriages', MarriageViewSet)
router.register(r'relations', RelationViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
