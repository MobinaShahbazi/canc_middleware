from typing import Dict, Any, Optional, Type
from pydantic import BaseModel


class Form(BaseModel):

    clinical_assessment: bool
    biopsy_hist: int
    chest_radiotherapy_hist: bool
    personal_breast_cancer_hist: bool
    personal_ovarian_cancer_hist: bool
    personal_pancreatic_cancer_hist: bool
    family_hist: bool
    risk: str
    age_of_diagnose: int
    biopsy_date: int
    birth_date: int
    radiotherapy_date: int

class FormCreate(Form):
    pass

class FormUpdate(Form):
    pass

