# Generated by Django 2.0.13 on 2020-05-13 15:04

import core.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('genre_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=140)),
                ('plot', models.TextField()),
                ('release_date', models.DateField()),
                ('budget', models.PositiveIntegerField()),
                ('rating', models.IntegerField(choices=[(0, 'NR - Not Rated'), (1, 'U - Unrestricted public exhibition'), (2, 'U/A - Parental Guidance Suggested'), (3, 'A - Restricted')], default=0)),
                ('website', models.URLField(blank=True)),
                ('movie_poster', models.ImageField(blank=True, max_length=255, null=True, upload_to=core.models.get_user_profile_img_upload_path, verbose_name='Photo')),
            ],
            options={
                'ordering': ('-release_date', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('rating_value', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('review', models.CharField(max_length=1024)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=140)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Movie')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Person')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(blank=True, related_name='acting_credits', to='core.Person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='directed', to='core.Person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(related_name='genre', to='core.Genre'),
        ),
        migrations.AddField(
            model_name='movie',
            name='writers',
            field=models.ManyToManyField(blank=True, related_name='writing_credits', to='core.Person'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('user', 'movie')},
        ),
    ]