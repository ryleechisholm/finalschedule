from django.db import models
from django.db.models.deletion import CASCADE

class Employee(models.Model):
    jobs = (
        ('Nurse', 'Nurse'),
        ('Doctor', 'Doctor'),
        ('Manager', 'Manager')
        )
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    job = models.CharField(max_length=200, null=True, choices=jobs)

    def __str__(self):
        return self.name


class Day(models.Model):
    manager = models.CharField(max_length=100, null=True)
    doctor1 = models.CharField(max_length=100, null=True)
    doctor2 = models.CharField(max_length=100, null=True)
    nurse1 = models.CharField(max_length=100, null=True)
    nurse2 = models.CharField(max_length=100, null=True)
    nurse3 = models.CharField(max_length=100, null=True)
    nurse4 = models.CharField(max_length=100, null=True)
    nurse5 = models.CharField(max_length=100, null=True)
    nurse6 = models.CharField(max_length=100, null=True)


class Message(models.Model):
    user = models.CharField(null=True, max_length=100)
    content = models.CharField(max_length=200, null=True)
