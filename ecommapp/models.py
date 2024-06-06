from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CAT=((1,'Mobile'),(2,'shoes'),(3,'Clothes'))
    name=models.CharField(max_length=50 ,verbose_name='Product Name')
    price=models.FloatField()
    cat=models.IntegerField(verbose_name='Category' ,choices=CAT)
    pdetail=models.CharField(max_length=300, verbose_name='Product Detail')
    pimage=models.ImageField(upload_to='image')
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE, db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE, db_column='pid')
    qty=models.IntegerField(default=1)

class Order(models.Model):
    orderid=models.IntegerField()
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE, db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE, db_column='pid')
    qty=models.IntegerField(default=1)
    amount=models.FloatField()

