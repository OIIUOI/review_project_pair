# Generated by Django 3.2.13 on 2022-10-28 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_alter_review_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='image',
            field=models.ImageField(blank=True, default=1, upload_to='image/'),
            preserve_default=False,
        ),
    ]
