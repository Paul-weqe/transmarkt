# Generated by Django 4.1.5 on 2023-01-12 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_player_age_alter_player_agent_link_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, null=True)),
                ('link', models.URLField(max_length=500, null=True)),
                ('position', models.CharField(max_length=25, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='player',
            name='url',
            field=models.URLField(max_length=500, null=True, unique=True),
        ),
    ]