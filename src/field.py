"""Module containing the fields used in the CMS DRG Batch Interface"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Diagnosis:
    code: str
    poa: str


@dataclass(frozen=True)
class Procedure:
    code: str
    date: str


class Date:
    pass


class Field(ABC):
    """Base Class used for all record fields"""

    @abstractmethod
    def __str__(self):
        raise NotImplementedError


class PatientName(Field):
    """
    Patient Name field

    Length 31
    Alphanumeric
    Left justified, blank-filled.
    All blanks if no value is entered.
    """
    field_length = 31

    def __init__(self, patient_name: str = "") -> None:
        super().__init__()
        if patient_name.isalnum():
            self.patient_name = patient_name
        else:
            raise ValueError(f"Invalid patient_name {patient_name}"
                             f" patient_name must be alphanumeric")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(\"{self.patient_name}\")"

    def __str__(self) -> str:
        return self.patient_name[:self.field_length].ljust(self.field_length)


class MedicalRecordNumber(Field):
    """
    Medical record number.
    Alphanumeric.
    Left-justified, blank-filled.
    All blanks if no value is entered.
    """
    field_length = 13

    def __init__(self, medical_record_number: str = "") -> None:
        super().__init__()
        if medical_record_number.isalnum():
            self.medical_record_number = medical_record_number
        else:
            raise ValueError(f"Invalid medical record number "
                             f"{medical_record_number}.  medical_record_number "
                             f"must be alphanumeric.")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(\"{self.medical_record_number}\")"

    def __str__(self):
        return self.medical_record_number[:self.field_length].ljust(self.field_length)


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
    def __init__(self):
        pass

    def __str__(self):
        return " "


class OptionalInformation(Field):
    pass


class Filler(Field):
    pass
