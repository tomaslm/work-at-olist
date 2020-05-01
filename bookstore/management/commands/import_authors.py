import csv
import logging
import math

from django.core.management.base import BaseCommand

from bookstore.models import Author


class Command(BaseCommand):
    help = "Imports a csv file with author names"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)
        parser.add_argument(
            "-n",
            "--chunk-size",
            default=1_000,
            type=int,
            help="Chunk size for batch import authors in chunks",
        )

    def handle(self, *args, **options):
        self.stdout.write(
            f"Will import authors from {options['file_path']} file"
            f" in chunks of {options.get('chunk_size')}"
        )

        with open(options["file_path"]) as csvfile:
            import_count = 0

            chunk_size = options.get("chunk_size")
            auhtors_chunk = []
            for row in csv.DictReader(csvfile):
                auhtors_chunk.append(Author(name=row["name"]))

                if len(auhtors_chunk) > chunk_size:
                    Author.objects.bulk_create(auhtors_chunk)
                    import_count += len(auhtors_chunk)
                    auhtors_chunk = []

            if len(auhtors_chunk) > 0:
                Author.objects.bulk_create(auhtors_chunk)
                import_count += len(auhtors_chunk)
                auhtors_chunk = []

        self.stdout.write(
            f"\nDone importing {import_count} authors from "
            f"{options['file_path']} file in "
            f"{math.ceil(import_count/chunk_size)} chunks of"
            f" {options.get('chunk_size')}",
            self.style.SUCCESS,
        )
