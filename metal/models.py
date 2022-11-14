from django.db import models


# Create your models here.
class MetalPrice(models.Model):
    """
    貴金属の情報

    1gあたりの価格を示す
    """

    class Meta:
        db_table = "metal"

    metal_type = models.CharField(verbose_name="金属名", max_length=100)
    buy = models.PositiveIntegerField(verbose_name="買値", null=True, blank=True)
    sell = models.PositiveIntegerField(verbose_name='売値', null=True, blank=True)

    def __str__(self):
        return self.metal_type


class MetalPurchase(models.Model):
    """
    貴金属の買取履歴
    """

    class Meta:
        db_table = "purchase"

    metal_type = models.ForeignKey(MetalPrice, verbose_name="金属名", on_delete=models.PROTECT)
    weight = models.PositiveIntegerField(verbose_name="重量", null=True, blank=True)
    email = models.CharField(verbose_name="email", max_length=255)
    name = models.CharField(verbose_name="取引者", max_length=255)
    created = models.DateTimeField(verbose_name="取引日時", auto_now_add=True)

    def __str__(self):
        return f'{str(self.metal_type)}_{str(self.created)}'

