# Generated by Django 4.1 on 2024-03-27 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobpost', '0006_rename_recuiter_login_recruiter_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='gmail_cv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField()),
                ('mail', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('heading', models.TextField()),
                ('body', models.TextField()),
                ('skill', models.TextField()),
                ('contact_no', models.CharField(max_length=20)),
                ('contact_mail', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('company_name', models.CharField(max_length=30)),
                ('recruiter_name', models.CharField(max_length=30)),
                ('filename', models.CharField(max_length=30)),
                ('uniqueid', models.CharField(max_length=20)),
            ],
        ),
    ]