from distutils.command.upload import upload
from statistics import mode
from tabnanny import verbose
from django.conf import settings
from django.db import models
from django.utils import timezone

from requests import session
from util.get_bs_date import bs_date

# Create your models here.


class Branch(models.Model):
    class Meta:
        verbose_name_plural = "Branches "

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5, unique=True)
    is_active = models.BooleanField(default=True)
    created_date_ad = models.DateTimeField()
    created_date_bs = models.CharField(max_length=15)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date_ad = timezone.now()
            date_bs = bs_date(self.created_date_ad)
            self.created_date_bs = date_bs
        super().save(*args, **kwargs)


class District(models.Model):
    name = models.CharField(max_length=25)
    name_nepali = models.CharField(max_length=25)
    is_active = models.BooleanField(default=True)
    created_date_ad = models.DateTimeField()
    created_date_bs = models.CharField(max_length=15)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date_ad = timezone.now()
            date_bs = bs_date(self.created_date_ad)
            self.created_date_bs = date_bs
        super().save(*args, **kwargs)


class Print(models.Model):
    CARD_CHOICES = (
        ("1", "DEBIT"),
        ("2", "CREDIT"),
    )
    first_name = models.CharField(max_length=50)
    first_name_nepali = models.CharField(max_length=50)
    card_type = models.CharField(max_length=1, choices=CARD_CHOICES)
    middle_name = models.CharField(max_length=50, blank=True)
    middle_name_nepali = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    last_name_nepali = models.CharField(max_length=50)
    name = models.CharField(max_length=150, blank=True)
    card_no = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    address_nepali = models.CharField(max_length=50)
    citizenship_no = models.CharField(max_length=20)
    citizenship_no_nepali = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=10)
    mobile_no_nepali = models.CharField(max_length=10)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True)
    created_date_ad = models.DateTimeField()
    qr = models.ImageField(upload_to="print/")
    owner_photo = models.ImageField(upload_to="print/")
    created_date_bs = models.CharField(max_length=15)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date_ad = timezone.now()
            date_bs = bs_date(self.created_date_ad)
            self.created_date_bs = date_bs
        super().save(*args, **kwargs)


class FiscalSessionAD(models.Model):
    session_full_name = models.CharField(max_length=10, unique=True, blank=True)
    session_short_name = models.CharField(max_length=5, unique=True, blank=True)
    created_date_ad = models.DateTimeField()
    created_date_bs = models.CharField(max_length=15)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True
    )

    def __str__(self):
        return self.session_short_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date_ad = timezone.now()
            date_bs = bs_date(self.created_date_ad)
            self.created_date_bs = date_bs
        super().save(*args, **kwargs)


class FiscalSessionBS(models.Model):
    session_full_name = models.CharField(max_length=10, unique=True, blank=True)
    session_short_name = models.CharField(max_length=5, unique=True, blank=True)
    created_date_ad = models.DateTimeField()
    created_date_bs = models.CharField(max_length=15)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True
    )

    def __str__(self):
        return self.session_short_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date_ad = timezone.now()
            date_bs = bs_date(self.created_date_ad)
            self.created_date_bs = date_bs
        super().save(*args, **kwargs)
