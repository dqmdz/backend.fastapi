from tortoise import fields, models

class Product(models.Model):
    id = fields.IntField(pk=True, generated=True)
    name = fields.CharField(max_length=255)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    description = fields.TextField()

    class Meta:
        table = "products"

class Sale(models.Model):
    id = fields.IntField(pk=True, generated=True)
    sale_date = fields.DatetimeField(auto_now_add=True)
    quantity = fields.IntField()
    product = fields.ForeignKeyField('models.Product', related_name='sales')

    class Meta:
        table = "sales"