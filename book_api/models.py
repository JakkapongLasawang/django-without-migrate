from django.db import models
import pytz
from datetime import datetime


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    number_of_pages = models.IntegerField()
    author = models.CharField(max_length=128)
    quantity = models.IntegerField()
    published = models.DateTimeField(default=datetime.now(pytz.utc))

    class Meta:
        db_table = "book_"
