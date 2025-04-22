from campaign.paginations import CampaignPagination
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date
from campaign.constants import StatusChoices
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Campaign, DiscountApplication
from .serializers import (
    ApplyDiscountSerializer,
    ApplyDiscountResponseSerializer,
    AvailableCampaignRequestSerializer,
    CampaignSerializer
)


@swagger_auto_schema(request_body=CampaignSerializer)
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



class ApplyDiscountView(APIView):

    @swagger_auto_schema(request_body=ApplyDiscountSerializer,responses={
        status.HTTP_200_OK: ApplyDiscountResponseSerializer,
        status.HTTP_400_BAD_REQUEST: 'No eligible campaigns found.',
        status.HTTP_500_INTERNAL_SERVER_ERROR: 'An unexpected error occurred'
    })
    def post(self, request):
        try:
            serializer = ApplyDiscountSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            customer_id = serializer.validated_data["customer_id"]
            cart_total = serializer.validated_data["cart_total"]
            delivery_charge = serializer.validated_data["delivery_charge"]

            try:
                customer = User.objects.get(id=customer_id)
            except User.DoesNotExist:
                return Response(
                    {"error": "Customer does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )

            today = date.today()
            applications_today = DiscountApplication.objects.filter(
                customer=customer,
                created_at__date=today
            ).count()

            active_campaigns = Campaign.objects.filter(
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now(),
                status=StatusChoices.ACTIVE,
                target_customers_rel__customer=customer,
            )

            for campaign in active_campaigns:
                remaining_budget = campaign.total_budget - campaign.budget_consumed
                if remaining_budget <= 0:
                    continue

                if applications_today >= campaign.max_usage_per_customer_per_day:
                    continue

                if campaign.discount_type == "cart":
                    discount = min(cart_total, campaign.discount_value)
                else:  # delivery
                    discount = min(delivery_charge, campaign.discount_value)

                final_amount = cart_total + delivery_charge - discount

                DiscountApplication.objects.create(
                    campaign=campaign,
                    customer=customer,
                    amount=discount
                )

                campaign.budget_consumed += discount
                if campaign.budget_consumed >= campaign.total_budget:
                    campaign.status = StatusChoices.INACTIVE
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

        except ValidationError as ve:
            return Response(
                {"error": "Invalid input", "details": ve.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class AvailableCampaignsView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('discount_code', openapi.IN_QUERY, description="Discount code to apply", type=openapi.TYPE_STRING),
        ],
        responses={
            status.HTTP_200_OK: CampaignSerializer,
            status.HTTP_404_NOT_FOUND: 'Invalid input.',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'An unexpected error occurred.'
        }
    )
    def get(self, request):
        try:
            serializer = AvailableCampaignRequestSerializer(data=request.GET.dict())
            serializer.is_valid(raise_exception=True)

            customer_id = serializer.validated_data["customer_id"]

            try:
                customer = User.objects.get(id=customer_id)
            except User.DoesNotExist:
                return Response(
                    {"error": "Customer does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )

            active_campaigns = Campaign.objects.filter(
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now(),
                status=StatusChoices.ACTIVE,
                target_customers_rel__customer=customer,
            )

            eligible_campaigns = [
                campaign for campaign in active_campaigns
                if (campaign.total_budget - campaign.budget_consumed) > 0
            ]

            serialized = CampaignSerializer(eligible_campaigns, many=True)
            return Response(serialized.data)

        except ValidationError as ve:
            return Response(
                {"error": "Invalid input", "details": ve.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )