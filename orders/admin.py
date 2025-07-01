from django.contrib import admin
from .models import Order, Address, OrderedItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'order_status_display', 'total_price', 'created_at', 'updated_at', 'delete_status_display')
    list_filter = ('order_status', 'delete_status', 'created_at')
    search_fields = ('owner__user__username', 'owner__user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def order_status_display(self, obj):
        return obj.get_order_status_display()
    order_status_display.short_description = 'Status'

    def delete_status_display(self, obj):
        return obj.get_delete_status_display()
    delete_status_display.short_description = 'Deleted'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'city', 'state', 'postal_code', 'country', 'owner', 'order')
    list_filter = ('state', 'country', 'created_at')
    search_fields = ('full_name', 'phone', 'city', 'state', 'postal_code')
    ordering = ('-created_at',)


@admin.register(OrderedItem)
class OrderedItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'size', 'owner')
    list_filter = ('size',)
    search_fields = ('product__name',)
