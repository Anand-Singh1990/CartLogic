from django.contrib import admin
from campaign.models import Campaign, CampaignCustomer, CampaignUsage


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("name", "discount_type", "sponsored_by", "total_budget", "budget_consumed", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active", "sponsored_by", "discount_type")


admin.site.register(CampaignCustomer)
admin.site.register(CampaignUsage)
