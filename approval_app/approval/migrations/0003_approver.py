# Generated by Django 5.1.3 on 2024-11-08 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0002_approvallevel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Approver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
