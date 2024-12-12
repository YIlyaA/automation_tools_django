# Generated by Django 5.1.4 on 2024-12-11 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("roll_no", models.CharField(max_length=10)),
                ("name", models.CharField(max_length=20)),
                ("age", models.IntegerField()),
            ],
        ),
    ]