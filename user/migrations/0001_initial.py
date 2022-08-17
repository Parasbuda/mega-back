# Generated by Django 3.1.9 on 2022-04-09 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("first_name", models.CharField(max_length=40)),
                ("middle_name", models.CharField(blank=True, max_length=40)),
                ("name", models.CharField(blank=True, max_length=120)),
                ("last_name", models.CharField(max_length=40)),
                (
                    "gender",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[(1, "MALE"), (2, "FEMALE"), (3, "OTHERS")],
                        help_text="where 1=MALE 2=FEMALE 3=OTHERS",
                        null=True,
                    ),
                ),
                ("employee_id", models.CharField(blank=True, max_length=30)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("username", models.CharField(max_length=20, unique=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("created_date_ad", models.DateTimeField()),
                ("created_date_bs", models.CharField(max_length=15)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "group",
                    models.CharField(max_length=1, default=2),
                ),
                (
                    "user_branch",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="branch",
                        to="core.branch",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
