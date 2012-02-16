from django.core.management.base import BaseCommand, CommandError
from newrooms.models import NRoom
from datetime import datetime

class Command(BaseCommand):
    args = '<file>'
    help = ''

    def handle(self, *args, **options):
        for file in args:
            f = open(file, "r")
            for line in f:
                l = line.split()
                room = NRoom()
                room.number            = l[0]
                room.capacity          = int(l[1])
                room.short_unlock_time = datetime.now()
                room.save()

            self.stdout.write('Successfully imported\n')