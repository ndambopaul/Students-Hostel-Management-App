# Generated by Django 5.1.1 on 2024-10-27 13:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hostels", "0004_hostel_hostelroom_hostel"),
        ("students", "0006_student_guardian_name_student_guardian_phone_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="room_assigned",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="hostels.hostelroom",
            ),
        ),
    ]
