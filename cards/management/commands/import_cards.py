import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from cards.models import Card, Deck

REQUIRED_COLUMNS = {"level", "kind", "front", "reading", "meaning", "example"}


class Command(BaseCommand):
    help = "Import cards from a CSV (columns: level, kind, front, reading, meaning, example)."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=Path)

    @transaction.atomic
    def handle(self, *args, **options):
        path = options["csv_path"]
        if not path.exists():
            raise CommandError(f"File not found: {path}")

        created = updated = 0
        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            if missing:
                raise CommandError(f"Missing columns: {', '.join(sorted(missing))}")

            for line_no, row in enumerate(reader, start=2):
                level, kind = row["level"].strip(), row["kind"].strip()
                if level not in Deck.Level.values:
                    raise CommandError(f"Line {line_no}: invalid level '{level}'")
                if kind not in Card.Kind.values:
                    raise CommandError(f"Line {line_no}: invalid kind '{kind}'")

                deck, _ = Deck.objects.get_or_create(
                    name=f"JLPT {level} {kind.capitalize()}", level=level
                )
                _, was_created = Card.objects.update_or_create(
                    deck=deck,
                    kind=kind,
                    front=row["front"].strip(),
                    defaults={
                        "reading": row["reading"].strip(),
                        "meaning": row["meaning"].strip(),
                        "example": row["example"].strip(),
                    },
                )
                created += was_created
                updated += not was_created

        self.stdout.write(self.style.SUCCESS(f"Done: {created} created, {updated} updated."))