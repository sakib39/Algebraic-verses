from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    # Additional fields as necessary

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    # Additional fields as necessary

    def __str__(self):
        return self.name

class Problem(models.Model):
    sub_category = models.ForeignKey(SubCategory, related_name='problems', on_delete=models.CASCADE)
    statement = models.TextField()
    solution = models.TextField()
    TRUE_FALSE_CHOICES = (
        (True, 'True'),
        (False, 'False'),
    )

    answer = models.BooleanField(choices=TRUE_FALSE_CHOICES)
    # Additional fields and methods as necessary

    def __str__(self):
        return self.statement
