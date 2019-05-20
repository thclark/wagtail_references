# Generated by Django 2.1.4 on 2019-05-17 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_references', '0003_reference_sort_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='slug',
            field=models.SlugField(help_text='A short key to cite the reference by. Determined from the BibTeX entry key. Must be unique.', max_length=255, unique=True, verbose_name='slug'),
        ),
    ]