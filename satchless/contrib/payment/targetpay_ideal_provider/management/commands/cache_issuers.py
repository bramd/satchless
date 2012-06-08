from django.core.management.base import BaseCommand, CommandError

from ...settings import ideal

class Command(BaseCommand):
    help = 'Retrieve a list of Ideal issuers and cache tem in the DB'
    
    def handle(self, *args, **options):
        from ...models import TargetpayIdealIssuer as Issuer
        issuers = ideal.getIssuers()
        issuer_ids = []
        for issuer_id, issuer_name in issuers.items():
            issuer_ids.append(issuer_id)
            issuer, created = Issuer.objects.get_or_create(issuer_id=issuer_id, defaults={'name': issuer_name})
            if not created:
                issuer.name = issuer_name
                issuer.save()
        Issuer.objects.exclude(issuer_id__in=issuer_ids).delete()
