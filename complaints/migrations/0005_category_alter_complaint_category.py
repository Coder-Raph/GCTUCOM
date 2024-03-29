# Generated by Django 5.0.1 on 2024-02-07 18:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0004_alter_complaint_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='complaint',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='complaints.category'),
        ),
    ]
