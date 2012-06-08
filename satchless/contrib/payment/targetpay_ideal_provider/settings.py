from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    import targetpay.ideal
except ImportError:
    raise ImproperlyConfigured('Please install the targetpay Python module, version 0.2 or newer.')

def _get_setting(attr, error=None):
    if not error:
        error = 'Please ad %s to your settings.' % attr
    try:
        return getattr(settings, attr)
    except AttributeError:
        raise ImproperlyConfigured(error)

rtlo = _get_setting('TARGETPAY_RTLO')
test = _get_setting('TARGETPAY_TEST')

ideal = targetpay.ideal.Ideal(rtlo=rtlo, test=test)
