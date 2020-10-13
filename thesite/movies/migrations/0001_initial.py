# Generated by Django 3.1.2 on 2020-10-13 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('year', models.CharField(max_length=100, verbose_name='Year')),
                ('rated', models.CharField(max_length=100, verbose_name='Rated')),
                ('released', models.CharField(max_length=100, verbose_name='Released')),
                ('runtime', models.CharField(max_length=100, verbose_name='Runtime')),
                ('genre', models.CharField(max_length=1000, verbose_name='Genre')),
                ('director', models.CharField(max_length=100, verbose_name='Director')),
                ('plot', models.CharField(max_length=10000, verbose_name='Plot')),
                ('language', models.CharField(max_length=100, verbose_name='Language')),
                ('country', models.CharField(max_length=100, verbose_name='Country')),
                ('awards', models.CharField(max_length=100, verbose_name='Awards')),
                ('poster', models.CharField(max_length=1000, verbose_name='Poster URL')),
                ('metascore', models.CharField(max_length=100, verbose_name='Metascore')),
                ('imdb_rating', models.CharField(max_length=100, verbose_name='IMDB rating')),
                ('imdb_votes', models.CharField(max_length=100, verbose_name='IMDB votes')),
                ('imdb_id', models.CharField(max_length=100, verbose_name='IMDB ID')),
                ('movie_type', models.CharField(max_length=100, verbose_name='Type')),
                ('dvd', models.CharField(max_length=100, verbose_name='DVD')),
                ('box_office', models.CharField(max_length=100, verbose_name='Box office')),
                ('production', models.CharField(max_length=100, verbose_name='Production')),
                ('website', models.CharField(max_length=100, verbose_name='Website')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
        ),
    ]
