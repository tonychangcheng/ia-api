from django.core.management.base import BaseCommand
from room.models import Room, User, Message
from django.utils import timezone
from datetime import datetime, timezone as dt_timezone


class Command(BaseCommand):
    help = "Delete rooms and their associated users and messages before a specified date"

    def add_arguments(self, parser):
        parser.add_argument("date", type=str, help="Date in the format YYYY-MM-DD")

    def handle(self, *args, **kwargs):
        date_str = kwargs["date"]
        try:
            # Parse the date and make it timezone-aware with UTC
            date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=dt_timezone.utc)
        except ValueError:
            self.stdout.write(self.style.ERROR("Invalid date format. Use YYYY-MM-DD."))
            return

        # Fetch all rooms created before the given date
        rooms_to_delete = Room.objects.filter(createdate__lt=date)

        if not rooms_to_delete.exists():
            self.stdout.write(self.style.WARNING("No rooms found before the given date."))
            return

        # Delete associated users and messages for each room
        room_ids = rooms_to_delete.values_list("roomid", flat=True)
        User.objects.filter(roomid__in=room_ids).delete()
        Message.objects.filter(roomid__in=room_ids).delete()
        rooms_to_delete.delete()

        self.stdout.write(
            self.style.SUCCESS(f"Successfully deleted rooms, users, and messages created before {date_str}.")
        )
