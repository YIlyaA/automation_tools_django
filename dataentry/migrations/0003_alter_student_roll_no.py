# Generated by Django 5.1.4 on 2024-12-11 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataentry", "0002_alter_student_roll_no"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="roll_no",
            field=models.IntegerField(),
        ),
    ]
