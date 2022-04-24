# Generated by Django 4.0.4 on 2022-04-21 09:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9_]+$', message='Invalid name for tag')])),
            ],
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='posts.tag'),
        ),
    ]