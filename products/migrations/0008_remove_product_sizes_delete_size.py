# Generated by Django 4.2.3 on 2023-08-02 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_rating_product_alter_rating_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sizes',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]