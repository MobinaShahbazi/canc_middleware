from sqlalchemy.orm import Session
from app import crud, schemas
from fastapi import Depends
from app.dependencies import get_db


def init_db(db: Session) -> None:

    dmn_model_files = [{
        'code': 'bmi_level',
        'title': 'BMI Risk Check',
        'description': 'Checks Disease Risk Based on BMI',
        'path': './BMILevel.dmn'
    },
        {
            'code': 'dinner_decisions',
            'title': 'Dinner Decisions',
            'description': 'Decide what to have for dinner.',
            'path': './dinner_decisions.dmn'
        }
    ]

    for dmn_model_file in dmn_model_files:
        dmn_in = schemas.dmn_models.DMNModelCreate(**dmn_model_file)
        crud.dmn_crud.create(db=db, obj_in=dmn_in)