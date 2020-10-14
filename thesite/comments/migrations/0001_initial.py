# Generated by Django 3.1.2 on 2020-10-14 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=10000)),
                ('date', models.DateField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['movie'], name='comments_co_movie_i_5bd45e_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['date'], name='comments_co_date_19d22f_idx'),
        ),
    ]
