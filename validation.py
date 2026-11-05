
import json
from pathlib import Path
from decimal import Decimal, InvalidOperation


# Folders
actual_folder = Path("json_output")
expected_folder = Path("expected_json")


# Fields to compare
fields = [
    "supplier_name",
    "customer_name",
    "invoice_number",
    "invoice_date",
    "due_date",
    "subtotal",
    "tax",
    "total",
    "currency"
]

# Invoices to include in validation
invoice_files = [
    "invoice_01_simple.json",
    "invoice_02_multipage.json",
    "invoice_03_irrelevant_content.json",
    "invoice_05_complex_calculations.json",
    "invoice_06_missing_information.json",
    "invoice_07_ambiguous.json",
    "invoice_08_scanned.json",
    "invoice_10_unusual_layout.json"
]


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def values_match(field, actual, expected):

    # Compare missing values
    if actual is None or expected is None:
        return actual is None and expected is None

    # Compare monetary amounts accurately
    if field in ["subtotal", "tax", "total"]:
        try:
            return Decimal(str(actual)) == Decimal(str(expected))
        except InvalidOperation:
            return False

    # Compare names and currency without case differences
    if field in ["supplier_name", "customer_name", "currency"]:
        return str(actual).strip().casefold() == str(expected).strip().casefold()

    # Compare other fields exactly
    return str(actual).strip() == str(expected).strip()


def main():

    total_correct = 0
    total_fields = 0
    exact_invoice_count = 0

    field_correct = {field: 0 for field in fields}
    field_total = {field: 0 for field in fields}

    print("\n========== INVOICE VALIDATION ==========\n")

    for filename in invoice_files:

        actual_path = actual_folder / filename
        expected_path = expected_folder / filename

        print(f"\nInvoice: {filename}")
        print("-" * 50)

        if not expected_path.exists():
            print("Expected JSON missing. Skipping this invoice.")
            continue

        expected_data = load_json(expected_path)

        if not actual_path.exists():
            print("Actual JSON missing. All fields counted as incorrect.")
            actual_data = {}
        else:
            actual_data = load_json(actual_path)

        invoice_correct = 0

        for field in fields:

            expected_value = expected_data.get(field)
            actual_value = actual_data.get(field)

            is_correct = values_match(
                field,
                actual_value,
                expected_value
            )

            field_total[field] += 1
            total_fields += 1

            if is_correct:
                field_correct[field] += 1
                total_correct += 1
                invoice_correct += 1
                print(f"PASS  {field}")
            else:
                print(f"FAIL  {field}")
                print(f"      Expected: {expected_value}")
                print(f"      Actual:   {actual_value}")

        if invoice_correct == len(fields):
            exact_invoice_count += 1

        print(f"\nInvoice accuracy: {invoice_correct}/{len(fields)}")


    # Overall accuracy
    overall_accuracy = (
        total_correct / total_fields * 100
        if total_fields else 0
    )

    print("\n========== FIELD ACCURACY ==========\n")

    for field in fields:

        correct = field_correct[field]
        total = field_total[field]

        accuracy = correct / total * 100 if total else 0

        print(
            f"{field}: {correct}/{total} "
            f"({accuracy:.2f}%)"
        )

    print("\n========== FINAL RESULTS ==========")

    print(f"Correct fields: {total_correct}/{total_fields}")
    print(f"Overall field accuracy: {overall_accuracy:.2f}%")
    print(
        f"Completely correct invoices: "
        f"{exact_invoice_count}/{len(invoice_files)}"
    )


if __name__ == "__main__":
    main()
