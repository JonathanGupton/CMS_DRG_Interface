from src.field import *


def test_patient_name():

    p = PatientName("")
    assert len(str(p)) == 31

    p = PatientName("Jonathan")
    assert len(str(p)) == 31
    assert (str(p)[0] == "J") and (str(p)[-1] == " ")

    p = PatientName("john jacob jingleheimer schmidt His name is my name too")
    assert len(str(p)) == 31