from django.db import models

class StatusChoices(models.TextChoices):

    ACTIVE = 'Active', 'active'
    INACTIVE = 'inactive', 'Inactive'
    DELETED = 'deleted', 'Deleted'


class CampaignDiscountOnChoices(models.TextChoices):

    CART = 'cart', 'Cart Discount'
    DELIVERY = 'delivery', 'Delivery Discount'


class CampaignSponsorTypeChoices(models.TextChoices):

    VENDOR = 'vendor', 'Vendor'
    PRODUCT_GROUP = 'product_group', 'Product Group'
    PLATFORM = 'platform', 'Platform'


class DiscountTypeChoices(models.TextChoices):

    NET_PERCENTAGE = 'net_percentage', 'Net Percentage'
    PERCENTAGE_WITH_LIMIT = 'percentage_with_limit', "Percentage with limit"
    NET_AMOUNT = 'amount', 'net_amount'