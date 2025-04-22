from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from campaign.models import Campaign, CampaignCustomer, DiscountApplication
from django.utils import timezone
from datetime import timedelta
import random
from decimal import Decimal
from campaign.constants import StatusChoices, CampaignSponsorTypeChoices, CampaignDiscountOnChoices, DiscountTypeChoices


class Command(BaseCommand):
    help = "Creates dummy campaigns, users, and related data"

    def handle(self, *args, **options):
        # Create Users
        self.stdout.write("Creating users...")
        users = []
        for i in range(5):
            user, _ = User.objects.get_or_create(
                username=f"user{i+1}",
                defaults={"email": f"user{i+1}@example.com", "password": "pass1234"}
            )
            users.append(user)

        # Create Campaigns
        self.stdout.write("Creating campaigns...")
        for j in range(3):
            campaign = Campaign.objects.create(
                name=f"Campaign {j+1}",
                status=StatusChoices.ACTIVE,
                sponsored_by=CampaignSponsorTypeChoices.PLATFORM,
                discount_on=CampaignDiscountOnChoices.CART,
                discount_type=DiscountTypeChoices.NET_PERCENTAGE,
                discount_value=Decimal("50.00"),
                start_date=timezone.now() - timedelta(days=1),
                end_date=timezone.now() + timedelta(days=10),
                total_budget=Decimal("1000.00"),
                budget_consumed=Decimal("0.00"),
                max_usage_per_customer_per_day=3,
            )
            self.stdout.write(f"Created campaign: {campaign.name}")

            # Assign campaign to random customers
            target_users = random.sample(users, 3)
            for user in target_users:
                CampaignCustomer.objects.get_or_create(campaign=campaign, customer=user)
                self.stdout.write(f"  Linked {user.username} to {campaign.name}")

            # Add some discount applications
            for user in target_users[:2]:  # Only first 2 get applied
                DiscountApplication.objects.create(
                    campaign=campaign,
                    customer=user,
                    amount=Decimal("50.00")
                )
                campaign.budget_consumed += Decimal("50.00")
                campaign.save()
                self.stdout.write(f"  Discount applied for {user.username} on {campaign.name}")

        self.stdout.write(self.style.SUCCESS("✅ Dummy data created successfully!"))