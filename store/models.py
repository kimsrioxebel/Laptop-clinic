# # from django.db import models

# # # class Laptop(models.Model):
# # #     brand = models.CharField(max_length=100)
# # #     model_name = models.CharField(max_length=100)
# # #     price = models.DecimalField(max_digits=10, decimal_places=2)
# # #     ram = models.CharField(max_length=50)
# # #     storage = models.CharField(max_length=50)
# # #     processor = models.CharField(max_length=100)
# # #     stock = models.PositiveIntegerField()
# # #     created_at = models.DateTimeField(auto_now_add=True)

# # #     def __str__(self):
# # #         return f"{self.brand} {self.model_name}"
# # class Laptop(models.Model):
# #     brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
# #     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

# #     model_name = models.CharField(max_length=100)
# #     price = models.DecimalField(max_digits=10, decimal_places=2)
# #     ram = models.CharField(max_length=50)
# #     storage = models.CharField(max_length=50)
# #     processor = models.CharField(max_length=100)
# #     stock = models.PositiveIntegerField()
# #     created_at = models.DateTimeField(auto_now_add=True)

# #     def __str__(self):
# #         return f"{self.brand} {self.model_name}"
# from django.db import models


# class Brand(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name


# class Category(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name


# class Laptop(models.Model):
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

#     model_name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     ram = models.CharField(max_length=50)
#     storage = models.CharField(max_length=50)
#     processor = models.CharField(max_length=100)
#     stock = models.PositiveIntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.brand} {self.model_name}"
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Laptop(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    model_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ram = models.CharField(max_length=50)
    storage = models.CharField(max_length=50)
    processor = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model_name}"
