# Generated by Django 5.0.3 on 2024-03-19 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobpost', '0003_alter_company_login_company_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company_login_v2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=20)),
            ],
        ),
    ]