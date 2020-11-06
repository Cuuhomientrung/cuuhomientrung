import sys

from django.core.management import BaseCommand, call_command

from app.tests.factories import (
    CuuHoFactory,
    HoDanFactory,
    TNVFactory,
    NguonLucFactory,
    TinTucFactory
)
from app.models import Tinh

class Command(BaseCommand):
    help = "Populate dummy data"

    def add_arguments(self, parser):
        parser.add_argument(
            "size",
            type=int,
            default=50,
            help="Size of the dummy data to populate",
            nargs="?"
        )

    def handle(self, *args, **options):
        size = options.get("size", 50)

        if not Tinh.objects.exists():
            print("Calling add_du_lieu_location command")
            call_command("add_du_lieu_location")

        print("Generating dummy data")
        for i in range(size):
            CuuHoFactory()
            HoDanFactory()
            TNVFactory()
            NguonLucFactory()
            TinTucFactory()
            print("{:.0%}".format((i+1)/size))
        print("DONE!")