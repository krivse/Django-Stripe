import os

import stripe


def get_session_id(items: list) -> str:
    stripe.api_key = os.getenv('SK_KEY')
    line_items = []
    coupon = None
    for i in range(len(items)):

        # Рассчитать Tax
        tax_rate = items[i].get('tax')
        if tax_rate is not None:
            tax_rate = [stripe.TaxRate.create(
                display_name='Tax',
                percentage=items[i].get('tax'),
                inclusive=False
            )['id']]

        # Рассчитать Discount
        discount = items[i].get('discount')
        if discount is not None:
            coupon = stripe.Coupon.create(
                percent_off=discount,
                duration='once',
            ).id

        price = int(items[i].get('price'))
        line_items.append({
            'price_data': {
                'currency': items[i].get('currency'),
                'unit_amount': price if items[i].get('currency') == 'usd' else price * 89,
                'product_data': {
                    'name': items[i].get('name'),
                    'description': items[i].get('description'),
                },
            },
            'quantity': int(items[i].get('quantity')),
            'tax_rates': tax_rate
        })
    session = stripe.checkout.Session.create(
        line_items=line_items,
        discounts=[{
            'coupon': coupon
        }],
        mode='payment',
        success_url='https://127.0.0.1/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://45.12.238.205/',
    )

    return session.get('id')
