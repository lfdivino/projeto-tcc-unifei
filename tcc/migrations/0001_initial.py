# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Perguntas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pergunta', models.TextField()),
                ('ativa', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='PerguntasRespondidasUsuarios',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('id_pergunta', models.ForeignKey(to='tcc.Perguntas')),
            ],
        ),
        migrations.CreateModel(
            name='Respostas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('resposta', models.IntegerField()),
                ('data_resposta', models.DateField()),
                ('id_pergunta', models.ForeignKey(to='tcc.Perguntas')),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome_completo', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('aniversario', models.DateField()),
                ('formado', models.BooleanField()),
                ('matricula', models.IntegerField(blank=True, null=True)),
                ('formatura', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='perguntasrespondidasusuarios',
            name='id_usuario',
            field=models.ForeignKey(to='tcc.Usuarios'),
        ),
        migrations.AlterUniqueTogether(
            name='perguntasrespondidasusuarios',
            unique_together=set([('id_usuario', 'id_pergunta')]),
        ),
    ]
