from django.db import models
from django.utils import timezone


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    chat_id = models.IntegerField()
    telegram_id = models.IntegerField()
    registration_date = models.DateField(default=timezone.now)


class ItemType(models.Model):
    type_id = models.AutoField(primary_key=True)
    data_type = models.CharField(max_length=50, default="item")
    description = models.CharField(max_length=500)


class ToSeeItem(models.Model):
    record_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message_id = models.IntegerField()
    date_received = models.DateField()
    data_type = models.ForeignKey(
        ItemType, on_delete=models.SET_DEFAULT, default="item"
    )
    raw_data = models.CharField(max_length=1000)
