from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RuleViewSet, UserAttributeViewSet

router = DefaultRouter()
router.register(r'rules', RuleViewSet, basename='rule')
router.register(r'user_attributes', UserAttributeViewSet, basename='user_attribute')

urlpatterns = [
    path('', include(router.urls)),
]
