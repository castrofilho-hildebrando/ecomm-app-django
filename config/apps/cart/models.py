import uuid

from django.db import models


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "carts"

    def __str__(self):
        return f"Cart for user {self.user_id}"


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product_id = models.UUIDField()
    quantity = models.IntegerField()

    class Meta:
        db_table = "cart_items"
        unique_together = ["cart", "product_id"]

    def __str__(self):
        return f"CartItem {self.product_id} x {self.quantity}"
