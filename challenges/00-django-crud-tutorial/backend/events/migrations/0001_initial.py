from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("clubs", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("event_date", models.DateField()),
                ("location", models.CharField(max_length=120)),
                ("capacity", models.PositiveIntegerField(default=20)),
                ("status", models.CharField(choices=[("scheduled", "Scheduled"), ("cancelled", "Cancelled"), ("completed", "Completed")], default="scheduled", max_length=20)),
                ("club", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="events", to="clubs.club")),
            ],
        ),
    ]
