"""Module containing the fields used in the CMS DRG Batch Interface"""


class Field:
    pass


class PatientName(Field):
    """
    Patient Name field

    Length 31
    Alphanumeric
    Left justified, blank-filled.
    All blanks if no value is entered.
    """
    max_len = 31

    def __init__(self, patient_name: str = ""):
        super().__init__()
        if patient_name.isalnum():
            self._text = patient_name
        else:
            raise ValueError(f"Invalid patient_name {patient_name}"
                             f" patient_name must be alphanumeric")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(\"{self._text}\")"

    def __str__(self) -> str:
        return self._text[:self.max_len].ljust(self.max_len)


class MedicalRecordNumber(Field):
    pass


class AccountNumber(Field):
    pass


class AdmitDate(Field):
    pass


class DischargeDate(Field):
    pass


class DischargeStatus(Field):
    pass


class PrimaryPayer(Field):
    pass


class LOS(Field):
    pass


class BirthDate(Field):
    pass


class Age(Field):
    pass


class Sex(Field):
    pass


class AdmitDiagnosis(Field):
    pass


class PrincipalDiagnosis(Field):
    pass


class SecondaryDiagnoses(Field):
    pass


class PrincipalProcedure(Field):
    pass


class SecondaryProcedures(Field):
    pass


class ProcedureDate(Field):
    pass


class ApplyHACLogic(Field):
    pass


class UNUSED(Field):
    pass


class OptionalInformation(Field):
    pass


class Filler(Field):
    pass
