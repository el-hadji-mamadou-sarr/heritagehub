from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from heritagehub.heritagehubapp.views import (
    FamillyViewSet,
    PersonViewSet,
    EventViewSet,
    MarriageViewSet,
    RelationViewSet,
    UserViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
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
]
