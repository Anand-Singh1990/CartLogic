from rest_framework import serializers
from campaign.constants import *
from campaign.models import Campaign


class ApplyDiscountSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    cart_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = serializers.DecimalField(max_digits=10, decimal_places=2)


class ApplyDiscountResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    discount_applied = serializers.DecimalField(max_digits=10, decimal_places=2)
    final_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    campaign_id = serializers.IntegerField()
    message = serializers.CharField()


class AvailableCampaignRequestSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()


class CampaignSerializer(serializers.ModelSerializer):
    remaining_budget = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "discount_type",
            "discount_value",
            "total_budget",
            "budget_consumed",
            "remaining_budget",
            "max_usage_per_customer_per_day",
            "sponsored_by",
            "discount_on"
        ]

    def get_remaining_budget(self, obj):
        return obj.total_budget - obj.budget_consumed
