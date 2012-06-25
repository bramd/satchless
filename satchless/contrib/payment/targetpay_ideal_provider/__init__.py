from django.forms import Form
from django.utils.translation import ugettext_lazy as _

import urlparse
from targetpay.base import TargetPayException

from ....payment import (PaymentProvider, PaymentFailure, 
        PaymentType, ConfirmationFormNeeded)
from . import forms
from . import models
from . import settings

class TargetpayIdealProvider(PaymentProvider):
    form_class = forms.TargetpayIdealPaymentForm

    # Callable that returns the URL to redirect to after a payment has been processed
    # Please note that the view at this URL is responsible for checking payment
    # status and updating the order status
    get_redirect_url = None

    def enum_types(self, order=None, customer=None):
        yield PaymentType(provider=self, typ='targetpay_ideal', name='Ideal')

    def get_configuration_form(self, order, typ, data):
        instance = self.payment_class(order=order)
        return self.form_class(data or None, instance=instance)

    def save(self, order, form, typ=None):
        order.payment_price = 0
        order.payment_type_name = 'Ideal'
        order.payment_type_description = ''
        if form.is_valid():
            form.save()
        else:
            raise PaymentFailure(_("Could not create Ideal Variant"))

    def confirm(self, order, typ=None):
        v = order.paymentvariant
        amount = int(order.get_total().gross * 100) # in cents
        v.amount = amount
        v.description = 'Order %d' % order.id
        try:
            v.transaction_id, v.redirect_url = settings.ideal.startPayment(
                    v.issuer.issuer_id, v.description, v.amount,
                    self.get_redirect_url(order))
        except TargetPayException, e:
            v.result_code = e.args[0]
            raise PaymentFailure(e)
        finally:
            v.save()
        base_url = v.redirect_url.split('?')[0]
        url_params = urlparse.parse_qsl(urlparse.urlparse(v.redirect_url).query)
        raise ConfirmationFormNeeded(forms.TargetpayIdealRedirectForm(url_params,
        auto_id=False), base_url, 'GET')

    def update_order_status(self, order):
        """Set the order status to payment-complete or payment-failed

        This function expects an order instance with a paymentvariant that has
        a set transaction_id.
        E.g. call this function after the payment has been processed to check
        the result and update the order accordingly.
        """
        v = order.paymentvariant
        try:
            settings.ideal.checkPayment(v.transaction_id)
            order.status = 'payment-complete'
        except TargetpayException, e:
            order.status = 'payment-failed'
            v.result_code = e.args[0]
            v.save()
        finally:
            order.save()
        return order
