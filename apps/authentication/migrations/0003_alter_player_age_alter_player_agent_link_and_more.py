# Generated by Django 4.1.5 on 2023-01-11 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_player_alter_team_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='agent_link',
            field=models.URLField(max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='citizenship',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='contract_expires',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='current_club',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='current_value',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='date_of_birth',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='foot',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='height',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='joined',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='last_contract_extension',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='league_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='max_value',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='max_value_date',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='on_loan',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='outfitter',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='place_of_birth',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='player_agent',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='url',
            field=models.URLField(max_length=500, null=True),
        ),
    ]
