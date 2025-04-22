import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from campaign.models import Campaign, DiscountApplication

class Command(BaseCommand):
    help = "Create dummy users, campaigns, and discount applications"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating dummy users...")
        users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f"user{i}",
                defaults={
                    "email": f"user{i}@example.com",
                    "password": "password123"  # not hashed, for testing only
                }
            )
            users.append(user)

        self.stdout.write("Creating dummy campaigns...")
        for i in range(3):
            campaign = Campaign.objects.create(
                name=f"Campaign {i+1}",
                discount_type=random.choice(["cart", "delivery"]),
                discount_value=random.randint(50, 300),
                total_budget=random.randint(1000, 5000),
                budget_consumed=0,
                start_date=timezone.now() - timedelta(days=1),
                end_date=timezone.now() + timedelta(days=10),
                is_active=True,
                max_usage_per_customer_per_day=2,
                sponsored_by="TestSponsor",
                is_percentage=False,
            )
            # Randomly assign users
            campaign.target_customers.set(random.sample(users, k=random.randint(1, len(users))))
            campaign.save()

        self.stdout.write("Creating dummy discount applications...")
        campaigns = Campaign.objects.all()
        for user in users:
            for campaign in campaigns:
                if user in campaign.target_customers.all():
                    DiscountApplication.objects.create(
                        customer=user,
                        campaign=campaign,
                        amount=random.randint(10, 100),
                    )
                    campaign.budget_consumed += 50
                    campaign.save()

        self.stdout.write(self.style.SUCCESS("Dummy data created successfully."))