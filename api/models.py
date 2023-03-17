from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


class Products(models.Model):
    name=models.CharField(max_length=150)
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=150)
    category=models.CharField(max_length=150)
    image=models.ImageField(null=True,upload_to="images")


    @property
    def avg_rating(self):
        ratings=self.reviews_set.all().values_list("rating",flat=True)
        if ratings:
         return sum(ratings)/len(ratings)
        else:
            return 0

    @property
    def number_rating(self):
        num=self.reviews_set.all().values_list("rating",flat=True)
        if num:
            return len(num)
        else:
            return  0


    def __str__(self):
        return self.name

#orm-orm for creating a resource
#modelname.objects.create(field1=val 1,field2=val2)

class Carts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now=True)
    options=(
        ("order-placed","order-placed"),
        ("in-cart","in-cart"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=options,default="in-cart")


class Reviews(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=200)

    def __str__(self):
        return self.comment


class Orders(models.Model):
    Product=models.ForeignKey(Products,on_delete=models.CASCADE)
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
        ("order-placed","order-placed"),
        ("despatched","despatched"),
        ("in-transit","in-transit"),
        ("cancelled","cancelled")

    )
    status=models.CharField(max_length=200,choices=options,default="in-cart")
    date=models.DateField(auto_now=True)
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=20)