"""Module containing the fields used in the CMS DRG Batch Interface"""

from collections import deque
from typing import Sequence, Optional

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
    ProcedureHospitalAcquiredConditionAssignmentCriteriaValue,
    DRGCCMCCUsageValue,
    HACStatusValue,
)
from src.field import Field
from src.value_container import Date, Diagnosis, DiagnosisCode, ProcedureCode


def is_alphanumeric_or_space(text: str) -> bool:
    """Check if a string contains only alphanumeric or space values"""
    return all(char.isalnum() or char.isspace() for char in text)


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
    name = "patient_name"

    def __init__(self, patient_name: str = "") -> None:
        super().__init__()
        if is_alphanumeric_or_space(patient_name):
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

    @classmethod
    def extract_from_output(cls, output: str) -> str:
        return output[cls.position : cls.position + cls.field_length].strip()


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
    name = "medical_record_number"

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

    def __str__(self) -> str:
        return self.medical_record_number[: self.field_length].ljust(self.field_length)

    @classmethod
    def extract_from_output(cls, output) -> str:
        return output[cls.position : cls.position + cls.field_length].strip()


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
    name = "account_number"

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

    def __str__(self) -> str:
        return self.account_number[: self.field_length].ljust(self.field_length)

    @classmethod
    def extract_from_output(cls, output) -> str:
        return output[cls.position : cls.position + cls.field_length].strip()


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
    name = "admit_date"

    def __init__(self, admit_date: Date) -> None:
        self.admit_date = admit_date

    def __str__(self) -> str:
        return str(self.admit_date)

    @classmethod
    def extract_from_output(cls, output) -> Date:
        return Date.from_string(output[cls.position : cls.position + cls.field_length])


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
    name = "discharge_date"

    def __init__(self, discharge_date: Date) -> None:
        self.discharge_date = discharge_date

    def __str__(self) -> str:
        return str(self.discharge_date)

    @classmethod
    def extract_from_output(cls, output) -> Date:
        return Date.from_string(output[cls.position : cls.position + cls.field_length])


class DischargeStatus(Field):
    """
    UB-04 discharge status.
    Right-justified
    Zero-filled
    """

    field_length = 2
    position = 81
    name = "discharge_status"

    def __init__(self, discharge_disposition: DischargeDispositionValue) -> None:
        self.discharge_disposition = discharge_disposition

    def __str__(self):
        return str(self.discharge_disposition.value).zfill(self.field_length)

    @classmethod
    def extract_from_output(cls, output) -> str:
        dc_disposition = int(output[cls.position : cls.position + cls.field_length])
        return DischargeDispositionValue(dc_disposition)


class PrimaryPayer(Field):
    """
    Primary pay source.
    Right-justified.
    Zero-filled.
    """

    field_length = 2
    position = 83
    name = "primary_payer"

    def __init__(self, primary_payer: PayerValue) -> None:
        self.primary_payer = primary_payer

    def __str__(self) -> str:
        return str(self.primary_payer.value).zfill(self.field_length)

    @classmethod
    def extract_from_output(cls, output):
        payer = int(output[cls.position : cls.position + cls.field_length])
        return PayerValue(payer)


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
    name = "los"

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

    @classmethod
    def extract_from_output(cls, output):
        return int(output[cls.position : cls.position + cls.field_length])


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

    def __init__(self, birth_date: Date) -> None:
        self.birth_date = birth_date

    def __str__(self) -> str:
        return str(self.birth_date)

    @classmethod
    def extract_from_output(cls, output):
        return Date.from_string(output[cls.position : cls.position + cls.field_length])


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
    name = "age"

    def __init__(self, age: int) -> None:
        if (age < self.min_age) or (age > self.max_age):
            raise ValueError(
                f"Invalid age {age}.  age must be between "
                f"{self.min_age} and {self.max_age}."
            )
        self.age = age

    def __str__(self):
        return str(self.age).zfill(self.field_length)

    @classmethod
    def extract_from_output(cls, output):
        return int(output[cls.position : cls.position + cls.field_length])


class Sex(Field):
    """
    Sex
    Numeric
    """

    position = 103
    field_length = 1
    name = "sex"

    def __init__(self, sex: SexValue) -> None:
        self.sex = sex

    def __str__(self) -> str:
        return str(self.sex.value)

    @classmethod
    def extract_from_output(cls, output):
        sex = int(output[cls.position : cls.position + cls.field_length])
        return SexValue(sex)


class AdmitDiagnosis(Field):
    """
    Admit diagnosis
    Left-justified, blank-filled.
    Diagnosis code without decimal.
    All blanks if no value is entered.
    """

    position = 104
    field_length = 7
    name = "admit_diagnosis"

    def __init__(self, admit_diagnosis: DiagnosisCode) -> None:
        self.admit_diagnosis = admit_diagnosis

    def __str__(self):
        return str(self.admit_diagnosis)

    @classmethod
    def extract_from_output(cls, output):
        return DiagnosisCode(output[cls.position : cls.position + cls.field_length])


class PrincipalDiagnosis(Field):
    """
    Principal Diagnosis
    First 7 bytes left-justified, blank filled without decimals.
    Eighth byte represents POA indicator.
    """

    field_length = 8
    position = 111
    name = "principal_diagnosis"

    def __init__(self, principal_diagnosis: Diagnosis) -> None:
        self.principal_diagnosis = principal_diagnosis

    def __str__(self):
        return str(self.principal_diagnosis)

    @classmethod
    def extract_from_output(cls, output):
        diagnosis = output[cls.position : cls.position + cls.field_length]
        return Diagnosis.extract_from_output(diagnosis)


class SecondaryDiagnoses(Field):
    """
    Secondary Diagnoses
    First 7 bytes left-justified, blank-filled.
    Eighth byte represents POA indicator.
    Up to 24 diagnoses without decimals.
    """

    position = 119
    max_secondary_diagnoses = 24
    field_length = max_secondary_diagnoses * Diagnosis.field_length
    name = "secondary_diagnoses"

    def __init__(self, secondary_diagnoses: Sequence[Diagnosis]) -> None:
        self.secondary_diagnoses = deque(
            [Diagnosis()] * self.max_secondary_diagnoses,
            maxlen=self.max_secondary_diagnoses,
        )
        for i, dx in enumerate(secondary_diagnoses[: self.max_secondary_diagnoses]):
            self.secondary_diagnoses[i] = dx

    def __str__(self) -> str:
        return "".join(map(str, self.secondary_diagnoses))

    @classmethod
    def extract_from_output(cls, output) -> list[Diagnosis]:
        diagnoses = []
        position = cls.position
        for i in range(cls.max_secondary_diagnoses):
            next_position = position + Diagnosis.field_length
            diagnoses.append(
                Diagnosis.extract_from_output(output[position:next_position])
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
    name = "principal_procedure"

    def __init__(self, principal_procedure: Optional[ProcedureCode] = None) -> None:
        self.principal_procedure = (
            principal_procedure if principal_procedure else ProcedureCode()
        )

    def __str__(self) -> str:
        return str(self.principal_procedure)

    @classmethod
    def extract_from_output(cls, output):
        return ProcedureCode(output[cls.position : cls.position + cls.field_length])


class SecondaryProcedures(Field):
    """
    Procedure codes
    Seven left-justified characters, blank-filled.
    Up to 24 procedure codes without decimal.
    """

    max_secondary_procedures = 24
    position = 318
    field_length = max_secondary_procedures * ProcedureCode.field_length
    name = "secondary_procedures"

    def __init__(
        self, secondary_procedures: Optional[Sequence[ProcedureCode]] = None
    ) -> None:
        self.secondary_procedures = deque(
            [ProcedureCode()] * self.max_secondary_procedures,
            maxlen=self.max_secondary_procedures,
        )
        if secondary_procedures:
            for i, procedure in enumerate(
                secondary_procedures[: self.max_secondary_procedures]
            ):
                self.secondary_procedures[i] = procedure

    def __str__(self) -> str:
        return "".join(map(str, self.secondary_procedures))

    @classmethod
    def extract_from_output(cls, output):
        procedures = []
        position = cls.position
        for i in range(cls.max_secondary_procedures):
            next_position = position + ProcedureCode.field_length
            code_str = output[position:next_position].strip()
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
    max_procedure_dates = 25
    field_length = max_procedure_dates * Date.field_length
    name = "procedure_date"

    def __init__(self, procedure_dates: Optional[Sequence[Date]] = None) -> None:

        self.procedure_dates = deque(
            [Date()] * self.max_procedure_dates,
            maxlen=self.max_procedure_dates,
        )
        if procedure_dates:
            for i, date in enumerate(procedure_dates[: self.max_procedure_dates]):
                self.procedure_dates[i] = date

    def __str__(self) -> str:
        return "".join(map(str, self.procedure_dates))

    @classmethod
    def extract_from_output(cls, output):
        procedure_dates = []
        position = cls.position
        for i in range(cls.max_procedure_dates):
            next_position = position + Date.field_length
            date_str = output[position:next_position].strip()
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
    name = "apply_hac_logic"

    def __init__(self, apply_hac_logic_value: ApplyHACLogicValue) -> None:
        self.apply_hac_logic_value = apply_hac_logic_value

    def __str__(self):
        return str(self.apply_hac_logic_value.value)

    @classmethod
    def extract_from_output(cls, output) -> ApplyHACLogicValue:
        hac_logic = output[cls.position : cls.position + cls.field_length]
        return ApplyHACLogicValue(hac_logic)


class UNUSED(Field):
    """
    UNUSED

    This field is noted to be unused in the CMS Grouper UserGuide
    """

    position = 737
    field_length = 1
    name = "unused"

    def __init__(self):
        self.field_value = ""

    def __str__(self):
        return self.field_value.ljust(self.field_length)

    @classmethod
    def extract_from_output(cls, output):
        raise NotImplementedError


class OptionalInformation(Field):
    """
    Optional field
    Left justified, blank-filled.
    All blanks if no value is entered.
    """

    position = 738
    field_length = 72
    name = "optional_information"

    def __init__(self, optional_information: str = "") -> None:
        self.optional_information = optional_information

    def __str__(self):
        return self.optional_information[: self.field_length].ljust(self.field_length)

    @classmethod
    def extract_from_output(cls, output):
        return output[cls.position : cls.position + cls.field_length].strip()


class Filler(Field):
    """
    Filler
    Not used
    Blank-filled
    """

    position = 810
    field_length = 25
    name = "filler"

    def __init__(self):
        self.filler = ""

    def __str__(self):
        return self.filler.ljust(self.field_length)

    @classmethod
    def extract_from_output(cls, output):
        raise NotImplementedError


class MSGMCEVersionUsed(Field):
    """
    Version of the software used to process the claim.
    Right-justified, blank-filled.
    Stored without decimal point.
    """

    position = 835
    field_length = 3
    name = "msg_mce_version_used"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output):
        return output[cls.position : cls.position + cls.field_length]


class InitialDRG(Field):
    """
    Initial diagnosis related group
    Right-justified, zero filled.
    """

    position = 838
    field_length = 3
    name = "initial_drg"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output):
        return int(output[cls.position : cls.position + cls.field_length])


class InitialMSIndicator(Field):
    """
    Initial medical/surgical indicator
    """

    position = 841
    field_length = 1
    name = "initial_medical_surgical_indicator"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output) -> MedicalSurgicalIndicatorValue:
        ms_indicator = int(output[cls.position : cls.position + cls.field_length])
        return MedicalSurgicalIndicatorValue(ms_indicator)


class FinalMDC(Field):
    """
    Major diagnostic category.
    Right-justified, zero-filled.
    """

    position = 841
    field_length = 3
    name = "final_mdc"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output) -> int:
        return int(output[cls.position : cls.position + cls.field_length])


class FinalDRG(Field):
    """
    Final diagnosis related group.
    Right-justified, zero-filled.
    """

    position = 844
    field_length = 3
    name = "final_drg"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output) -> int:
        return int(output[cls.position : cls.position + cls.field_length])


class FinalMSIndicator(Field):
    """
    Final Medical/Surgical Indicator
    """

    position = 847
    field_length = 1
    name = "final_medical_surgical_indicator"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output) -> MedicalSurgicalIndicatorValue:
        ms_indicator = int(output[cls.position : cls.position + cls.field_length])
        return MedicalSurgicalIndicatorValue(ms_indicator)


class DRGReturnCode(Field):
    """
    DRG Return Code
    Numeric.
    Right-justified, zero-filled.
    """

    position = 848
    field_length = 2
    name = "drg_return_code"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output) -> DRGReturnCodeValue:
        return_code = int(output[cls.position : cls.position + cls.field_length])
        return DRGReturnCodeValue(return_code)


class MSGMCEEditReturnCode(Field):
    """
    MSG/MCE edit return code
    Four-character return code, right-justified, zero-filled.
    """

    position = 850
    field_length = 4
    name = "msg_mce_edit_return_code"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output) -> MSGMCEEditReturnCodeValue:
        return_code = int(output[cls.position : cls.position + cls.field_length])
        return MSGMCEEditReturnCodeValue(return_code)


class DiagnosisCodeCount(Field):
    """
    Diagnosis code count
    Number of diagnosis codes processed.
    Right-justified, zero-filled.
    This field does not include the admit diagnosis.
    """

    position = 854
    field_length = 2
    name = "diagnosis_code_count"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output) -> int:
        return int(output[cls.position : cls.position + cls.field_length])


class ProcedureCodeCount(Field):
    """
    Procedure code count
    Number of procedure codes processed.
    Right-justified, zero-filled.
    """

    position = 856
    field_length = 2
    name = "procedure_code_count"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output) -> int:
        return int(output[cls.position : cls.position + cls.field_length])


class PrincipalDiagnosisEditReturnFlag(Field):
    """
    Principal diagnosis edit return flag
    Two-byte flag.
    Right-justified, zero-filled.
    A maximum of four flags can be returned for each diagnosis code.
    """

    position = 858
    field_length = 8
    name = "principal_diagnosis_edit_return_flag"
    return_flag_length = 2
    max_return_flags = 4

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output):
        return_flags = []
        position = cls.position
        for i in range(cls.max_return_flags):
            next_position = position + cls.return_flag_length
            val = int(output[position:next_position])
            return_flags.append(PrincipalDiagnosisEditReturnFlagValue(val))
            position = next_position
        return return_flags


class PrincipalDiagnosisHospitalAcquiredConditionCriteria(Field):
    """
    Principal diagnosis hospital acquired condition criteria
    """

    position = 866
    n_criteria_fields = 5
    criteria_field_length = 2
    field_length = n_criteria_fields * criteria_field_length
    name = "principal_diagnosis_hospital_acquired_condition_assignment_criteria"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output):
        return_flags = []
        position = cls.position
        for i in range(cls.n_criteria_fields):
            next_position = position + cls.criteria_field_length
            val = output[position:next_position]
            return_flags.append(
                PrincipalDiagnosisHospitalAcquiredConditionAssignmentCriteriaValue(val)
            )
            position = next_position
        return return_flags


class PrincipalDiagnosisHospitalAcquiredConditionUsage(Field):
    """
    Principal diagnosis hospital acquired condition usage
    """

    position = 876
    usage_value_field_length = 1
    n_usage_fields = 5
    field_length = n_usage_fields * usage_value_field_length
    name = "principal_diagnosis_hospital_acquired_condition_usage"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output):
        hac_usage = []
        position = cls.position
        for i in range(cls.n_usage_fields):
            next_position = position + cls.usage_value_field_length
            val = output[position:next_position]
            hac_usage.append(DiagnosisHospitalAcquiredConditionUsageValue(val))
            position = next_position
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
    n_return_flag_fields = 24
    field_length = return_flag_field_length * n_return_flag_fields

    name = "secondary_diagnosis_return_flag"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output) -> list[SecondaryDiagnosisEditReturnFlagValue]:
        # TODO:  The return value is a list of 8-char str instead of up to 4 flag values
        flags = []
        position = cls.position
        for i in range(cls.n_return_flag_fields):
            next_position = position + cls.return_flag_field_length
            flags.append(output[position:next_position])
            position = next_position
        return flags


class SecondaryDiagnosisHospitalAcquiredConditionAssignmentCriteria(Field):
    """
    Hospital Acquired Condition (HAC) assigned
    #1-5. These 2-byte flags are a combination
    of information concerning every diagnosis
    from the DRG assignment and the editor.
    """

    position = 1073
    hac_field_length = 10
    n_hac_criteria_fields = 24
    field_length = hac_field_length * n_hac_criteria_fields
    name = "secondary_diagnosis_hospital_acquired_condition_assignment_criteria"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output):
        # TODO:  Figure out how these are parsed at a criteria flag level and fix return value
        hac_criteria = []
        position = cls.position
        for i in range(cls.n_hac_criteria_fields):
            next_position = position + cls.hac_field_length
            hac_criteria.append(output[position:next_position])
            position = next_position
        return hac_criteria


class SecondaryDiagnosisHospitalAcquiredConditionUsage(Field):
    """
    Hospital Acquired Condition (HAC) usage
    #1-5. This 1-byte flag is a combination of
    information concerning every diagnosis from
    the DRG assignment and the editor.
    """

    position = 1313
    usage_field_length = 5
    occurrences = 24
    name = "secondary_diagnosis_hospital_acquired_condition_usage"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output):
        # TODO:  Figure out how these are parsed at a usage flag level and fix return value
        hac_usage = []
        position = cls.position
        for i in range(cls.occurrences):
            next_position = position + cls.usage_field_length
            hac_usage.append(output[position:next_position])
            position = next_position
        return hac_usage


class ProcedureEditReturnFlag(Field):
    """ """

    position = 1433
    return_flag_field_length = 8
    occurrences = 25
    field_length = occurrences * return_flag_field_length
    name = "procedure_edit_return_flag"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output):
        # TODO:  Figure out how these are parsed at a usage flag level and fix return value
        return_flags = []
        position = cls.position
        for i in range(cls.occurrences):
            next_position = position + cls.return_flag_field_length
            return_flags.append(output[position:next_position])
            position = next_position
        return return_flags


class ProcedureHospitalAcquiredConditionAssignmentCriteria(Field):
    """ """

    position = 1633
    occurrences = 25
    criteria_field_length = 10
    field_length = occurrences * criteria_field_length
    name = "procedure_hospital_acquired_condition_assignment_criteria"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output):
        # TODO:  Figure out how these are parsed at a usage flag level and fix return value
        criteria = []
        position = cls.position
        for i in range(cls.occurrences):
            next_position = position + cls.criteria_field_length
            criteria.append(output[position:next_position])
            position = next_position
        return criteria


class InitialFourDigitDRG(Field):
    """Initial 4-digit DRG. Right-justified, zero-filled."""

    position = 1883
    field_length = 4
    name = "initial_four_digit_drg"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output):
        return output[cls.position : cls.position + cls.field_length]


class FinalFourDigitDRG(Field):
    """Final 4-digit DRG.  Right-justified, zero-filled."""

    position = 1887
    field_length = 4
    name = "final_four_digit_drg"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output):
        return output[cls.position : cls.position + cls.field_length]


class FinalDRGCCMCCUsage(Field):
    """Final DRG CC/MCC Usage"""

    position = 1891
    field_length = 1
    name = "final_drg_cc_mcc_usage"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output):
        return DRGCCMCCUsageValue(
            int(output[cls.position : cls.position + cls.field_length])
        )


class InitialDRGCCMCCUsage(Field):
    """Initial DRG CC/MCC Usage"""

    position = 1892
    field_length = 1
    name = "initial_drg_cc_mcc_usage"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output):
        return DRGCCMCCUsageValue(
            int(output[cls.position : cls.position + cls.field_length])
        )


class NumberOfUniqueHospitalAcquiredConditionsMet(Field):
    """The Number of unique hospital acquired conditions that have been met."""

    position = 1893
    field_length = 2
    name = "number_of_unique_hospital_acquired_conditions_met"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output) -> int:
        return int(output[cls.position : cls.position + cls.field_length])


class HospitalAcquiredConditionStatus(Field):
    """ """

    position = 1895
    field_length = 1
    name = "hospital_acquired_condition_status"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output):
        return HACStatusValue(int(output[cls.position : cls.position + cls.field_length]))


class CostWeight(Field):
    """
    The DRG cost weight
    This 7-byte field is displayed as 2 digits followed by a decimal point
    followed by 4 digits.
    """

    position = 1896
    field_length = 7
    name = "cost_weight"

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def extract_from_output(cls, output) -> float:
        return float(output[cls.position : cls.position + cls.field_length])
