# Generated by Django 5.1.3 on 2025-05-20 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('icon', models.CharField(default='⚔️', max_length=50)),
                ('color', models.CharField(default='#6633ff', max_length=7)),
            ],
            options={
                'verbose_name_plural': 'Character Classes',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='character_classes',
            field=models.ManyToManyField(blank=True, related_name='profiles', to='users.characterclass'),
        ),
    ]
