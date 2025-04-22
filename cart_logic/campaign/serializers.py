from rest_framework import serializers
from campaign.constants import *
from campaign.models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    campaign_id = serializers.IntegerField(source="id")

    class Meta:
        model = Campaign
        fields = ["campaign_id", "name", "discount_type", "discount_value", "valid_until"]


