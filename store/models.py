#Imports relevant Django Modules.
from django.db import models
from django.contrib.auth.models import User

#Creates customer database model with user, name and email of customer being recorded
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)

    #Defines function that retrieves a customer's orders, and lists by order date. 
    def get_orders(self):
        return Order.objects.filter(customer=self).order_by('-order_date')

    #Defines function that converts the name attribute of customer object to a string
    def __str__(self):
        return self.name

#Creates product database model with product name, description, price and the image
class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=300, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)

    #Defines function that converts the product name into a string.
    def __str__(self):
        return self.name
    
    #Defines function that retrieves image url for each product
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url

#Defines the Order model
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)
    products = models.ManyToManyField(Product, through="OrderItem") #Many to many relationship with OrderItem. This ensures each order can have a variety of products.
    
    
    #Returns ID of the order as a string
    def __str__(self):
        return str(self.id)
    #Defines function that calculates an order total
    def get_order_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total
    
    #Returns a queryset of all items within an order.
    @property
    def get_order_items(self):
        return self.orderitem_set.all()
    
    #Defines function that returns the value of items within the user's cart
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    #Defines function that returns the quantity of items within a cart.
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    
#Defines the OrderItem model within the database, which represents items within an order
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    #Returns a string containing quantity, product name and the order ID
    @property
    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order: {self.order.id})"

    #Defines function that calculates and returns the total cost of the order item by multiplying the product's price by the quantity
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total 

#Creates ShippingAddress table within DB
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True) #Foreign Key associates each shipping address with a customer
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True) #Foreign Key associates each shipping address with an order.
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    county = models.CharField(max_length=50, null=True)
    postcode = models.CharField(max_length=8, null=True)
    
    #Defines function that converts the address object as a string.
    def __str__(self):
        return self.address
