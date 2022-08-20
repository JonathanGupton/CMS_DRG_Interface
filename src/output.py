from __future__ import annotations

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
)


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

    @classmethod
    def from_line(cls, line):
        record = cls(line)
        for field in cls.fields:
            setattr(record, field.name, field.extract_from_output(line))
        return record
