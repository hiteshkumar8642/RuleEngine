from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RuleViewSet, UserAttributeViewSet

router = DefaultRouter()
router.register(r'rules', RuleViewSet)
router.register(r'user-attributes', UserAttributeViewSet)

urlpatterns = router.urls
