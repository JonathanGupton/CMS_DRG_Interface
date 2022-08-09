"""Module containing the fields used in the CMS DRG Batch Interface"""

from abc import ABC, abstractmethod
from collections import deque
from typing import Sequence

from src.field_literal import (
    DischargeDispositionValue,
    PayerValue,
    SexValue,
    ApplyHACLogicValue,
)
from src.value_container import Date, Diagnosis, ProcedureCode


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
            raise ValueError(
                f"Invalid patient_name {patient_name}"
                f" patient_name must be alphanumeric"
            )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.patient_name}")'

    def __str__(self) -> str:
        return self.patient_name[: self.field_length].ljust(self.field_length)


class MedicalRecordNumber(Field):
    """
    Medical record number.
    Length 13.
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
            raise ValueError(
                f"Invalid medical record number "
                f"{medical_record_number}.  medical_record_number "
                f"must be alphanumeric."
            )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.medical_record_number}")'

    def __str__(self):
        return self.medical_record_number[: self.field_length].ljust(self.field_length)


class AccountNumber(Field):
    """
    Account number.
    Length 17.
    Alphanumeric.
    Left-justified, blank-filled.
    All blanks if no value is entered.
    """

    field_length = 17

    def __init__(self, account_number: str = "") -> None:
        super().__init__()
        if account_number.isalnum():
            self.account_number = account_number
        else:
            raise ValueError(
                f"Invalid account number "
                f"{account_number}.  account_number "
                f"must be alphanumeric."
            )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.account_number}")'

    def __str__(self):
        return self.account_number[: self.field_length].ljust(self.field_length)


class AdmitDate(Field):
    """
    Admit Date field.
    Field length 10.
    mm/dd/yyyy format.
    All blanks if no value is entered.
    Used by grouper in age and LOS calculations.
    """

    def __init__(self, admit_date: Date) -> None:
        self.admit_date = admit_date

    def __str__(self):
        return str(self.admit_date)


class DischargeDate(Field):
    """
    Discharge Date field.
    Field length 10.
    mm/dd/yyyy format.
    All blanks if no value is entered.
    Used by grouper in LOS calculations.
    """

    def __init__(self, discharge_date: Date) -> None:
        self.discharge_date = discharge_date

    def __str__(self):
        return str(self.discharge_date)


class DischargeStatus(Field):
    """
    UB-04 discharge status.
    Right-justified
    Zero-filled
    """

    field_length = 2

    def __init__(self, discharge_disposition: DischargeDispositionValue) -> None:
        self.discharge_disposition = discharge_disposition

    def __str__(self):
        return str(self.discharge_disposition.value).zfill(self.field_length)


class PrimaryPayer(Field):
    """
    Primary pay source.
    Right-justified.
    Zero-filled.
    """

    field_length = 2

    def __init__(self, primary_payer: PayerValue) -> None:
        self.primary_payer = primary_payer

    def __str__(self) -> str:
        return str(self.primary_payer.value).zfill(self.field_length)


class LOS(Field):
    """
    Length of stay
    Right-justified
    Zero-filled
    All blanks if no value is entered.
    Calculated LOS overrides enter LOS.
    Valid values 00000 - 45291
    """

    min_days = 0
    max_days = 45291
    field_length = 5

    def __init__(self, length_of_stay: int) -> None:
        if (length_of_stay < self.min_days) or (length_of_stay > self.max_days):
            raise ValueError(
                f"Invalid length of stay.  length_of_stay must be "
                f"more than {self.min_days} and less than "
                f"{self.max_days}"
            )
        self.length_of_stay = length_of_stay

    def __str__(self) -> str:
        return str(self.length_of_stay).zfill(self.field_length)


class BirthDate(Field):
    """
    Birth date.
    mm/dd/yyyy format.
    All blanks if no value is entered.
    Used in CMS Grouper's age calculation.
    """

    def __init__(self, birth_date: Date) -> None:
        self.birth_date = birth_date

    def __str__(self) -> str:
        return str(self.birth_date)


class Age(Field):
    """
    Age
    Right justified, zero-filled.
    Valid values:  0 - 124 years
    Calculated age (admit date minus birth date) takes precedence over
    entered age.
    """

    min_age = 0
    max_age = 124
    field_length = 3

    def __init__(self, age: int) -> None:
        if (age < self.min_age) or (age > self.max_age):
            raise ValueError(
                f"Invalid age {age}.  age must be between "
                f"{self.min_age} and {self.max_age}."
            )
        self.age = age

    def __str__(self):
        return str(self.age).zfill(self.field_length)


class Sex(Field):
    """
    Sex
    Numeric
    """

    def __init__(self, sex: SexValue) -> None:
        self.sex = sex

    def __str__(self) -> str:
        return str(self.sex.value)


class AdmitDiagnosis(Field):
    """
    Admit diagnosis
    Left-justified, blank-filled.
    Diagnosis code without decimal.
    All blanks if no value is entered.
    """

    field_length = 7

    def __init__(self, admit_diagnosis: Diagnosis) -> None:
        self.admit_diagnosis = admit_diagnosis

    def __str__(self):
        return str(self.admit_diagnosis.code)


class PrincipalDiagnosis(Field):
    """
    Principal Diagnosis
    First 7 bytes left-justified, blank filled without decimals.
    Eighth byte represents POA indicator.
    """

    def __init__(self, principal_diagnosis: Diagnosis) -> None:
        self.principal_diagnosis = principal_diagnosis

    def __str__(self):
        return str(self.principal_diagnosis)


class SecondaryDiagnoses(Field):
    """
    Secondary Diagnoses
    First 7 bytes left-justified, blank-filled.
    Eighth byte represents POA indicator.
    Up to 24 diagnoses without decimals.
    """

    max_secondary_diagnoses = 24

    def __init__(self, secondary_diagnoses: Sequence[Diagnosis]) -> None:
        self.secondary_diagnoses = deque(
            [Diagnosis()] * self.max_secondary_diagnoses,
            maxlen=self.max_secondary_diagnoses,
        )
        for i, dx in enumerate(secondary_diagnoses[: self.max_secondary_diagnoses]):
            self.secondary_diagnoses[i] = dx

    def __str__(self) -> str:
        return "".join(map(str, self.secondary_diagnoses))


class PrincipalProcedure(Field):
    """
    Procedure code
    Seven left-justified characters, blank-filled.
    """

    def __init__(self, principal_procedure: ProcedureCode) -> None:
        self.principal_procedure = principal_procedure

    def __str__(self) -> str:
        return str(self.principal_procedure)


class SecondaryProcedures(Field):
    """
    Procedure codes
    Seven left-justified characters, blank-filled.
    Up to 24 procedure codes without decimal.
    """

    max_secondary_procedures = 24

    def __init__(self, secondary_procedures: Sequence[ProcedureCode]) -> None:
        self.secondary_procedures = deque(
            [ProcedureCode()] * self.max_secondary_procedures,
            maxlen=self.max_secondary_procedures,
        )
        for i, procedure in enumerate(
            secondary_procedures[: self.max_secondary_procedures]
        ):
            self.secondary_procedures[i] = procedure

    def __str__(self) -> str:
        return "".join(map(str, self.secondary_procedures))


class ProcedureDate(Field):
    """
    Procedure dates
    The format is mm/dd/yyyy (for future use with POA logic)
    All blanks if no value is entered.
    Up to 25 procedure dates accepted.
    """

    max_procedure_dates = 25

    def __init__(self, procedure_dates: Sequence[Date]) -> None:

        self.procedure_dates = deque(
            [Date()] * self.max_procedure_dates,
            maxlen=self.max_procedure_dates,
        )
        for i, date in enumerate(procedure_dates[: self.max_procedure_dates]):
            self.procedure_dates[i] = date

    def __str__(self) -> str:
        return "".join(map(str, self.procedure_dates))


class ApplyHACLogic(Field):
    """
    Value X or Z to be captured for use with HAC logic.
    These values reflect whether a hospital requires POA reporting.
    X = Exempt from POA indicator reporting
    Z = Requires POA indicator reporting

    Note:  If value no X or Z an error code may result
    """

    def __init__(self, apply_hac_logic_value: ApplyHACLogicValue) -> None:
        self.apply_hac_logic_value = apply_hac_logic_value

    def __str__(self):
        return str(self.apply_hac_logic_value.value)


class UNUSED(Field):
    """
    UNUSED

    This field is noted to be unused in the CMS Grouper UserGuide
    """

    field_length = 1

    def __init__(self):
        self.field_value = ""

    def __str__(self):
        return self.field_value.ljust(self.field_length)


class OptionalInformation(Field):
    """
    Optional field
    Left justified, blank-filled.
    All blanks if no value is entered.
    """

    field_length = 72

    def __init__(self, optional_information: str) -> None:
        self.optional_information = optional_information

    def __str__(self):
        return self.optional_information[: self.field_length].ljust(self.field_length)


class Filler(Field):
    """
    Filler
    Not used
    Blank-filled
    """

    field_length = 25

    def __init__(self):
        self.filler = ""

    def __str__(self):
        return self.filler.ljust(self.field_length)
