# Generated by Django 3.0.7 on 2020-07-26 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('code', models.CharField(max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TranslatedHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.TextField()),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='translations.Language')),
                ('translations', models.ManyToManyField(related_name='_translatedheader_translations_+', to='translations.TranslatedHeader')),
            ],
        ),
    ]