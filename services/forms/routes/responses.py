'''
    Responses: routes handler
'''
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# Import schemas for form responses
from schemas.responses import (
    StartFormSessionRequest,
    StartFormSessionResponse,
    SubmitAnswerRequest,
    NextQuestionResponse,
    GetQuestionToModifyRequest,
    GetQuestionToModifyResponse,
    UpdateAnswerInSessionRequest,
    FinalizeFormRequest,
    FinalizeFormResponse,
    FormResponseDetailResponse,
    FormResponseSummaryResponse,
    FormResponseUpdate
)

# Import controllers for form responses
from controllers.responses import (
    start_form_session,
    submit_answer_and_get_next_question,
    get_question_to_modify,
    update_answer_in_session,
    finalize_form_session,
    get_form_response_by_id,
    get_all_form_responses,
    update_form_response_status
)

from services.db_connection import GET_DB_DEPENDENCY
from services.logger_config import custom_logger as logger
from services.security import get_current_user # To get current_user_id from JWT

router = APIRouter(prefix = '/v1/form-responses', tags = ['Form Responses'])

# --- Endpoints for Form Session Management (DynamoDB backed) ---

@router.post(
    '/start-session',
    response_model = StartFormSessionResponse,
    status_code = status.HTTP_201_CREATED,
    summary = 'Starts a new form-filling session and returns the first question'
)
async def start_form_session_route(
    session_data: StartFormSessionRequest,
    db: Session = Depends(GET_DB_DEPENDENCY),
    current_user: str = Depends(get_current_user)
):
    '''
        Initiates a new form-filling session for a given form,
        creates initial Person and Contact records, and returns the first question.
        The session state is stored temporarily in DynamoDB.

        Args:
            session_data (StartFormSessionRequest): Contains form_id, person, and
                                                    contact info.
            db (Session): The database session.
            current_user (str): The ID of the authenticated user.

        Returns:
            StartFormSessionResponse: Details of the started session and the first
                                    question.
    '''
    message = f'''User {current_user} request to start form session for form_id:
            {session_data.form_id}'''
    logger.info(message)
    return await start_form_session(db, session_data, current_user)

@router.post(
    '/submit-answer',
    response_model = NextQuestionResponse,
    summary = 'Submits an answer and gets the next question in the session'
)
async def submit_answer_route(
    answer_data: SubmitAnswerRequest,
    db: Session = Depends(GET_DB_DEPENDENCY),
    current_user: str = Depends(get_current_user)
):
    '''
        Submits an answer for the current question in a form session,
        updates the temporary session cache in DynamoDB, and determines
        and returns the next question based on form flow rules.

        Args:
            answer_data (SubmitAnswerRequest): Contains session_id, question_number,
                                            and answer_value.
            db (Session): The database session.
            current_user (str): The ID of the authenticated user.

        Returns:
            NextQuestionResponse: Details of the next question or indicates form
                                completion.
    '''
    message = f'''User {current_user} request to submit answer for session
            {answer_data.session_id}, question {answer_data.question_number}'''
    logger.info(message)
    return await submit_answer_and_get_next_question(db, answer_data, current_user)

@router.post(
    '/get-question-to-modify',
    response_model = GetQuestionToModifyResponse,
    summary = '''Retrieves a specific question and its current answer from a session for
            modification'''
)
async def get_question_to_modify_route(
    request_data: GetQuestionToModifyRequest,
    db: Session = Depends(GET_DB_DEPENDENCY),
    current_user: str = Depends(get_current_user)
):
    '''
        Allows the user to retrieve a previously answered question and its value
        from a temporary form session. This is useful for 'back' functionality or review.

        Args:
            request_data (GetQuestionToModifyRequest): Contains session_id and
                                                    question_number.
            db (Session): The database session.
            current_user (str): The ID of the authenticated user.

        Returns:
            GetQuestionToModifyResponse: Details of the requested question and its
                                        current answer.
    '''
    message = f'''User {current_user} request to get question
            {request_data.question_number} to modify in session
            {request_data.session_id}'''
    logger.info(message)
    return await get_question_to_modify(db, request_data, current_user)

@router.put(
    '/update-answer-in-session',
    response_model = NextQuestionResponse, # Same response as submit, as it re-evaluates flow
    summary = 'Updates an answer for a specific question within a form session'
)
async def update_answer_in_session_route(
    update_data: UpdateAnswerInSessionRequest,
    db: Session = Depends(GET_DB_DEPENDENCY),
    current_user: str = Depends(get_current_user)
):
    '''
        Updates the answer for a specific question in an ongoing form session.
        After update, the form flow is re-evaluated from the updated question's point.

        Args:
            update_data (UpdateAnswerInSessionRequest): Contains session_id,
                                                        question_number, and
                                                        new_answer_value.
            db (Session): The database session.
            current_user (str): The ID of the authenticated user.

        Returns:
            NextQuestionResponse: Details of the next question (after re-evaluation) or
                                indicates form completion.
    '''
    message = f'''User {current_user} request to update answer for question
            {update_data.question_number} in session {update_data.session_id}'''
    logger.info(message)
    return await update_answer_in_session(db, update_data, current_user)

@router.post(
    '/finalize-session',
    response_model = FinalizeFormResponse,
    status_code = status.HTTP_200_OK,
    summary = 'Finalizes a form session and persists all answers to MySQL'
)
async def finalize_form_session_route(
    finalize_data: FinalizeFormRequest,
    db: Session = Depends(GET_DB_DEPENDENCY),
    current_user: str = Depends(get_current_user)
):
    '''
        Concludes a form-filling session, moves all temporary answers from DynamoDB
        to the permanent MySQL database, and clears the temporary session.

        Args:
            finalize_data (FinalizeFormRequest): Contains the session_id to finalize.
            db (Session): The database session.
            current_user (str): The ID of the authenticated user.

        Returns:
            FinalizeFormResponse: Confirmation of finalization with the new
                                form_response_id.
    '''
    message = f'''User {current_user} request to finalize form session:
            {finalize_data.session_id}'''
    logger.info(message)
    return await finalize_form_session(db, finalize_data, current_user)

# --- Endpoints for Completed Form Responses (MySQL backed) ---

@router.get(
    '/{form_response_id}',
    response_model = FormResponseDetailResponse,
    summary = 'Get a completed form response by ID with all answers and contact info'
)
async def get_form_response_by_id_route(
    form_response_id: int,
    db: Session = Depends(GET_DB_DEPENDENCY),
    current_user: str = Depends(get_current_user)
):
    '''
        Retrieves a single completed form response by its ID, including all
        associated answers, and the contact and person details.

        Args:
            form_response_id (int): The ID of the completed form response.
            db (Session): The database session.
            current_user (str): The ID of the authenticated user.

        Returns:
            FormResponseDetailResponse: The detailed completed form response.
    '''
    message = f'''User {current_user} request to get form response by ID:
            {form_response_id}'''
    logger.info(message)
    return await get_form_response_by_id(db, form_response_id, current_user)

@router.get(
    '/',
    response_model = List[FormResponseSummaryResponse],
    summary = 'Get all completed form responses (paginated)'
)
async def get_all_form_responses_route(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(GET_DB_DEPENDENCY),
    current_user: str = Depends(get_current_user)
):
    '''
        Retrieves a paginated list of all completed form responses.
        This endpoint returns a summary view, without nested answers, for performance.

        Args:
            skip (int): The number of items to skip (for pagination).
            limit (int): The maximum number of items to return (for pagination).
            db (Session): The database session.
            current_user (str): The ID of the authenticated user.

        Returns:
            List[FormResponseSummaryResponse]: A list of summarized form responses.
    '''
    message = f'''User {current_user} request to get all form responses (skip: {skip},
            limit: {limit})'''
    logger.info(message)

    return await get_all_form_responses(db, current_user, skip = skip, limit = limit)

@router.put(
    '/{form_response_id}/status',
    response_model = FormResponseDetailResponse,
    summary = 'Update the status of a completed form response'
)
async def update_form_response_status_route(
    form_response_id: int,
    status_data: FormResponseUpdate,
    db: Session = Depends(GET_DB_DEPENDENCY),
    current_user: str = Depends(get_current_user)
):
    '''
        Updates the administrative status of a previously completed form response
        (e.g., from 'PENDING' to 'REVIEWED').

        Args:
            form_response_id (int): The ID of the form response to update.
            status_data (FormResponseUpdate): The new status to apply.
            db (Session): The database session.
            current_user (str): The ID of the authenticated user.

        Returns:
            FormResponseDetailResponse: The updated form response with its new status.
    '''
    message = f'''User {current_user} request to update status for form response
            {form_response_id} to {status_data.status.value}'''
    logger.info(message)
    return await update_form_response_status(db, form_response_id, status_data, current_user)
