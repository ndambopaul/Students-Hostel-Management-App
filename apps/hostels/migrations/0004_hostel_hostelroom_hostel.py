# Generated by Django 5.1.1 on 2024-10-27 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hostels", "0003_hostelroom"),
    ]

    operations = [
        migrations.CreateModel(
            name="Hostel",
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
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("rooms", models.IntegerField(default=1)),
                ("capacity", models.IntegerField(default=1)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="hostelroom",
            name="hostel",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="hostels.hostel",
            ),
        ),
    ]