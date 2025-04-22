from datetime import date
from django.utils import timezone
from rest_framework import status as rest_status
from campaign.models import Campaign, CampaignUsage, DiscountApplication


class DiscountHandler:

    @classmethod
    def get_best_discount(cls, customer, cart_total, delivery_fee, sponsor_filter=None):
        try:
            now = timezone.now()
            today = now.date()

            # Get eligible campaigns based on the current date
            eligible_campaigns = Campaign.objects.filter(
                is_active=True,
                start_date__lte=now,
                end_date__gte=now
            )

            if sponsor_filter:
                eligible_campaigns = eligible_campaigns.filter(sponsored_by=sponsor_filter)

            best_campaign = None
            max_saving = 0
            final_cart = cart_total
            final_delivery = delivery_fee

            # Iterate over eligible campaigns to check discount eligibility and calculate savings
            for campaign in eligible_campaigns:
                # Check if the customer is eligible (check if they are a target customer for this campaign)
                if campaign.target_customers.exists() and customer not in campaign.target_customers.all():
                    continue

                # Check if the campaign's total budget has been consumed
                if campaign.total_budget and campaign.budget_consumed >= campaign.total_budget:
                    continue

                # Check the usage limit: How many times has this customer used the campaign today?
                usage = CampaignUsage.objects.filter(campaign=campaign, customer=customer, date=today).first()
                if usage and usage.usage_count >= campaign.max_usage_per_customer_per_day:
                    continue

                # Calculate potential discount for this campaign
                cart_discount = 0
                delivery_discount = 0

                if campaign.discount_type == 'cart':
                    cart_discount = min(campaign.discount_value, cart_total) if not campaign.is_percentage else (cart_total * campaign.discount_value / 100)
                elif campaign.discount_type == 'delivery':
                    delivery_discount = min(campaign.discount_value, delivery_fee) if not campaign.is_percentage else (delivery_fee * campaign.discount_value / 100)

                total_saving = cart_discount + delivery_discount

                # Track the best discount (maximum savings)
                if total_saving > max_saving:
                    max_saving = total_saving
                    final_cart = cart_total - cart_discount
                    final_delivery = delivery_fee - delivery_discount
                    best_campaign = campaign

            # Return the final cart and delivery fee after applying the best discount
            return {
                'final_cart_total': final_cart,
                'final_delivery_fee': final_delivery,
                'discount_applied': max_saving,
                'campaign': best_campaign
            }
        except Exception as e:
            raise Exception(str(e))


    def apply_discount(cls, customer, cart_total, delivery_fee, campaign_id=None):
        try:
            """
            Applies the best discount for the customer based on the current campaigns.
            """
            best_discount = cls.get_best_discount(customer, cart_total, delivery_fee)

            if best_discount['discount_applied'] > 0:
                DiscountApplication.objects.create(
                    campaign=best_discount['campaign'],
                    customer=customer,
                    amount=best_discount['discount_applied']
                )

                best_discount['campaign'].budget_consumed += best_discount['discount_applied']
                best_discount['campaign'].save()

                CampaignUsage.increment_campaign_usage(best_discount['campaign'], customer)

                return rest_status.HTTP_200_OK, "Success",{
                    'message': 'Discount applied successfully',
                    'applied_discount': best_discount['discount_applied'],
                    'final_cart_total': best_discount['final_cart_total'],
                    'final_delivery_fee': best_discount['final_delivery_fee']
                }

            return rest_status.HTTP_200_OK, "Success", {'message': 'No eligible discount found'}

        except Exception as e:
            return rest_status.HTTP_400_BAD_REQUEST, "Failure", {"error_text":str(e)}