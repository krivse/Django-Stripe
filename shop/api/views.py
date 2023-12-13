import os

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .serializers import ItemSerializer, OrderSerializer
from .models import Item, Order
from .stripe import get_session_id
from .templates_renderer import ItemsTemplateHTMLRender, OrdersTemplateHTMLRender


class ItemViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """Один товар."""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'item.html'


class BuyViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """Покупка товара"""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'checkout.html'

    def retrieve(self, request, *args, **kwargs):
        """
        Переопределение метода с целью получения session_id из модуля Stripe
        для последующего редиректа на страницу оплаты товарной единицы.
        """
        currency = self.request.GET.get('currency', 'usd').lower()

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            instance = serializer.data
            instance['quantity'] = self.request.GET.get('quantity')
            items = [instance]
            self.calculate(currency, instance, instance.get('currency'))
            instance['currency'] = currency
        except:
            items = []
            instance = Item.objects.all()
            for item in instance:
                serializer = self.get_serializer(item)
                instance = serializer.data

                try:
                    instance['quantity'] = item.orders.get().quantity
                except ObjectDoesNotExist:
                    continue
                try:
                    instance['tax'] = item.orders.get().tax.amount
                except ObjectDoesNotExist:
                    instance['tax'] = None
                try:
                    instance['discount'] = item.orders.get().discount.amount
                except ObjectDoesNotExist:
                    instance['discount'] = None

                instance['currency'] = currency
                self.calculate(currency, instance, item.currency)
                items.append(instance)

        session_id = get_session_id(items)

        return Response({'session_id': session_id, 'pk_key': os.getenv('PK_KEY')})

    @staticmethod
    def calculate(currency, instance, item_currency):
        price = instance['price']
        if currency == 'usd':
            instance['price'] = (
                round(price * 100, 2) if item_currency.lower() == currency else round(price / 89 * 100, 2)
            )
        else:
            instance['price'] = (
                round(price / 89 * 100, 2) if item_currency.lower() == currency else round(price * 100, 2)
            )


class ItemsViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """Список товаров."""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    renderer_classes = [ItemsTemplateHTMLRender]
    template_name = 'items.html'


class OrderViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Список заказов."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    renderer_classes = [OrdersTemplateHTMLRender]
    template_name = 'order.html'

    def dispatch(self, request, *args, **kwargs):
        """Переопределяем dispatch, чтобы корректно перенаправить запрос,"""
        method = self.request.POST.get('_method', '')
        if method == 'delete':
            return self.destroy(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        self.perform_create(serializer)
        return HttpResponseRedirect(redirect_to='/')

    def get_object(self):
        item = get_object_or_404(Item, pk=self.kwargs.get('pk'))
        return Order.objects.filter(item=item.id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return HttpResponseRedirect(redirect_to='/')
