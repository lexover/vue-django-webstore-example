from django.contrib import admin

from .models import ProductGroup
from .models import Product
from .models import ShippingAddress
from .models import Country
from .models import OrderItem
from .models import Order


class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    exclude = ('owner', )


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    # Fields 'price' and 'sale_price' is created programmatically from correspond product.
    # So this field should be read only.
    readonly_fields = ('price', 'sale_price')


# Admin view for order contain shipping address info and list of items
class OrderAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    inlines = [ShippingAddressInline, OrderItemsInline]
    readonly_fields = ('owner',)


admin.site.site_header = 'Pharmative Admin'
admin.site.site_title = 'Pharmative Amin Portal'
admin.site.index_title = 'Pharmative Amin Portal'

admin.site.register(ProductGroup)
admin.site.register(Product)
admin.site.register(Country)
admin.site.register(Order, OrderAdmin)
