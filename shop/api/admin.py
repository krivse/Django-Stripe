from django.contrib import admin

from .models import Item, Order, Discount, Tax


class ItemAdmin(admin.ModelAdmin):
    """Админ-зона для товаров."""
    list_display = ('id', 'name', 'description', 'price', 'currency')
    search_fields = ('name', 'price', 'currency')


class OrderAdmin(admin.ModelAdmin):
    """Админ-зона для заказов."""
    list_display = ('id', 'item', 'quantity')
    search_fields = ('item', 'quantity')


class DiscountAdmin(admin.ModelAdmin):
    """Админ-зона для скидок."""
    list_display = ('id', 'amount')


class TaxAdmin(admin.ModelAdmin):
    """Админ-зона для налога."""
    list_display = ('id', 'amount')


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Tax, TaxAdmin)
