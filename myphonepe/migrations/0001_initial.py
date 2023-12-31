# Generated by Django 4.1.13 on 2023-12-16 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('transaction_id', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to='payment')),
                ('datetime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentInitiate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('source', models.CharField(max_length=150)),
                ('transaction_id', models.CharField(max_length=150)),
                ('status', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentSecret',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchantid', models.CharField(max_length=200)),
                ('key', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Security',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ACCOUNT_SID', models.CharField(blank=True, max_length=200)),
                ('AUTH_TOKEN', models.CharField(blank=True, max_length=200)),
                ('VARIFY_SID', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]
