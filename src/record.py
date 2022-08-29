from __future__ import annotations

from pathlib import Path
from typing import Iterator, Sequence

from src.batch_field import (
    PatientName,
    MedicalRecordNumber,
    AccountNumber,
    AdmitDate,
    DischargeDate,
    DischargeStatus,
    PrimaryPayer,
    LOS,
    BirthDate,
    Age,
    Sex,
    AdmitDiagnosis,
    PrincipalDiagnosis,
    SecondaryDiagnoses,
    PrincipalProcedure,
    SecondaryProcedures,
    ProcedureDates,
    ApplyHACLogic,
    UNUSED,
    OptionalInformation,
    Filler,
    MSGMCEVersionUsed,
    InitialDRG,
    InitialMSIndicator,
    FinalMDC,
    FinalDRG,
    FinalMSIndicator,
    DRGReturnCode,
    MSGMCEEditReturnCode,
    DiagnosisCodeCount,
    ProcedureCodeCount,
    PrincipalDiagnosisEditReturnFlag,
    PrincipalDiagnosisHospitalAcquiredConditionCriteria,
    PrincipalDiagnosisHospitalAcquiredConditionUsage,
    SecondaryDiagnosisReturnFlag,
    SecondaryDiagnosisHospitalAcquiredConditionAssignmentCriteria,
    SecondaryDiagnosisHospitalAcquiredConditionUsage,
    ProcedureEditReturnFlag,
    ProcedureHospitalAcquiredConditionAssignmentCriteria,
    InitialFourDigitDRG,
    FinalFourDigitDRG,
    FinalDRGCCMCCUsage,
    InitialDRGCCMCCUsage,
    NumberOfUniqueHospitalAcquiredConditionsMet,
    HospitalAcquiredConditionStatus,
    CostWeight,
)
from src.field import Field


class InputRecord:
    """Object representing individual records to be grouped"""

    __slots__ = [
        "patient_name",
        "medical_record_number",
        "account_number",
        "admit_date",
        "discharge_date",
        "discharge_status",
        "primary_payer",
        "los",
        "birth_date",
        "age",
        "sex",
        "admit_diagnosis",
        "principal_diagnosis",
        "secondary_diagnoses",
        "principal_procedure",
        "secondary_procedures",
        "procedure_date",
        "apply_hac_logic",
        "unused",
        "optional_information",
        "filler",
    ]

    def __init__(
        self,
        patient_name: PatientName,
        medical_record_number: MedicalRecordNumber,
        account_number: AccountNumber,
        admit_date: AdmitDate,
        discharge_date: DischargeDate,
        discharge_status: DischargeStatus,
        primary_payer: PrimaryPayer,
        los: LOS,
        birth_date: BirthDate,
        age: Age,
        sex: Sex,
        admit_diagnosis: AdmitDiagnosis,
        principal_diagnosis: PrincipalDiagnosis,
        secondary_diagnoses: SecondaryDiagnoses,
        principal_procedure: PrincipalProcedure,
        secondary_procedures: SecondaryProcedures,
        procedure_date: ProcedureDates,
        apply_hac_logic: ApplyHACLogic,
        optional_information: OptionalInformation = None,
    ) -> None:
        self.patient_name: PatientName = patient_name
        self.medical_record_number: MedicalRecordNumber = medical_record_number
        self.account_number: AccountNumber = account_number
        self.admit_date: AdmitDate = admit_date
        self.discharge_date: DischargeDate = discharge_date
        self.discharge_status: DischargeStatus = discharge_status
        self.primary_payer: PrimaryPayer = primary_payer
        self.los: LOS = los
        self.birth_date: BirthDate = birth_date
        self.age: Age = age
        self.sex: Sex = sex
        self.admit_diagnosis: AdmitDiagnosis = admit_diagnosis
        self.principal_diagnosis: PrincipalDiagnosis = principal_diagnosis
        self.secondary_diagnoses: SecondaryDiagnoses = secondary_diagnoses
        self.principal_procedure: PrincipalProcedure = principal_procedure
        self.secondary_procedures: SecondaryProcedures = secondary_procedures
        self.procedure_date: ProcedureDates = procedure_date
        self.apply_hac_logic: ApplyHACLogic = apply_hac_logic
        self.unused = UNUSED()
        self.optional_information = (
            optional_information if optional_information else OptionalInformation()
        )
        self.filler = Filler()

    def __str__(self) -> str:
        return "".join(map(str, self))

    def __len__(self) -> int:
        return len(str(self))

    def __iter__(self) -> Iterator[Field]:
        yield self.patient_name
        yield self.medical_record_number
        yield self.account_number
        yield self.admit_date
        yield self.discharge_date
        yield self.discharge_status
        yield self.primary_payer
        yield self.los
        yield self.birth_date
        yield self.age
        yield self.sex
        yield self.admit_diagnosis
        yield self.principal_diagnosis
        yield self.secondary_diagnoses
        yield self.principal_procedure
        yield self.secondary_procedures
        yield self.procedure_date
        yield self.apply_hac_logic
        yield self.unused
        yield self.optional_information
        yield self.filler


class OutputRecord:
    """Class for storing and parsing output record strings"""

    fields = [
        PatientName,
        MedicalRecordNumber,
        AccountNumber,
        AdmitDate,
        DischargeDate,
        DischargeStatus,
        PrimaryPayer,
        LOS,
        BirthDate,
        Age,
        Sex,
        AdmitDiagnosis,
        PrincipalDiagnosis,
        SecondaryDiagnoses,
        PrincipalProcedure,
        SecondaryProcedures,
        ProcedureDates,
        ApplyHACLogic,
        OptionalInformation,
        MSGMCEVersionUsed,
        InitialDRG,
        InitialMSIndicator,
        FinalMDC,
        FinalDRG,
        FinalMSIndicator,
        DRGReturnCode,
        MSGMCEEditReturnCode,
        DiagnosisCodeCount,
        ProcedureCodeCount,
        PrincipalDiagnosisEditReturnFlag,
        PrincipalDiagnosisHospitalAcquiredConditionCriteria,
        PrincipalDiagnosisHospitalAcquiredConditionUsage,
        SecondaryDiagnosisReturnFlag,
        SecondaryDiagnosisHospitalAcquiredConditionAssignmentCriteria,
        SecondaryDiagnosisHospitalAcquiredConditionUsage,
        ProcedureEditReturnFlag,
        ProcedureHospitalAcquiredConditionAssignmentCriteria,
        InitialFourDigitDRG,
        FinalFourDigitDRG,
        FinalDRGCCMCCUsage,
        InitialDRGCCMCCUsage,
        NumberOfUniqueHospitalAcquiredConditionsMet,
        HospitalAcquiredConditionStatus,
        CostWeight,
    ]

    def __init__(self, record: str) -> None:
        self.record = record

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.account_number)})"

    @classmethod
    def from_line(cls, line):
        """Parse an output record from a grouper batchfile output line"""
        record = cls(line)
        for field in cls.fields:
            setattr(record, field.name, field.new_from_output_string(line))
        return record


def load_output_from_file(filepath: Path) -> Sequence[OutputRecord]:
    """Read in the grouped records from the CMS MCE Grouper output file"""
    with open(filepath, "r") as f:
        output_records = [OutputRecord.from_line(line) for line in f.readlines()]
    return output_records
