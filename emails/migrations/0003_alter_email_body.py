# Generated by Django 5.1.4 on 2024-12-15 15:42

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("emails", "0002_alter_email_attachment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="email",
            name="body",
            field=ckeditor.fields.RichTextField(),
        ),
    ]
