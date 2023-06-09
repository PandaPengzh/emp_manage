# Generated by Django 4.0.5 on 2022-06-18 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('password', models.CharField(max_length=10)),
                ('age', models.IntegerField()),
                ('create_time', models.DateField()),
                ('gender', models.SmallIntegerField(choices=[(2, '女'), (1, '男')], verbose_name='性别')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.department')),
            ],
        ),
    ]
