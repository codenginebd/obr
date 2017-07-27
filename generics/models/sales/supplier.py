from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u'Name'))
    address_line1 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'Address'))
    address_line2 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'Address'))
    address_line3 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'Address'))
    address_line4 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'Address'))
    phone_number1 = models.ForeignKey(Phone, related_name='supplier_phone1')
    phone_number2 = models.ForeignKey(Phone, related_name='supplier_phone2')
    notes = models.TextField(null=True, blank=True, verbose_name=(u'Notes'))

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Supplier')
        verbose_name_plural = _(u'Suppliers')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('supplier_view', [str(self.id)])
