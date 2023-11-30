from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class LeaveBalance(models.Model):
    emp_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    coff = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    el = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    lwp = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    rh = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    sl = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    wfh = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )


class LeaveAvailed(models.Model):
    emp_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    leave_type = models.CharField(max_length=50)
    action = models.CharField(max_length=50)
    date = models.DateField()
    debit = models.PositiveIntegerField()

