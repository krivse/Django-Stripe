from rest_framework.renderers import TemplateHTMLRenderer

from .models import Order


class ItemsTemplateHTMLRender(TemplateHTMLRenderer):
    """Переделяем базовый шаблон для рендеринга страниц и передаём словарь."""
    def get_template_context(self, data, renderer_context):
        quantity = sum(order.quantity for order in Order.objects.all())
        items = super().get_template_context(data, renderer_context)

        return {'items': items, 'quantity': quantity}


class OrdersTemplateHTMLRender(TemplateHTMLRenderer):
    """Переделяем базовый шаблон для рендеринга страниц и передаём словарь."""
    def get_template_context(self, data, renderer_context):
        orders = Order.objects.all()
        context = []
        for i in orders:
            name = i.item.name
            quantity = i.quantity
            currency = i.item.currency
            summ = quantity * i.item.price

            context.append({
                'name': name,
                'quantity': quantity,
                'currency': currency,
                'summ_dollar': summ if currency == 'USD' else round(summ / 90, 2),
                'summ_rub': summ if currency == 'RUB' else round(summ * 90),
            })
        total_price_usd = round(sum(i.get('summ_dollar') for i in context), 2)
        total_price_rub = round(sum(i.get('summ_rub') for i in context), 2)

        return {'orders': context, 'total_price_rub': total_price_rub, 'total_price_usd': total_price_usd}
