# Generated by Django 5.1.5 on 2025-01-22 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fncapp', '0003_alter_pianoformativo_fondo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RappresentanteSindacale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_cognome', models.CharField(max_length=100)),
                ('data_nascita', models.DateField()),
                ('luogo_nascita', models.CharField(max_length=100)),
                ('citta_residenza', models.CharField(max_length=100)),
                ('via_residenza', models.CharField(max_length=200)),
                ('numero_civico', models.CharField(max_length=10)),
                ('codice_fiscale', models.CharField(max_length=16)),
                ('firma', models.TextField()),
            ],
        ),
    ]
