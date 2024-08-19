from typing import Dict, Any, Optional, Type
from pydantic import BaseModel


class PatientConsent(BaseModel):

    patient_consent: bool


class PatientConsentCreate(PatientConsent):
    pass

class PatientConsentUpdate(PatientConsent):
    pass

