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

urlpatterns = [
    path('', include(router.urls)),
    path('users/auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
