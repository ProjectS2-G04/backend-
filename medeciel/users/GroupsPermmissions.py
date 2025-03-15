from django.contrib.auth.models import Group , Permission

doctor_group , created = Group.objects.get_or_create(name="Doctors")

admin_group , created = Group.objects.get_or_create(name="Admin")

patient_group ,created=Group.objects.get_or_create(name="Patient")
