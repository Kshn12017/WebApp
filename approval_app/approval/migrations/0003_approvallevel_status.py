# Generated by Django 5.1.3 on 2024-11-09 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0002_alter_approvallevel_approver'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvallevel',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
