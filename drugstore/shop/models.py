from django.db import models
from django.db.models import DecimalField
from django.db.models import F
from django.db.models import Sum
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class ProductGroup(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


class Product(models.Model):
    group = models.ForeignKey('ProductGroup', on_delete=models.PROTECT, default='')
    name = models.CharField(max_length=120, unique=True)
    image = models.FileField(upload_to='images', blank=True, default='')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    # If sale price is not given use copy price to sale price.
    def save(self, *args, **kwargs):
        if self.sale_price == 0:
            self.sale_price = self.price
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.group.name}: {self.name} - ${self.price}'


class Country(models.Model):
    name = models.CharField(max_length=16, blank=False, unique=True)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class Order(models.Model):
    order_created = models.DateTimeField(auto_now_add=True)
    order_updated = models.DateTimeField(auto_now=True)

    class OrderStatus(models.TextChoices):
        NOT_CONFIRMED = 'NC', _('Not confirmed')
        CONFIRMED = 'CF', _('Confirmed')
        PAID = 'PD', _('Paid')
        SENT = 'SN', _('Sent')
        DELIVERED = 'DL', _('Delivered')

    order_status = models.CharField(max_length=2, choices=OrderStatus.choices, default=OrderStatus.NOT_CONFIRMED)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)


    @property
    def get_subtotal(self):
        val = (OrderItem.objects
               .filter(order__exact=self.pk)
               .aggregate(subtotal=Sum(F('price') * F('quantity'), output_field=DecimalField()))['subtotal'])
        return val

    @property
    def get_total(self):
        val = (OrderItem.objects
               .filter(order__exact=self.pk)
               .aggregate(total=Sum(F('sale_price') * F('quantity'), output_field=DecimalField()))['total'])
        return val

    def __str__(self):
        return f'#{self.id} ({self.order_created.strftime("%d.%m.%Y %H:%M")}); ' \
               f'Status: {self.OrderStatus(self.order_status).label}'


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_address')
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    country = models.ForeignKey('Country', on_delete=models.PROTECT)
    address = models.CharField(max_length=256)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. "
                                         "Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    owner = models.ForeignKey('auth.User', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.country}, {self.address}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    # Field price and sale_price created programmatically from correspond product.
    # The data is needed because the price of the product may change in the future, which
    # should not affect the price of the order.
    price = models.DecimalField(max_digits=7, decimal_places=2, editable=False)
    sale_price = models.DecimalField(max_digits=7, decimal_places=2, editable=False)

    # The overridden method to copy price and sale price from product to order item.
    def save(self, *args, **kwargs):
        product = Product.objects.get(pk=self.product.id)
        self.price = product.price
        self.sale_price = product.sale_price
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name}: {self.price} - ${self.quantity}'
