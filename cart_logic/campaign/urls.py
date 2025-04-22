from django.urls import path, include
from rest_framework.routers import DefaultRouter
from campaign.views import *

router = DefaultRouter()
router.register('campaigns', CampaignViewSet, basename='campaigns')

urlpatterns = [
    path('', include(router.urls)),
]