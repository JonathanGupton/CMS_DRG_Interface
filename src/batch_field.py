"""Module containing the fields used in the CMS DRG Batch Interface"""

from __future__ import annotations
from collections import deque
from typing import Sequence, Optional, Type, Union

from src.field_literal import (
    ApplyHACLogicValue,
    DischargeDispositionValue,
    PayerValue,
    SexValue,
    MedicalSurgicalIndicatorValue,
    DRGReturnCodeValue,
    MSGMCEEditReturnCodeValue,
    PrincipalDiagnosisEditReturnFlagValue,
    PrincipalDiagnosisHospitalAcquiredConditionAssignmentCriteriaValue,
    DiagnosisHospitalAcquiredConditionUsageValue,
    SecondaryDiagnosisEditReturnFlagValue,
    SecondaryDiagnosisHospitalAcquiredConditionAssignmentCriteriaValue,
    ProcedureEditReturnFlagValue,
    ProcedureHACAssignmentCriteriaValue,
    DRGCCMCCUsageValue,
    HACStatusValue,
)
from src.field import Field
from src.value_container import Date, Diagnosis, DiagnosisCode, ProcedureCode


FIELD_LITERAL = Union[
    ApplyHACLogicValue,
    DischargeDispositionValue,
    PayerValue,
    SexValue,
    MedicalSurgicalIndicatorValue,
    DRGReturnCodeValue,
    MSGMCEEditReturnCodeValue,
    PrincipalDiagnosisEditReturnFlagValue,
    PrincipalDiagnosisHospitalAcquiredConditionAssignmentCriteriaValue,
    DiagnosisHospitalAcquiredConditionUsageValue,
    SecondaryDiagnosisEditReturnFlagValue,
    SecondaryDiagnosisHospitalAcquiredConditionAssignmentCriteriaValue,
    ProcedureEditReturnFlagValue,
    ProcedureHACAssignmentCriteriaValue,
    DRGCCMCCUsageValue,
    HACStatusValue,
]


def is_alphanumeric_or_space(text: str) -> bool:
    """Check if a string contains only alphanumeric or space values"""
    return all(char.isalnum() or char.isspace() for char in text)


def parse_field_substring(
    substr: str,
    n_fields: int,
    field_len: int,
    break_values: Sequence[str],
    cast: Type[int] | Type[str],
    value_literal,
) -> list[FIELD_LITERAL]:
    """
    Process the field substrings into the appropriate field literal values

    Args:
        substr: The substring to be parsed, e.g. the 10-character HAC Usage field
        n_fields: Number of fields in the substring
        field_len: Length of each field in the substring
        break_values: The values to break the operation, typically "00", "0", or "  "
        cast:  The object type to supply to the value_type, typically int or str
        value_literal: The field literal type to be created

    Return:
        Sequence[value_literal]
    """
    position = 0
    value_collection = []
    for _ in range(n_fields):
        value = substr[position : position + field_len]
        if value in break_values:
            if not value_collection:
                value_collection.append(value_literal(cast(value)))
            break
        else:
            value_collection.append(value_literal(cast(value)))
            position += field_len
    return value_collection


class PatientName(Field):
    """
    Patient Name field

    Length 31
    Alphanumeric
    Left justified, blank-filled.
    All blanks if no value is entered.
    """

    field_length = 31
    position = 0
    occurrence = 1
    name = "patient_name"

    def __init__(self, value: str = "") -> None:
        if is_alphanumeric_or_space(value):
            super().__init__(value)
        else:
            raise ValueError(
                f"Invalid patient_name {value}" f" patient_name must be alphanumeric"
            )

    def __str__(self) -> str:
        return self.value[: self.field_length].ljust(self.field_length)

    @classmethod
    def parse_field_string(cls, field_str: str) -> str:
        return field_str.strip()


class MedicalRecordNumber(Field):
    """
    Medical record number.
    Length 13.
    Alphanumeric.
    Left-justified, blank-filled.
    All blanks if no value is entered.
    """

    field_length = 13
    position = 31
    occurrence = 1
    name = "medical_record_number"

    def __init__(self, value: str = "") -> None:
        if value.isalnum():
            super().__init__(value)
        else:
            raise ValueError(
                f"Invalid medical record number "
                f"{value}.  medical_record_number "
                f"must be alphanumeric."
            )

    def __str__(self) -> str:
        return self.value[: self.field_length].ljust(self.field_length)

    @classmethod
    def parse_field_string(cls, field_str) -> str:
        return field_str.strip()


class AccountNumber(Field):
    """
    Account number.
    Length 17.
    Alphanumeric.
    Left-justified, blank-filled.
    All blanks if no value is entered.
    """

    field_length = 17
    position = 44
    occurrence = 1
    name = "account_number"

    def __init__(self, value: str = "") -> None:
        if value.isalnum():
            super().__init__(value)
        else:
            raise ValueError(
                f"Invalid account number {value}.  account_number "
                f"must be alphanumeric."
            )

    def __str__(self) -> str:
        return self.value[: self.field_length].ljust(self.field_length)

    @classmethod
    def parse_field_string(cls, field_str: str) -> str:
        return field_str.strip()


class AdmitDate(Field):
    """
    Admit Date field.
    Field length 10.
    mm/dd/yyyy format.
    All blanks if no value is entered.
    Used by grouper in age and LOS calculations.
    """

    field_length = Date.field_length
    position = 61
    occurrence = 1
    name = "admit_date"

    def __init__(self, value: Date) -> None:
        super().__init__(value)

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def parse_field_string(cls, field_str: str) -> Date:
        return Date.from_string(field_str)


class DischargeDate(Field):
    """
    Discharge Date field.
    Field length 10.
    mm/dd/yyyy format.
    All blanks if no value is entered.
    Used by grouper in LOS calculations.
    """

    field_length = Date.field_length
    position = 71
    occurrence = 1
    name = "discharge_date"

    def __init__(self, value: Date) -> None:
        super().__init__(value)

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def parse_field_string(cls, field_str: str) -> Date:
        return Date.from_string(field_str)


class DischargeStatus(Field):
    """
    UB-04 discharge status.
    Right-justified
    Zero-filled
    """

    field_length = 2
    position = 81
    occurrence = 1
    name = "discharge_status"

    def __init__(self, value: DischargeDispositionValue) -> None:
        super().__init__(value)

    def __str__(self):
        return str(self.value.value).zfill(self.field_length)

    @classmethod
    def parse_field_string(cls, field_str: str) -> DischargeDispositionValue:
        return DischargeDispositionValue(int(field_str))


class PrimaryPayer(Field):
    """
    Primary pay source.
    Right-justified.
    Zero-filled.
    """

    field_length = 2
    position = 83
    occurrence = 1
    name = "primary_payer"

    def __init__(self, value: PayerValue) -> None:
        super().__init__(value)

    def __str__(self) -> str:
        return str(self.value.value).zfill(self.field_length)

    @classmethod
    def parse_field_string(cls, field_str: str) -> PayerValue:
        return PayerValue(int(field_str))


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
    position = 85
    occurrence = 1
    name = "los"

    def __init__(self, value: int) -> None:
        if (value < self.min_days) or (value > self.max_days):
            raise ValueError(
                f"Invalid length of stay.  length_of_stay must be "
                f"more than {self.min_days} and less than "
                f"{self.max_days}"
            )
        super().__init__(value)

    def __str__(self) -> str:
        return str(self.value).zfill(self.field_length)

    @classmethod
    def parse_field_string(cls, field_str: str) -> int:
        return int(field_str)


class BirthDate(Field):
    """
    Birth date.
    mm/dd/yyyy format.
    All blanks if no value is entered.
    Used in CMS Grouper's age calculation.
    """

    field_length = Date.field_length
    position = 90
    name = "birth_date"

    def __init__(self, value: Date) -> None:
        super().__init__(value)

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def parse_field_string(cls, field_str: str) -> Date:
        return Date.from_string(field_str)


class Age(Field):
    """
    Age
    Right justified, zero-filled.
    Valid values:  0 - 124 years
    Calculated age (admit date minus birthdate) takes precedence over
    entered age.
    """

    min_age = 0
    max_age = 124
    field_length = 3
    position = 100
    occurrence = 1
    name = "age"

    def __init__(self, value: int) -> None:
        if (value < self.min_age) or (value > self.max_age):
            raise ValueError(
                f"Invalid age {value}.  age must be between "
                f"{self.min_age} and {self.max_age}."
            )
        super().__init__(value)

    def __str__(self):
        return str(self.value).zfill(self.field_length)

    @classmethod
    def parse_field_string(cls, field_str: str) -> int:
        return int(field_str)


class Sex(Field):
    """
    Sex
    Numeric
    """

    position = 103
    field_length = 1
    occurrence = 1
    name = "sex"

    def __init__(self, sex: SexValue) -> None:
        super().__init__(sex)

    def __str__(self) -> str:
        return str(self.value.value)

    @classmethod
    def parse_field_string(cls, field_str: str) -> SexValue:
        return SexValue(int(field_str))


class AdmitDiagnosis(Field):
    """
    Admit diagnosis
    Left-justified, blank-filled.
    Diagnosis code without decimal.
    All blanks if no value is entered.
    """

    position = 104
    field_length = 7
    occurrence = 1
    name = "admit_diagnosis"

    def __init__(self, value: DiagnosisCode) -> None:
        super().__init__(value)

    def __str__(self):
        return str(self.value)

    @classmethod
    def parse_field_string(cls, field_str: str) -> DiagnosisCode:
        return DiagnosisCode(field_str)


class PrincipalDiagnosis(Field):
    """
    Principal Diagnosis
    First 7 bytes left-justified, blank filled without decimals.
    Eighth byte represents POA indicator.
    """

    field_length = 8
    position = 111
    name = "principal_diagnosis"

    def __init__(self, value: Diagnosis) -> None:
        super().__init__(value)

    def __str__(self):
        return str(self.value)

    @classmethod
    def parse_field_string(cls, field_str: str) -> Diagnosis:
        return Diagnosis.extract_from_output(field_str)


class SecondaryDiagnoses(Field):
    """
    Secondary Diagnoses
    First 7 bytes left-justified, blank-filled.
    Eighth byte represents POA indicator.
    Up to 24 diagnoses without decimals.
    """

    position = 119
    occurrence = 24
    field_length = occurrence * Diagnosis.field_length
    name = "secondary_diagnoses"

    def __init__(self, value: Sequence[Diagnosis]) -> None:
        secondary_diagnoses = deque(
            [Diagnosis()] * self.occurrence,
            maxlen=self.occurrence,
        )
        for i, dx in enumerate(value[: self.occurrence]):
            secondary_diagnoses[i] = dx

        super().__init__(secondary_diagnoses)

    def __str__(self) -> str:
        return "".join(map(str, self.value))

    @classmethod
    def parse_field_string(cls, field_str: str) -> Sequence[Diagnosis]:
        diagnoses = []
        position = 0
        for i in range(cls.occurrence):
            next_position = position + Diagnosis.field_length
            diagnoses.append(
                Diagnosis.extract_from_output(field_str[position:next_position])
            )
            position = next_position
        return diagnoses


class PrincipalProcedure(Field):
    """
    Procedure code
    Seven left-justified characters, blank-filled.
    """

    position = 311
    field_length = 7
    occurrence = 1
    name = "principal_procedure"

    def __init__(self, principal_procedure: Optional[ProcedureCode] = None) -> None:
        principal_procedure = (
            principal_procedure if principal_procedure else ProcedureCode()
        )
        super().__init__(principal_procedure)

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def parse_field_string(cls, field_str: str) -> ProcedureCode:
        return ProcedureCode(field_str)


class SecondaryProcedures(Field):
    """
    Procedure codes
    Seven left-justified characters, blank-filled.
    Up to 24 procedure codes without decimal.
    """

    occurrence = 24
    position = 318
    field_length = occurrence * ProcedureCode.field_length
    name = "secondary_procedures"

    def __init__(self, value: Optional[Sequence[ProcedureCode]] = None) -> None:
        secondary_procedures_queue = deque(
            [ProcedureCode()] * self.occurrence,
            maxlen=self.occurrence,
        )
        if value:
            for i, procedure in enumerate(value[: self.occurrence]):
                secondary_procedures_queue[i] = procedure
        super().__init__(secondary_procedures_queue)

    def __str__(self) -> str:
        return "".join(map(str, self.value))

    @classmethod
    def parse_field_string(cls, field_str: str) -> Sequence[ProcedureCode]:
        procedures = []
        position = 0
        for i in range(cls.occurrence):
            next_position = position + ProcedureCode.field_length
            code_str = field_str[position:next_position].strip()
            if not code_str:
                break
            procedures.append(ProcedureCode(code_str))
            position = next_position
        return procedures


class ProcedureDates(Field):
    """
    Procedure dates
    The format is mm/dd/yyyy (for future use with POA logic)
    All blanks if no value is entered.
    Up to 25 procedure dates accepted.
    """

    position = 486
    occurrence = 25
    field_length = occurrence * Date.field_length
    name = "procedure_date"

    def __init__(self, value: Optional[Sequence[Date]] = None) -> None:

        procedure_dates_queue = deque(
            [Date()] * self.occurrence,
            maxlen=self.occurrence,
        )
        if value:
            for i, date in enumerate(value[: self.occurrence]):
                procedure_dates_queue[i] = date
        super().__init__(procedure_dates_queue)

    def __str__(self) -> str:
        return "".join(map(str, self.value))

    @classmethod
    def parse_field_string(cls, field_str: str) -> Sequence[Date]:
        procedure_dates = []
        position = 0
        for i in range(cls.occurrence):
            next_position = position + Date.field_length
            date_str = field_str[position:next_position].strip()
            if not date_str:
                break
            procedure_dates.append(Date.from_string(date_str))
            position = next_position
        return procedure_dates


class ApplyHACLogic(Field):
    """
    Value X or Z to be captured for use with HAC logic.
    These values reflect whether a hospital requires POA reporting.
    X = Exempt from POA indicator reporting
    Z = Requires POA indicator reporting

    Note:  If value no X or Z an error code may result
    """

    position = 736
    field_length = 1
    occurrence = 1
    name = "apply_hac_logic"

    def __init__(self, apply_hac_logic_value: ApplyHACLogicValue) -> None:
        super().__init__(apply_hac_logic_value)

    def __str__(self):
        return str(self.value.value)

    @classmethod
    def parse_field_string(cls, field_str: str) -> ApplyHACLogicValue:
        return ApplyHACLogicValue(field_str)


class UNUSED(Field):
    """
    UNUSED

    This field is noted to be unused in the CMS Grouper UserGuide
    """

    position = 737
    field_length = 1
    occurrence = 1
    name = "unused"

    def __init__(self):
        super().__init__("")

    def __str__(self):
        return self.value.ljust(self.field_length)

    @classmethod
    def parse_field_string(cls, field_str: str):
        raise NotImplementedError


class OptionalInformation(Field):
    """
    Optional field
    Left justified, blank-filled.
    All blanks if no value is entered.
    """

    position = 738
    field_length = 72
    occurrence = 1
    name = "optional_information"

    def __init__(self, optional_information: str = "") -> None:
        super().__init__(optional_information)

    def __str__(self):
        return self.value[: self.field_length].ljust(self.field_length)

    @classmethod
    def parse_field_string(cls, field_str: str):
        return field_str.strip()


class Filler(Field):
    """
    Filler
    Not used
    Blank-filled
    """

    position = 810
    field_length = 25
    occurrence = 1
    name = "filler"

    def __init__(self):
        super().__init__("")

    def __str__(self):
        return self.value.ljust(self.field_length)

    @classmethod
    def parse_field_string(cls, field_str: str):
        raise NotImplementedError


class MSGMCEVersionUsed(Field):
    """
    Version of the software used to process the claim.
    Right-justified, blank-filled.
    Stored without decimal point.
    """

    position = 835
    field_length = 3
    occurrence = 1
    name = "msg_mce_version_used"

    def __init__(self, msg_mce_version_used) -> None:
        super().__init__(msg_mce_version_used)

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def parse_field_string(cls, field_str: str) -> str:
        return field_str


class InitialDRG(Field):
    """
    Initial diagnosis related group
    Right-justified, zero filled.
    """

    position = 838
    field_length = 3
    occurrence = 1
    name = "initial_drg"

    def __init__(self, initial_drg: int) -> None:
        super().__init__(initial_drg)

    def __str__(self):
        return str(self.value)

    @classmethod
    def parse_field_string(cls, field_str: str) -> int:
        return int(field_str)


class InitialMSIndicator(Field):
    """
    Initial medical/surgical indicator
    """

    position = 841
    field_length = 1
    occurrence = 1
    name = "initial_medical_surgical_indicator"

    def __init__(
        self, medical_surgical_indicator_value: MedicalSurgicalIndicatorValue
    ) -> None:
        super().__init__(medical_surgical_indicator_value)

    def __str__(self):
        return self.value.name

    @classmethod
    def parse_field_string(cls, field_str: str) -> MedicalSurgicalIndicatorValue:
        return MedicalSurgicalIndicatorValue(int(field_str))


class FinalMDC(Field):
    """
    Major diagnostic category.
    Right-justified, zero-filled.
    """

    position = 841
    field_length = 3
    occurrence = 1
    name = "final_mdc"

    def __init__(self, final_mdc: int) -> None:
        super().__init__(final_mdc)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(cls, field_str: str) -> int:
        return int(field_str)


class FinalDRG(Field):
    """
    Final diagnosis related group.
    Right-justified, zero-filled.
    """

    position = 844
    field_length = 3
    occurrence = 1
    name = "final_drg"

    def __init__(self, final_drg: int) -> None:
        super().__init__(final_drg)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(cls, field_str: str) -> int:
        return int(field_str)


class FinalMSIndicator(Field):
    """
    Final Medical/Surgical Indicator
    """

    position = 847
    field_length = 1
    occurrence = 1
    name = "final_medical_surgical_indicator"

    def __init__(self, med_surg_indicator: MedicalSurgicalIndicatorValue) -> None:
        super().__init__(med_surg_indicator)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(cls, field_str: str) -> MedicalSurgicalIndicatorValue:
        return MedicalSurgicalIndicatorValue(int(field_str))


class DRGReturnCode(Field):
    """
    DRG Return Code
    Numeric.
    Right-justified, zero-filled.
    """

    position = 848
    field_length = 2
    occurrence = 1
    name = "drg_return_code"

    def __init__(self, drg_return_code: DRGReturnCodeValue) -> None:
        super().__init__(drg_return_code)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(cls, field_str: str) -> DRGReturnCodeValue:
        return DRGReturnCodeValue(int(field_str))


class MSGMCEEditReturnCode(Field):
    """
    MSG/MCE edit return code
    Four-character return code, right-justified, zero-filled.
    """

    position = 850
    field_length = 4
    occurrence = 1
    name = "msg_mce_edit_return_code"

    def __init__(self, msg_mce_edit_return_code: MSGMCEEditReturnCodeValue) -> None:
        super().__init__(msg_mce_edit_return_code)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(cls, field_str: str) -> MSGMCEEditReturnCodeValue:
        return MSGMCEEditReturnCodeValue(int(field_str))


class DiagnosisCodeCount(Field):
    """
    Diagnosis code count
    Number of diagnosis codes processed.
    Right-justified, zero-filled.
    This field does not include the admit diagnosis.
    """

    position = 854
    field_length = 2
    occurrence = 1
    name = "diagnosis_code_count"

    def __init__(self, diagnosis_code_count: int) -> None:
        super().__init__(diagnosis_code_count)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(cls, field_str: str) -> int:
        return int(field_str)


class ProcedureCodeCount(Field):
    """
    Procedure code count
    Number of procedure codes processed.
    Right-justified, zero-filled.
    """

    position = 856
    field_length = 2
    occurrence = 1
    name = "procedure_code_count"

    def __init__(self, procedure_code_count: int) -> None:
        super().__init__(procedure_code_count)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(cls, field_str: str) -> int:
        return int(field_str)


class PrincipalDiagnosisEditReturnFlag(Field):
    """
    Principal diagnosis edit return flag
    Two-byte flag.
    Right-justified, zero-filled.
    A maximum of four flags can be returned for each diagnosis code.
    """

    return_flag_length = 2
    max_return_flags = 4
    position = 858
    field_length = return_flag_length * max_return_flags
    occurrence = 1
    name = "principal_diagnosis_edit_return_flag"

    def __init__(self, principal_diagnosis_edit_return_flag):
        super().__init__(principal_diagnosis_edit_return_flag)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(
        cls, field_str: str
    ) -> Sequence[PrincipalDiagnosisEditReturnFlagValue]:
        val = parse_field_substring(
            substr=field_str,
            n_fields=cls.max_return_flags,
            field_len=cls.return_flag_length,
            break_values=["00"],
            cast=int,
            value_literal=PrincipalDiagnosisEditReturnFlagValue,
        )
        return val


class PrincipalDiagnosisHospitalAcquiredConditionCriteria(Field):
    """
    Principal diagnosis hospital acquired condition criteria
    """

    position = 866
    n_criteria_fields = 5
    criteria_field_length = 2
    field_length = n_criteria_fields * criteria_field_length
    occurrence = 1
    name = "principal_diagnosis_hospital_acquired_condition_assignment_criteria"

    def __init__(self, principal_diagnosis_hac_assignment_criteria):
        super().__init__(principal_diagnosis_hac_assignment_criteria)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(
        cls, field_str
    ) -> Sequence[PrincipalDiagnosisHospitalAcquiredConditionAssignmentCriteriaValue]:
        return_flags = parse_field_substring(
            substr=field_str,
            n_fields=cls.n_criteria_fields,
            field_len=cls.criteria_field_length,
            break_values=["00", "11"],
            cast=str,
            value_literal=PrincipalDiagnosisHospitalAcquiredConditionAssignmentCriteriaValue,
        )
        return return_flags


class PrincipalDiagnosisHospitalAcquiredConditionUsage(Field):
    """
    Principal diagnosis hospital acquired condition usage
    """

    position = 876
    usage_value_field_length = 1
    n_usage_fields = 5
    field_length = n_usage_fields * usage_value_field_length
    occurrence = 1
    name = "principal_diagnosis_hospital_acquired_condition_usage"

    def __init__(self, principal_diagnosis_hospital_acquired_condition_usage) -> None:
        super().__init__(principal_diagnosis_hospital_acquired_condition_usage)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(
        cls, field_str
    ) -> Sequence[DiagnosisHospitalAcquiredConditionUsageValue]:
        hac_usage = parse_field_substring(
            substr=field_str,
            n_fields=cls.n_usage_fields,
            field_len=cls.usage_value_field_length,
            break_values=["0", " "],
            cast=str,
            value_literal=DiagnosisHospitalAcquiredConditionUsageValue,
        )
        return hac_usage


class SecondaryDiagnosisReturnFlag(Field):
    """
    Secondary diagnosis return flag
    Two-byte flag.
    Right justified, zero-filled.
    A maximum of four flags can be returned for each diagnosis code.  These
    2-byte flags are a combination of information concerning every diagnosis
    from the DRG assignment and the editor.
    """

    position = 881
    return_flag_length = 2
    return_flags_per_diagnosis = 4
    return_flag_field_length = return_flag_length * return_flags_per_diagnosis
    occurrence = 24
    field_length = return_flag_field_length * occurrence

    name = "secondary_diagnosis_return_flag"

    def __init__(self, secondary_diagnosis_result_flags):
        super().__init__(secondary_diagnosis_result_flags)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(
        cls, field_str: str
    ) -> Sequence[Sequence[SecondaryDiagnosisEditReturnFlagValue]]:
        secondary_flags = []
        position = 0
        for _ in range(cls.occurrence):
            next_position = position + cls.return_flag_field_length
            dx_flags = parse_field_substring(
                substr=field_str[position : position + cls.return_flag_field_length],
                n_fields=cls.return_flags_per_diagnosis,
                field_len=cls.return_flag_length,
                break_values=["00"],
                cast=int,
                value_literal=SecondaryDiagnosisEditReturnFlagValue,
            )
            secondary_flags.append(dx_flags)
            position = next_position
        return secondary_flags


class SecondaryDiagnosisHospitalAcquiredConditionAssignmentCriteria(Field):
    """
    Hospital Acquired Condition (HAC) assigned
    #1-5. These 2-byte flags are a combination
    of information concerning every diagnosis
    from the DRG assignment and the editor.
    """

    hac_value_field_length = 2
    hac_value_occurrence = 5
    hac_field_length = hac_value_field_length * hac_value_occurrence
    position = 1073
    occurrence = 24
    field_length = hac_field_length * occurrence
    name = "secondary_diagnosis_hospital_acquired_condition_assignment_criteria"

    def __init__(
        self, secondary_diagnosis_hospital_acquired_condition_assignment_criteria
    ):
        super().__init__(
            secondary_diagnosis_hospital_acquired_condition_assignment_criteria
        )

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(
        cls, field_str: str
    ) -> Sequence[
        Sequence[SecondaryDiagnosisHospitalAcquiredConditionAssignmentCriteriaValue]
    ]:
        hac_criteria = []
        position = 0
        for _ in range(cls.occurrence):
            next_position = position + cls.hac_field_length
            dx_hac_criteria = parse_field_substring(
                substr=field_str[position:next_position],
                n_fields=cls.hac_value_occurrence,
                field_len=cls.hac_value_field_length,
                break_values=("  ", "00"),
                cast=str,
                value_literal=SecondaryDiagnosisHospitalAcquiredConditionAssignmentCriteriaValue,
            )
            hac_criteria.append(dx_hac_criteria)
            position = next_position
        return hac_criteria


class SecondaryDiagnosisHospitalAcquiredConditionUsage(Field):
    """
    Hospital Acquired Condition (HAC) usage
    #1-5. This 1-byte flag is a combination of
    information concerning every diagnosis from
    the DRG assignment and the editor.
    """

    hac_usage_value_length = 1
    hac_usage_value_occurrence = 5
    position = 1313
    usage_field_length = hac_usage_value_length * hac_usage_value_occurrence
    occurrence = 24
    field_length = usage_field_length * occurrence
    name = "secondary_diagnosis_hospital_acquired_condition_usage"

    def __init__(self, secondary_diagnosis_hospital_acquired_condition_usage):
        super().__init__(secondary_diagnosis_hospital_acquired_condition_usage)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(
        cls, field_str: str
    ) -> Sequence[Sequence[DiagnosisHospitalAcquiredConditionUsageValue]]:
        hac_usage = []
        position = 0
        for _ in range(cls.occurrence):
            next_position = position + cls.usage_field_length
            dx_hac_usage = parse_field_substring(
                substr=field_str[position:next_position],
                n_fields=cls.hac_usage_value_occurrence,
                field_len=cls.hac_usage_value_length,
                break_values=(" ", "0"),
                cast=str,
                value_literal=DiagnosisHospitalAcquiredConditionUsageValue,
            )
            hac_usage.append(dx_hac_usage)
            position = next_position
        return hac_usage


class ProcedureEditReturnFlag(Field):
    """ """

    position = 1433

    return_flag_value_length = 2
    return_flag_per_diagnosis = 4
    return_flag_field_length = return_flag_value_length * return_flag_per_diagnosis
    occurrence = 25
    field_length = occurrence * return_flag_field_length
    name = "procedure_edit_return_flag"

    def __init__(self, procedure_edit_return_flag):
        super().__init__(procedure_edit_return_flag)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(
        cls, field_str: str
    ) -> Sequence[Sequence[ProcedureEditReturnFlagValue]]:
        return_flags = []
        position = 0
        for _ in range(cls.occurrence):
            next_position = position + cls.return_flag_field_length
            proc_flags = parse_field_substring(
                substr=field_str[position:next_position],
                n_fields=cls.return_flag_per_diagnosis,
                field_len=cls.return_flag_value_length,
                break_values=("00",),
                cast=str,
                value_literal=ProcedureEditReturnFlagValue,
            )
            return_flags.append(proc_flags)
            position = next_position
        return return_flags


class ProcedureHospitalAcquiredConditionAssignmentCriteria(Field):
    """ """

    position = 1633
    occurrence = 25
    criteria_value_length = 2
    criteria_flag_per_diagnosis = 5
    criteria_field_length = criteria_value_length * criteria_flag_per_diagnosis
    field_length = occurrence * criteria_field_length
    name = "procedure_hospital_acquired_condition_assignment_criteria"

    def __init__(self, procedure_hospital_acquired_condition_assignment_criteria):
        super().__init__(procedure_hospital_acquired_condition_assignment_criteria)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(
        cls, field_str: str
    ) -> Sequence[Sequence[ProcedureHACAssignmentCriteriaValue]]:
        hac_assignment = []
        position = 0
        for _ in range(cls.occurrence):
            next_position = position + cls.criteria_field_length
            proc_hac_assignment = parse_field_substring(
                substr=field_str[position:next_position],
                n_fields=cls.criteria_flag_per_diagnosis,
                field_len=cls.criteria_value_length,
                break_values=("  ", "00"),
                cast=str,
                value_literal=ProcedureHACAssignmentCriteriaValue,
            )
            hac_assignment.append(proc_hac_assignment)
            position = next_position
        return hac_assignment


class InitialFourDigitDRG(Field):
    """Initial 4-digit DRG. Right-justified, zero-filled."""

    position = 1883
    field_length = 4
    occurrence = 1
    name = "initial_four_digit_drg"

    def __init__(self, initial_four_digit_drg) -> None:
        super().__init__(initial_four_digit_drg)

    def __str__(self) -> str:
        return self.value

    @classmethod
    def parse_field_string(cls, field_str: str) -> str:
        return field_str


class FinalFourDigitDRG(Field):
    """Final 4-digit DRG.  Right-justified, zero-filled."""

    position = 1887
    field_length = 4
    occurrence = 1
    name = "final_four_digit_drg"

    def __init__(self, final_four_digit_drg) -> None:
        super().__init__(final_four_digit_drg)

    def __str__(self) -> str:
        return self.value

    @classmethod
    def parse_field_string(cls, field_str: str) -> str:
        return field_str


class FinalDRGCCMCCUsage(Field):
    """Final DRG CC/MCC Usage"""

    position = 1891
    field_length = 1
    occurrence = 1
    name = "final_drg_cc_mcc_usage"

    def __init__(self, drg_cc_mcc_usage_value: DRGCCMCCUsageValue) -> None:
        super().__init__(drg_cc_mcc_usage_value)

    def __str__(self) -> str:
        return self.value.value

    @classmethod
    def parse_field_string(cls, field_str: str) -> DRGCCMCCUsageValue:
        return DRGCCMCCUsageValue(int(field_str))


class InitialDRGCCMCCUsage(Field):
    """Initial DRG CC/MCC Usage"""

    position = 1892
    field_length = 1
    occurrence = 1
    name = "initial_drg_cc_mcc_usage"

    def __init__(self, initial_drg_cc_mcc_usage: DRGCCMCCUsageValue) -> None:
        super().__init__(initial_drg_cc_mcc_usage)

    def __str__(self):
        pass

    @classmethod
    def parse_field_string(cls, field_str: str) -> DRGCCMCCUsageValue:
        return DRGCCMCCUsageValue(int(field_str))


class NumberOfUniqueHospitalAcquiredConditionsMet(Field):
    """The Number of unique hospital acquired conditions that have been met."""

    position = 1893
    field_length = 2
    occurrence = 1
    name = "number_of_unique_hospital_acquired_conditions_met"

    def __init__(self, number_of_unique_hospital_acquired_conditions_met):
        super().__init__(number_of_unique_hospital_acquired_conditions_met)

    def __str__(self):
        return str(self.value)

    @classmethod
    def parse_field_string(cls, field_str: str) -> int:
        return int(field_str)


class HospitalAcquiredConditionStatus(Field):
    """ """

    position = 1895
    field_length = 1
    occurrence = 1
    name = "hospital_acquired_condition_status"

    def __init__(self, hospital_acquired_condition_status) -> None:
        super().__init__(hospital_acquired_condition_status)

    def __str__(self):
        return self.value.value

    @classmethod
    def parse_field_string(cls, field_str: str) -> HACStatusValue:
        return HACStatusValue(int(field_str))


class CostWeight(Field):
    """
    The DRG cost weight
    This 7-byte field is displayed as 2 digits followed by a decimal point
    followed by 4 digits.
    """

    position = 1896
    field_length = 7
    occurrence = 1
    name = "cost_weight"

    def __init__(self, cost_weight) -> None:
        super().__init__(cost_weight)

    def __str__(self):
        return str(self.value)

    @classmethod
    def parse_field_string(cls, field_str: str) -> float:
        return float(field_str)
