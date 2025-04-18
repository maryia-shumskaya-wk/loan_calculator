# Generated by Django 4.2.7 on 2023-12-05 18:33

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='MortgageCalculation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mortgage_term_in_months', models.IntegerField()),
                ('monthly_payment', models.DecimalField(decimal_places=2, max_digits=15)),
                ('interest_rate', models.DecimalField(decimal_places=4, max_digits=7)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_over_loan_term', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
