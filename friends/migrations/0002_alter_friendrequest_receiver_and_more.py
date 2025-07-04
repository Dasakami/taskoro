# Generated by Django 5.1.3 on 2025-06-05 14:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0001_initial'),
        ('users', '0004_remove_profile_active_effects_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_requests', to='users.profile'),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_requests', to='users.profile'),
        ),
    ]
