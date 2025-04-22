from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from campaign.constants import *


class Campaign(models.Model):

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=25, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    sponsored_by = models.CharField(max_length=25, choices=CampaignSponsorTypeChoices.choices, default=CampaignSponsorTypeChoices.PLATFORM)
    discount_on = models.CharField(max_length=25, choices=CampaignDiscountOnChoices.choices)
    discount_type = models.CharField(max_length=25, choices = DiscountTypeChoices.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_budget = models.DecimalField(max_digits=12, decimal_places=2)
    budget_consumed = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    max_usage_per_customer_per_day = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def has_expired(self):
        return timezone.now() > self.end_date or self.budget_consumed >= self.total_budget
    
    class Meta:
        unique_together = ('status', 'name')
    


class CampaignCustomer(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='target_customers_rel')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('campaign', 'customer')


class CampaignUsage(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    usage_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('campaign', 'customer', 'date')

    @staticmethod
    def increment_usage(campaign, customer):
        today = timezone.now().date()
        usage, _ = CampaignUsage.objects.get_or_create(
            campaign=campaign,
            customer=customer,
            date=today,
            defaults={'usage_count': 0}
        )
        usage.usage_count += 1
        usage.save()


class DiscountApplication(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="applications")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discounts_applied")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.campaign.name} - {self.amount}"