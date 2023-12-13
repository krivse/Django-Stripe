from rest_framework import serializers

from .models import Item, Order


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    """Сериалайзер модели Item."""
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'currency']


class OrderSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Product."""
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        """Создание или обновление заказа."""
        item = validated_data.get('item')
        quantity = validated_data.get('quantity')
        order = Order.objects.filter(item=item.id)
        if not order.exists():
            return super().create(validated_data)
        else:
            quantity += order.first().quantity
            validated_data.update({'quantity': quantity})
            return super().update(order.first(), validated_data)
