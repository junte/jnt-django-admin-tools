# Generated by Django 4.0.6 on 2022-07-26 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0010_auto_20201119_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(related_name='+', to='test_app.tag'),
        ),
    ]
