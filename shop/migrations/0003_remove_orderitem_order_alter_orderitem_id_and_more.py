# Generated by Django 4.0.5 on 2022-07-11 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_order_orderitem_remove_cartorderitems_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
