# Generated by Django 2.2.2 on 2019-06-26 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_auto_20190610_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foo',
            name='bar',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='foos', to='test_app.Bar'),
        ),
        migrations.CreateModel(
            name='Baz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('foos', models.ManyToManyField(blank=True, related_name='bazes', to='test_app.Foo')),
            ],
        ),
    ]
