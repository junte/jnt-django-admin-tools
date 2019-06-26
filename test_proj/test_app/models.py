from django.db import models


class Bar(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Foo(models.Model):
    name = models.CharField(max_length=100, null=True)
    bar = models.ForeignKey(Bar, models.SET_NULL, null=True, related_name='foos')

    def __str__(self):
        return self.name


class Baz(models.Model):
    name = models.CharField(max_length=100, null=True)
    foos = models.ManyToManyField(Foo, related_name='bazes', blank=True)

    def __str__(self):
        return self.name
