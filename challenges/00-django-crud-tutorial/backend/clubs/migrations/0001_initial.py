from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Club",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("campus", models.CharField(max_length=80)),
                ("category", models.CharField(max_length=80)),
                ("member_count", models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
