from django.contrib import admin
from campaign.models import Campaign, CampaignCustomer, CampaignUsage

admin.site.register(Campaign)
admin.site.register(CampaignCustomer)
admin.site.register(CampaignUsage)
