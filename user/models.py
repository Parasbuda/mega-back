from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from core.models import Branch
from django.core.mail import EmailMultiAlternatives
from django_rest_resetpassword.signals import reset_password_token_created
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

# from rest_framework_simplejwt.tokens import RefreshToken
from util.get_bs_date import bs_date


# Create your models here.
@receiver(reset_password_token_created)
def reset_password_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        "current_user": reset_password_token.user,
        "user_name": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        # 'domain': "iims-backend.staging.merakitechs.com",
        "domain": "http://localhost:3000",
        # 'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
        "reset_password_url": "{}{}".format(
            "/reset-password/confirm/", reset_password_token.key
        ),
    }

    # render email text
    email_html_message = render_to_string("email.html", context)
    # email_plaintext_message = render_to_string('email/user_reset_password.txt', context)
    email_plaintext_message = "{}?token={}".format(
        reverse("password_reset:reset-password-request"), reset_password_token.key
    )
    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


class UserManager(BaseUserManager):
    def create_superuser(self, username, password=None, **other_fields):
        if not username:
            raise ValueError("Username is required")
        # if not email:
        #     raise ValueError("Email is required")
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        return self.create_user(username, password, **other_fields)

    def create_user(self, username, password=None, **other_fields):
        if not username:
            raise ValueError("Username is required")
        # if not email:
        #     raise ValueError("Email is required")

        # email = self.normalize_email(email)
        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    gender_choices = ((1, "MALE"), (2, "FEMALE"), (3, "OTHERS"))
    group_choices = ((1, "ADMIN"), (2, "STAFF"), (3, "MAINTAINER"))
    first_name = models.CharField(max_length=40, blank=True)
    middle_name = models.CharField(max_length=40, blank=True)
    name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=40, blank=True)

    gender = models.PositiveSmallIntegerField(
        choices=gender_choices,
        blank=True,
        null=True,
        help_text="where 1=MALE 2=FEMALE 3=OTHERS",
    )
    group = models.CharField(max_length=1, choices=group_choices, default=1)
    user_branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="branch",
    )
    employee_id = models.CharField(max_length=30, blank=True, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True
    )
    created_date_ad = models.DateTimeField()
    created_date_bs = models.CharField(max_length=15)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date_ad = timezone.now()
            date_bs = bs_date(self.created_date_ad)
            self.created_date_bs = date_bs
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True
