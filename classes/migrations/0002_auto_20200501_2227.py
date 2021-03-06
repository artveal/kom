# Generated by Django 3.0.5 on 2020-05-01 20:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'Cities'},
        ),
        migrations.RenameField(
            model_name='competitionround',
            old_name='competition_format',
            new_name='round_format',
        ),
        migrations.RenameField(
            model_name='competitionseasonround',
            old_name='competition_season',
            new_name='competition',
        ),
        migrations.RenameField(
            model_name='competitionseasonround',
            old_name='competition_format',
            new_name='round_format',
        ),
        migrations.RemoveField(
            model_name='competitionround',
            name='untie_rule',
        ),
        migrations.RemoveField(
            model_name='competitionseasonround',
            name='untie_rule',
        ),
        migrations.AddField(
            model_name='competitionround',
            name='table_tiebreak',
            field=models.CharField(choices=[('global', 'Goal difference > Scored goals (global table)'), ('local', 'Results between tied teams will be used to tiebreak. If still tied, use global tiebreak')], default='local', help_text='Only for leagues', max_length=15),
        ),
        migrations.AddField(
            model_name='competitionround',
            name='tiebreak_rule',
            field=models.CharField(choices=[('et_away_goals', 'Use away goals rule (if # of rounds > 1). If tied, play extra time and penalty shootout'), ('et', 'Play extra time and penalty shootout directly'), ('penalties', 'Play penalty shootout directly')], default='et_away_goals', help_text='Only for cup rounds', max_length=15),
        ),
        migrations.AddField(
            model_name='competitionseasonround',
            name='table_tiebreak',
            field=models.CharField(choices=[('global', 'Goal difference > Scored goals (global table)'), ('local', 'Results between tied teams will be used to tiebreak. If still tied, use global tiebreak')], default='local', help_text='Only for leagues', max_length=15),
        ),
        migrations.AddField(
            model_name='competitionseasonround',
            name='tiebreak_rule',
            field=models.CharField(choices=[('et_away_goals', 'Use away goals rule (if # of rounds > 1). If tied, play extra time and penalty shootout'), ('et', 'Play extra time and penalty shootout directly'), ('penalties', 'Play penalty shootout directly')], default='et_away_goals', help_text='Only for cup rounds', max_length=15),
        ),
        migrations.AddField(
            model_name='player',
            name='yellow_cards_d',
            field=models.PositiveIntegerField(default=0, verbose_name='Domestic competitions yellow cards'),
        ),
        migrations.AddField(
            model_name='player',
            name='yellow_cards_i',
            field=models.PositiveIntegerField(default=0, verbose_name='Int. club competitions yellow cards'),
        ),
        migrations.AddField(
            model_name='player',
            name='yellow_cards_n',
            field=models.PositiveIntegerField(default=0, verbose_name='National team yellow cards'),
        ),
        migrations.AlterField(
            model_name='player',
            name='domestic_susp',
            field=models.PositiveIntegerField(default=0, verbose_name='Domestic competitions suspension'),
        ),
        migrations.AlterField(
            model_name='player',
            name='fitness',
            field=models.PositiveIntegerField(default=100, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='player',
            name='injury_time',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='int_susp',
            field=models.PositiveIntegerField(default=0, verbose_name='Int. club competitions suspension'),
        ),
        migrations.AlterField(
            model_name='player',
            name='loan_by_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='loan_team', to='classes.Team', verbose_name='Loaned by'),
        ),
        migrations.AlterField(
            model_name='player',
            name='loan_contrib',
            field=models.IntegerField(default=0, help_text='Paid by current team to loan team', verbose_name='Loan contribution'),
        ),
        migrations.AlterField(
            model_name='player',
            name='n_shirt_number',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(1)], verbose_name='National team shirt number'),
        ),
        migrations.AlterField(
            model_name='player',
            name='nt_susp',
            field=models.PositiveIntegerField(default=0, verbose_name='National team suspension'),
        ),
        migrations.AlterField(
            model_name='player',
            name='salary',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='player',
            name='t_shirt_number',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(1)], verbose_name='Team shirt number'),
        ),
        migrations.AlterField(
            model_name='player',
            name='transfer_status',
            field=models.CharField(choices=[('Trn', 'Transferable'), ('NTrn', 'Non transferable'), ('unset', 'Non set')], default='unset', max_length=5),
        ),
        migrations.AlterField(
            model_name='team',
            name='shirt1_color1',
            field=models.CharField(default='#ffffff', max_length=20, verbose_name='Home shirt main color'),
        ),
        migrations.AlterField(
            model_name='team',
            name='shirt1_color2',
            field=models.CharField(default='#000000', max_length=20, verbose_name='Home shirt details color'),
        ),
        migrations.AlterField(
            model_name='team',
            name='shirt1_style',
            field=models.CharField(default='style1', max_length=20, verbose_name='Home shirt style'),
        ),
        migrations.AlterField(
            model_name='team',
            name='shirt2_color1',
            field=models.CharField(default='#000000', max_length=20, verbose_name='Away shirt main color'),
        ),
        migrations.AlterField(
            model_name='team',
            name='shirt2_color2',
            field=models.CharField(default='#ffffff', max_length=20, verbose_name='Away shirt details color'),
        ),
        migrations.AlterField(
            model_name='team',
            name='shirt2_style',
            field=models.CharField(default='style1', max_length=20, verbose_name='Away shirt style'),
        ),
    ]
