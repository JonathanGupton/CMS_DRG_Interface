from interface import MSDRGGrouperSoftwareParameter
from batch import Batch
from field import (
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
    Date,
    DiagnosisCode,
    Diagnosis,
    ProcedureCode,
)
from value import (
    PayerValue as Payer,
    PresentOnAdmissionValue as POAValue,
    ApplyHACLogicValue as HACLogic,
    SexValue,
    DischargeDispositionValue as Disposition,
)
from grouper import Grouper
from record import InputRecord

# Create your record object from the patient record fields
record = InputRecord(
    patient_name=PatientName("Jonathan"),
    medical_record_number=MedicalRecordNumber("1234567"),
    account_number=AccountNumber("0987654321"),
    admit_date=AdmitDate(Date.from_string("08/01/2022")),
    discharge_date=DischargeDate(Date.from_string("08/09/2022")),
    discharge_status=DischargeStatus(Disposition.HOME_OR_SELF_CARE),
    primary_payer=PrimaryPayer(Payer.INSURANCE_COMPANY),
    los=LOS(8),
    birth_date=BirthDate(Date.from_string("01/01/1980")),
    age=Age(42),
    sex=Sex(SexValue.MALE),
    admit_diagnosis=AdmitDiagnosis(DiagnosisCode("J189")),
    principal_diagnosis=PrincipalDiagnosis(
        Diagnosis(DiagnosisCode("J189"), POAValue.YES)
    ),
    secondary_diagnoses=SecondaryDiagnoses(
        [
            Diagnosis(DiagnosisCode("E43"), POAValue.YES),
            Diagnosis(DiagnosisCode("K3521"), POAValue.NO),
            Diagnosis(DiagnosisCode("L89894"), POAValue.NO),
        ]
    ),
    principal_procedure=PrincipalProcedure(ProcedureCode("5A1955Z")),
    secondary_procedures=SecondaryProcedures([ProcedureCode("0KBP3ZZ")]),
    procedure_date=ProcedureDates(
        [
            Date.from_string("08/01/2022"),
            Date.from_string("08/07/2022"),
        ]
    ),
    apply_hac_logic=ApplyHACLogic(HACLogic.EXEMPT_FROM_POA_REPORTING),
)

# Combine your records into a batch
batch = Batch([record])

# Pass the created batch file and destination path to a param object
params = MSDRGGrouperSoftwareParameter(batch=batch)

# Create your grouper object
grouper = Grouper()

# Pass the grouper params to grouper.group() method
output = grouper.group(params=params)

output = output[0]
