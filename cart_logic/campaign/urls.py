from django.urls import path, include
from rest_framework.routers import DefaultRouter
from campaign.views import *

router = DefaultRouter()
router.register('campaigns', CampaignViewSet, basename='campaigns')

urlpatterns = [
    path('', include(router.urls)),
    path("apply-discount/", ApplyDiscountView.as_view(), name="apply-discount"),
    path("available-campaigns/", AvailableCampaignsView.as_view(), name="available-campaigns"),
]