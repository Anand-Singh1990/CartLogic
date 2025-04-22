from rest_framework import viewsets
from campaign.models import Campaign
from rest_framework.response import Response
from campaign.serializers import CampaignSerializer
from campaign.paginations import CampaignPagination
from rest_framework import status

from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Campaign, DiscountApplication
from .serializers import (
    ApplyDiscountSerializer,
    ApplyDiscountResponseSerializer,
    AvailableCampaignRequestSerializer,
    CampaignSerializer,
)




class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    pagination_class = CampaignPagination

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "success": True,
            "message": f"Campaign '{instance.name}' deleted successfully."
        }, status=status.HTTP_200_OK)



@api_view(["POST"])
def apply_discount(request):
    serializer = ApplyDiscountSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    customer_id = serializer.validated_data["customer_id"]
    cart_total = serializer.validated_data["cart_total"]
    delivery_charge = serializer.validated_data["delivery_charge"]

    try:
        customer = User.objects.get(id=customer_id)
    except User.DoesNotExist:
        return Response({"error": "Customer does not exist."}, status=status.HTTP_404_NOT_FOUND)

    today = date.today()
    applications_today = DiscountApplication.objects.filter(
        customer=customer,
        created_at__date=today
    ).count()

    active_campaigns = Campaign.objects.filter(
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now(),
        is_active=True,
        target_customers=customer,
    )

    for campaign in active_campaigns:
        # Calculate remaining budget dynamically
        remaining_budget = campaign.total_budget - campaign.budget_consumed

        if remaining_budget <= 0:
            continue

        if applications_today >= campaign.max_usage_per_customer_per_day:
            continue

        if campaign.discount_type == "cart":
            discount = min(cart_total, campaign.discount_value)
        else:  # "delivery"
            discount = min(delivery_charge, campaign.discount_value)

        final_amount = cart_total + delivery_charge - discount

        # Apply the discount
        DiscountApplication.objects.create(
            campaign=campaign,
            customer=customer,
            amount=discount
        )

        campaign.budget_consumed += discount
        if campaign.budget_consumed >= campaign.total_budget:
            campaign.is_active = False
        campaign.save()

        response_data = {
            "success": True,
            "discount_applied": discount,
            "final_amount": final_amount,
            "campaign_id": campaign.id,
            "message": "Discount applied successfully"
        }

        response_serializer = ApplyDiscountResponseSerializer(response_data)
        return Response(response_serializer.data)

    return Response(
        {"success": False, "message": "No eligible campaigns found."},
        status=status.HTTP_404_NOT_FOUND
    )


@api_view(["POST"])
def available_campaigns(request):
    serializer = AvailableCampaignRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    customer_id = serializer.validated_data["customer_id"]

    try:
        customer = User.objects.get(id=customer_id)
    except User.DoesNotExist:
        return Response({"error": "Customer does not exist."}, status=status.HTTP_404_NOT_FOUND)

    active_campaigns = Campaign.objects.filter(
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now(),
        is_active=True,
        target_customers=customer,
    )

    eligible_campaigns = []
    for campaign in active_campaigns:
        remaining_budget = campaign.total_budget - campaign.budget_consumed
        if remaining_budget > 0:
            eligible_campaigns.append(campaign)

    serialized = CampaignSerializer(eligible_campaigns, many=True)
    return Response(serialized.data)
