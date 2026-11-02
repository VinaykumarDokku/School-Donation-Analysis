"""Analyze school donations from a CSV file."""

import argparse
import csv
from collections import defaultdict
from decimal import Decimal, InvalidOperation


def analyze_donations(csv_file):
    school_totals = defaultdict(lambda: Decimal("0"))
    donors = set()
    donation_count = 0
    total = Decimal("0")

    with open(csv_file, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required = {"school", "donor_id", "amount"}

        if not reader.fieldnames or not required.issubset(
            set(reader.fieldnames)
        ):
            raise ValueError(
                "CSV must contain school, donor_id, and amount columns"
            )

        for row in reader:
            school = row["school"].strip()
            donor = row["donor_id"].strip()

            try:
                amount = Decimal(row["amount"].strip())
            except (InvalidOperation, AttributeError):
                raise ValueError("Invalid donation amount")

            if not amount.is_finite() or amount < 0:
                raise ValueError("Donation must be a nonnegative number")

            if not school or not donor:
                raise ValueError("School and donor ID are required")

            school_totals[school] += amount
            donors.add(donor)
            total += amount
            donation_count += 1

    average = (
        total / donation_count
        if donation_count
        else Decimal("0")
    )

    return {
        "total": total,
        "average": average,
        "donations": donation_count,
        "unique_donors": len(donors),
        "school_totals": dict(school_totals),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze school donation data"
    )
    parser.add_argument("csv_file")
    args = parser.parse_args()

    results = analyze_donations(args.csv_file)

    print(f"Total donations: ${results['total']:.2f}")
    print(f"Average donation: ${results['average']:.2f}")
    print(f"Donation records: {results['donations']}")
    print(f"Unique donors: {results['unique_donors']}")

    print("\nDonations by school:")
    for school, amount in sorted(
        results["school_totals"].items()
    ):
        print(f"{school}: ${amount:.2f}")


if __name__ == "__main__":
    main()
