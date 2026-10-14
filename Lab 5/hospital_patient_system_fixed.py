
"""Manage hospital patient admissions, treatment costs, and records."""

import hashlib
import secrets

PATIENT_RECORDS = {
    "P101": {
        "name": "John Doe",
        "ward": "ICU",
        "is_admitted": True,
        "bill": 2400.0,
    },
    "P102": {
        "name": "Jane Smith",
        "ward": "General",
        "is_admitted": False,
        "bill": 450.0,
    },
    "P103": {
        "name": "Robert Brown",
        "ward": "Private",
        "is_admitted": True,
        "bill": 1200.0,
    },
}


def admit_patient(p_id, name, ward, intake_log=None):
    """Admit a new patient and optionally record the admission."""
    if p_id in PATIENT_RECORDS:
        return False

    if intake_log is None:
        intake_log = []

    PATIENT_RECORDS[p_id] = {
        "name": name,
        "ward": ward,
        "is_admitted": True,
        "bill": 0.0,
    }
    intake_log.append(f"Admitted patient {p_id} into ward {ward}")
    return True


def discharge_patient(p_id):
    """Discharge a patient if the patient ID exists."""
    patient = PATIENT_RECORDS.get(p_id)
    if patient is None:
        return False

    patient["is_admitted"] = False
    return True


def verify_admission_status(p_id):
    """Return whether a patient is currently admitted."""
    patient = PATIENT_RECORDS.get(p_id)
    return patient is not None and patient["is_admitted"]


def calculate_treatment_cost(p_id, multiplier=1.12):
    """Calculate treatment cost using a numeric multiplier."""
    patient = PATIENT_RECORDS.get(p_id)
    if patient is None:
        raise ValueError(f"Unknown patient ID: {p_id}")

    if (
        isinstance(multiplier, bool)
        or not isinstance(multiplier, (int, float))
        or multiplier < 0
    ):
        raise ValueError("Multiplier must be a non-negative number.")

    return round(patient["bill"] * multiplier, 2)


def generate_patient_hash(p_id):
    """Generate a SHA-256 digest for a patient identifier."""
    return hashlib.sha256(p_id.encode("utf-8")).hexdigest()


def generate_ward_token():
    """Generate a cryptographically secure four-digit token."""
    return secrets.randbelow(9000) + 1000


def export_patient_ledger(filename="patient_records.txt"):
    """Export patient records to a UTF-8 text file."""
    with open(filename, "w", encoding="utf-8") as ledger_file:
        ledger_file.write(str(PATIENT_RECORDS))

    print(f"Patient ledger exported to: {filename}")


def get_ward_summary():
    """Return the number of currently admitted patients."""
    return sum(
        patient["is_admitted"]
        for patient in PATIENT_RECORDS.values()
    )


def main():
    """Run the hospital patient management demonstration."""
    admit_patient("P104", "Alice Walker", "General")
    discharge_patient("P101")

    print("Is P103 admitted:", verify_admission_status("P103"))
    print("Cost calculated:", calculate_treatment_cost("P103"))
    print("Patient Hash:", generate_patient_hash("P103"))
    print("Ward Token:", generate_ward_token())

    export_patient_ledger()
    print("Active admits:", get_ward_summary())


if __name__ == "__main__":
    main()
