
from pathlib import Path
from time import sleep

from src.adapter import (
    MSDRGGrouperSoftwareInterface,
    MSDRGGrouperSoftwareOptions,
    MSDRGGrouperSoftwareParameters,
)
from src.batch import Batch
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
)
from src.field_literal import (
    PayerValue as Payer,
    PresentOnAdmissionValue as POAValue,
    ApplyHACLogicValue as HACLogic,
    SexValue,
    DischargeDispositionValue as Disposition,
)
from src.record import InputRecord
from src.value_container import (
    Date,
    Diagnosis,
    DiagnosisCode,
    ProcedureCode,
)
from src.output import OutputRecord

#
# # Create the patient record fields
# patient_name = PatientName("Jonathan")
# medical_record_number = MedicalRecordNumber("1234567")
# account_number = AccountNumber("0987654321")
# admit_date = AdmitDate(Date.from_string("08/01/2022"))
# discharge_date = DischargeDate(Date.from_string("08/09/2022"))
# discharge_status = DischargeStatus(Disposition.HOME_OR_SELF_CARE)
# primary_payer = PrimaryPayer(Payer.INSURANCE_COMPANY)
# los = LOS(8)
# birth_date = BirthDate(Date.from_string("01/01/1980"))
# age = Age(42)
# sex = Sex(SexValue.MALE)
# admit_diagnosis = AdmitDiagnosis(DiagnosisCode("J189"))
# principal_diagnosis = PrincipalDiagnosis(
#     Diagnosis(DiagnosisCode("J189"), POAValue.YES)
# )
# secondary_diagnoses = SecondaryDiagnoses(
#     [Diagnosis(DiagnosisCode("E43"), POAValue.YES)]
# )
# principal_procedure = PrincipalProcedure(ProcedureCode("5A1955Z"))
# secondary_procedures = SecondaryProcedures()
# procedure_date = ProcedureDates([Date.from_string("08/01/2022")])
# apply_hac_logic = ApplyHACLogic(HACLogic.REQUIRES_POA_REPORTING)
#
# # Create your record object
# record = InputRecord(
#     patient_name=patient_name,
#     medical_record_number=medical_record_number,
#     account_number=account_number,
#     admit_date=admit_date,
#     discharge_date=discharge_date,
#     discharge_status=discharge_status,
#     primary_payer=primary_payer,
#     los=los,
#     birth_date=birth_date,
#     age=age,
#     sex=sex,
#     admit_diagnosis=admit_diagnosis,
#     principal_diagnosis=principal_diagnosis,
#     principal_procedure=principal_procedure,
#     secondary_diagnoses=secondary_diagnoses,
#     secondary_procedures=secondary_procedures,
#     procedure_date=procedure_date,
#     apply_hac_logic=apply_hac_logic,
# )
#
# # Combine your records into a batch
# batch = Batch([record])
#
# # Save your batch to a txt file
# input_filepath = Path().cwd() / "input.txt"
# with open(input_filepath, "w") as f:
#     f.write(str(batch))

# Create the output destination path
output_filepath = Path().cwd() / "output.txt"
#
# # Pass the created batch file and destination path to a param object
# params = MSDRGGrouperSoftwareParameters(
#     batchfile=input_filepath,
#     output_type=MSDRGGrouperSoftwareOptions.SingleLineOutput,
#     output_destination=output_filepath
# )
#
# # Create your grouper object
# grouper_filepath = Path(r"C:\Program Files\MSG MCE Software I10")
# grouper = MSDRGGrouperSoftwareInterface(grouper_directory=grouper_filepath)
#
# # Pass the grouper params to grouper.group() method
# grouper.group(params=params)
#
# sleep(3)

# Read in the output
output = []
with open(output_filepath, "r") as f:
    lines = f.read()
rec = OutputRecord.from_line(lines)
