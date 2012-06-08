from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from . import models
from ....payment import PaymentFailure

class TargetpayIdealPaymentForm(forms.ModelForm):

    class Meta:
        model = models.TargetpayIdealPayment
        fields = ['issuer']

class TargetpayIdealRedirectForm(forms.Form):
    def __init__(self, params, *args, **kwargs):
        super(TargetpayIdealRedirectForm, self).__init__(*args, **kwargs)
        for param in params:
            self.base_fields[param[0]] = forms.CharField(initial=param[1],
                widget=forms.HiddenInput)
