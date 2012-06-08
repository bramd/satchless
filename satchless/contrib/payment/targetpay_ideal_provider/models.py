from django.db import models
from django.utils.translation import ugettext_lazy as _

class TargetpayIdealPayment(models.Model):
    amount = models.PositiveIntegerField(null=True) # in cents
    result_code= models.CharField(max_length=100, blank=True, null=True)
    issuer = models.ForeignKey('TargetpayIdealIssuer', verbose_name=_('Bank'))
    transaction_id = models.CharField(max_length=16, blank=True, null=True)
    redirect_url = models.URLField(blank=True, null=True)

    class Meta:
        abstract = True

class TargetpayIdealIssuer(models.Model):
    """Issuer (aka bank)
    
    This model is used to cache the issuers list as returned by TargetPay.
    """
    issuer_id = models.PositiveIntegerField(max_length=6)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('Issuer')
        verbose_name_plural = _('Issuers')
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name
