from rest_framework import viewsets
from campaign.models import Campaign
from campaign.serializers import CampaignSerializer
from campaign.paginations import CampaignPagination

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    pagination_class = CampaignPagination