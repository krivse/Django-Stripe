from django.db import models


class Item(models.Model):
    """Модель товаров."""
    choices = [
        ('USD', 'usd'),
        ('RUB', 'rub'),
    ]
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    price = models.IntegerField('Цена', help_text='Цена товара в центах')
    currency = models.CharField(
        'Валюта', max_length=3, default=choices[0], choices=choices, help_text='Выбор валюты для конвертации'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Order(models.Model):
    """Модель заказов."""
    item = models.ForeignKey(
        Item, verbose_name='Товары',
        related_name='orders',
        on_delete=models.CASCADE,
        help_text='Выбрать товар'
    )
    quantity = models.PositiveIntegerField('Кол-во позиций в заказе')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Discount(models.Model):
    """Модель скидка."""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, unique=True)
    amount = models.IntegerField('Скидка в %')

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Tax(models.Model):
    """Модель налог."""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, unique=True)
    amount = models.IntegerField('Налог в %')

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'
