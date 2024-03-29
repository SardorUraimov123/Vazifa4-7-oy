from django.db import models
from django.contrib.auth.models import AbstractUser
from main.funcs import generate_code
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
    

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.code = generate_code()
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    banner_img = models.ImageField(upload_to='banner-img/')
    quantity = models.IntegerField() 
    delivery = models.BooleanField(default=False)


class ProductImg(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='img/')


class ProductVideo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    video = models.FileField(upload_to='video')
    link = models.URLField(null=True, blank=True)


from django.db import models
from django.core.exceptions import ValidationError

class Review(models.Model):
    mark = models.IntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    text = models.TextField()

    def save(self, *args, **kwargs):
        if self.pk:
            super().save(*args, **kwargs)
        else:
            existing_reviews = Review.objects.filter(product=self.product, user=self.user)
            if existing_reviews.exists():
                raise ValidationError("Bu foydalanuvchi allaqachon bu maxsulot uchun izoh qoldirgan!")
            super().save(*args, **kwargs)




class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    count = models.IntegerField()


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if WishList.objects.filter(user=self.user, product=self.product).count():
            raise ValueError('Ma`lumot bor')
        super(WishList, self).save(*args, **kwargs)


@receiver(post_save, sender=Product)
def generate_product_code(sender, instance, created, **kwargs):
    if created:
        instance.code = get_random_string(length=6)
        instance.save()

@receiver(post_save, sender=Cart)
def generate_cart_code(sender, instance, created, **kwargs):
    if created:
        instance.code = get_random_string(length=8)
        instance.save()

"""
USER
register -
login -
logout -
update -
set password -
delete -

CATEGORY
create +
update +
list +
delete +


Product 
create +
update +
list +
detail +
delete +

PRODUCT IMG/VIDEO
create + 
delete +

REVIEW
create - 
list +
update -

"""
