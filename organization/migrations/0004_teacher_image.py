# Generated by Django 2.0.5 on 2018-05-21 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20180520_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name='头像'),
        ),
    ]
