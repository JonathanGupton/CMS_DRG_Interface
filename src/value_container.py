"""Module containing the complex objects used by the grouper"""
import datetime
from typing import Optional

from src.field_literal import PresentOnAdmissionValue


def remove_decimal(text: str) -> str:
    """Remove the decimal from ICD-9/ICD-10 codes when present"""
    return text.replace(".", "")


class Date:
    """
    Date class used for all date fields
    mm/dd/yyyy format
    All blanks if no value is entered.
    """

    date_format = r"%m/%d/%Y"
    field_length = 10

    def __init__(self, date: Optional[datetime.date] = None) -> None:
        self.date = date

    def __str__(self):
        if self.date:
            return self.date.strftime(self.date_format)
        else:
            return " " * self.field_length


class DiagnosisCode:
    """
    Class containing the ICD-9/ICD-10 diagnosis code value
    Left-justified, blank filled
    Diagnosis code without decimal.
    All blanks if no value is entered.
    """

    max_len = 7

    def __init__(self, code: Optional[str] = None) -> None:
        if not code:
            self.code = ""
            return
        code = remove_decimal(code)
        if not code.isalnum():
            raise ValueError
        self.code = code

    def __str__(self) -> str:
        return self.code.ljust(self.max_len)


class Diagnosis:
    """
    Diagnosis field value containing the diagnosis code and POA indicator
    """

    def __init__(
        self,
        diagnosis_code: Optional[DiagnosisCode] = None,
        poa: Optional[PresentOnAdmissionValue] = None,
    ):
        if not diagnosis_code:
            self.code = DiagnosisCode()
        else:
            self.code = diagnosis_code

        if not poa:
            self.poa = PresentOnAdmissionValue.NONE_TYPE
        else:
            self.poa = poa

    def __str__(self):
        return str(self.code) + str(self.poa.value)


class ProcedureCode:
    """
    Class containing the ICD-9/ICD-10 procedure code value
    Left-justified, blank filled
    Procedure code without decimal.
    All blanks if no value is entered.
    """
    max_len = 7

    def __init__(self, procedure_code: Optional[str] = None) -> None:
        if not procedure_code:
            self.procedure_code = ""
            return

        procedure_code = remove_decimal(procedure_code)
        if not procedure_code.isalnum():
            raise ValueError
        self.procedure_code = procedure_code

    def __str__(self):
        if not self.procedure_code:
            return " " * self.max_len
        else:
            return self.procedure_code.ljust(self.max_len)


class Procedure:
    """
    Procedure object containing the procedure code and procedure date information
    """
    __slots__ = ["procedure_code", "date"]

    def __init__(
        self, procedure_code: Optional[ProcedureCode] = None, date: Optional[Date] = None
    ) -> None:
        if not procedure_code:
            self.procedure_code = Procedure()
        else:
            self.procedure_code = procedure_code

        if not date:
            self.date = Date()
        else:
            self.date = date
