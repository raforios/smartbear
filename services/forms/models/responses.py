# models/responses.py
'''
   Responses Models - Defines the database models for form submissions,
   including respondent (person) and contact details, and individual answers.
'''
from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Enum as SQLAlchemyEnum

from services.db_connection import Base
from schemas.responses import FormResponseStatus # Import the enum from schemas/responses.py

# --- Person Model (Encuestado/Entrevistado) ---
class Person(Base): # pylint: disable=too-few-public-methods, too-many-ancestors
    '''
        SQLAlchemy model for the 't_persons' table.
        Represents an individual (e.g., interviewee, surveyed person).
    '''
    __tablename__ = 't_persons'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(255), nullable = False)
    email = Column(String(255), nullable = True, unique = True, index = True)
    phone_number = Column(String(50), nullable = True, unique = True, index = True)
    identification_number = Column(String(50), nullable = True, unique = True, index = True)

    # Relationships: one-to-many with Contact
    contacts = relationship(
        'Contact',
        back_populates = 'person',
        cascade = 'all, delete-orphan' # Deletes associated contacts if a person is deleted
    )

# --- Contact Model (Georeferenced Location & Time of Interaction) ---
class Contact(Base): # pylint: disable=too-few-public-methods, too-many-ancestors
    '''
        SQLAlchemy model for the 't_contacts' table.
        Stores georeferenced location and time details for an interaction.
    '''
    __tablename__ = 't_contacts'

    id = Column(Integer, primary_key = True, index = True)
    person_id = Column(Integer, ForeignKey('t_persons.id'), nullable = False)
    latitude = Column(Float, nullable = False)
    longitude = Column(Float, nullable = False)
    start_datetime = Column(DateTime, nullable = False)

    # Relationships: many-to-one with Person, one-to-many with FormResponse
    person = relationship('Person', back_populates = 'contacts')
    t_form_responses = relationship(
        'FormResponse',
        back_populates = 'contact',
        cascade = 'all, delete-orphan' # Deletes associated form responses if a contact is deleted
    )


# --- FormResponse Model (Completed Form Submission) ---
class FormResponse(Base): # pylint: disable=too-few-public-methods, too-many-ancestors
    '''
        SQLAlchemy model for the 't_form_responses' table.
        Represents a completed submission of a form.
    '''
    __tablename__ = 't_form_responses'

    id = Column(Integer, primary_key = True, index = True)
    form_id = Column(Integer, ForeignKey('t_form_headers.id'), nullable = False)
    contact_id = Column(Integer, ForeignKey('t_contacts.id'), nullable = False)
    submission_date = Column(DateTime, server_default = func.now(), nullable = False)# pylint: disable=not-callable
    status = Column(SQLAlchemyEnum(
        *[status_member.value for status_member in FormResponseStatus.__members__.values()]),
        nullable = False, default = FormResponseStatus.COMPLETED)
    # The user who submitted this specific form response (from frontend)
    user = Column(String(255), nullable = False)

    # Relationships:
    # many-to-one with FormHeader (implicitly linked by form_id, no back_populates needed
    # here if FormHeader doesn't need to see responses)
    # For now, FormHeader does not need a back_populates from here.
    # If FormHeader needs to query its responses, we'd add:
    # `t_form_responses = relationship('FormResponse', back_populates='form_header',
    # cascade='all, delete-orphan')`
    # to FormHeader model, and `form_header = relationship('FormHeader')` here.
    # However, to maintain separation, we'll keep the link one-way for now
    # (FormResponse -> FormHeader).
    # Update: As per previous definition, FormHeader *did* have `t_form_responses` relation.
    # We should re-add it to FormHeader's model and define the back_populates here.

    # Re-adding relationships as they were in forms.py but pointing to the new models/responses.py
    # FormHeader (from models/forms.py) will reference 'FormResponse' (this model)
    # The 'form_header' relationship on this side is a simple reference back.
    # This maintains the link for querying from FormResponse to FormHeader.
    # The 'back_populates' on the FormHeader side will be important.
    form_header = relationship('FormHeader', primaryjoin="FormResponse.form_id == FormHeader.id")

    # Link to the new Contact model
    contact = relationship('Contact', back_populates = 't_form_responses')

    answers = relationship(
        'FormAnswer',
        back_populates = 'form_response',
        cascade = 'all, delete-orphan' # Deletes individual answers if form response is deleted
    )

# --- FormAnswer Model (Individual Answer within a Submission) ---
class FormAnswer(Base): # pylint: disable=too-few-public-methods, too-many-ancestors
    '''
        SQLAlchemy model for the 't_form_answers' table.
        Stores individual answers for questions within a completed form response.
    '''
    __tablename__ = 't_form_answers'

    id = Column(Integer, primary_key = True, index = True)
    form_response_id = Column(Integer, ForeignKey('t_form_responses.id'), nullable = False)
    question_id = Column(Integer, ForeignKey('t_question_details.id'), nullable = False)
    # The actual answer value (text, number, 'Si'/'No', S3 URL)
    answer_value = Column(Text, nullable = True)

    # Relationships:
    # many-to-one with FormResponse and QuestionDetail
    form_response = relationship('FormResponse', back_populates = 'answers')
    # QuestionDetail (from models/forms.py) will reference 'FormAnswer' (this model)
    # The 'question_detail' relationship on this side is a simple reference back.
    # The 'back_populates' on the QuestionDetail side will be important.
    question_detail = relationship('QuestionDetail',
                    primaryjoin = "FormAnswer.question_id == QuestionDetail.id")

    # Constraint to ensure unique answer per form_response_id and question_id
    __table_args__ = (
        UniqueConstraint('form_response_id', 'question_id', name = '_response_Youtube_uc'),
    )
