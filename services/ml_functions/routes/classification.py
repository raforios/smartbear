'''
    Classification: routes handler
'''
from typing import Union, List
from fastapi import APIRouter, Depends

from controllers.classification import (
    calculating_sigmoid,
    calculating_cost_logistic,
    calculating_gradient_logistic,
    performing_gradient_descent_logistic,
    predicting_logistic_classification,
)
from schemas.classification import (
    SigmoidBatchRequest,
    ComputeCostLogisticRequest,
    ComputeGradientLogisticRequest,
    ComputeGradientLogisticResponse,
    GradientDescentLogisticRequest,
    GradientDescentLogisticResponse,
    PredictLogisticRequest,
    PredictLogisticResponse
)
from services.security import get_current_user
from services.logger_config import custom_logger as logger

router = APIRouter(prefix = '/v1/classification', tags = ['ML Classification'])

# --- Endpoint para un único valor (GET) ---
@router.get(
    '/sigmoid/{z_value}',
    response_model = float,
    summary = "Calculate sigmoid for a single value",
    description = '''Calculates the sigmoid function for a given single
        numeric input value.'''
)
async def sigmoid_scalar_algorithm(z_value: Union[float, int],
    current_user: str = Depends(get_current_user)):
    '''
    Calculates the sigmoid of a single Z-value using the machine learning service.

    This endpoint takes a single numeric input 'z_value' from the URL path
    and returns its sigmoid transformation. Authentication is required.

    Args:
        z_value (Union[float, int]): The input numeric value for which to calculate the sigmoid.
        current_user (str): The authenticated user's identifier (injected by dependency).

    Returns:
        float: The sigmoid value, which will be a float between 0 and 1.

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'User: {current_user} requested sigmoid for scalar z_value: {z_value}'
    logger.info(message)
    # Convertir a float para asegurar que el controlador reciba un tipo consistente
    return await calculating_sigmoid(float(z_value))

# --- Endpoint para una lista de valores (POST) ---
@router.post(
    '/sigmoid-batch',
    response_model = List[float],
    summary = "Calculate sigmoid for a batch of values",
    description = '''Calculates the sigmoid function for a list of numeric
        input values.'''
)
async def sigmoid_batch_algorithm(request: SigmoidBatchRequest,
    current_user: str = Depends(get_current_user)):
    '''
    Calculates the sigmoid for a batch of Z-values using the machine learning service.

    This endpoint takes a list of numeric 'z_values' in the request body
    and returns a list of their sigmoid transformations. Authentication is required.

    Args:
        request (SigmoidBatchRequest): A Pydantic model containing a list of Z-values.
        current_user (str): The authenticated user's identifier (injected by dependency).

    Returns:
        List[float]: A list of sigmoid values, each a float between 0 and 1.

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'User: {current_user} requested sigmoid for batch z_values: {request.z_values}'
    logger.info(message)
    # Pasar directamente la lista de valores al controlador
    return await calculating_sigmoid(request.z_values)

@router.post(
    '/compute-cost-logistic',
    response_model = float,
    summary = "Compute logistic regression cost",
    description = '''Calculates the cost for logistic regression based on
        provided data, weights, and bias.'''
)
async def compute_cost_logistic_algorithm(request: ComputeCostLogisticRequest,
    current_user: str = Depends(get_current_user)):
    '''
    Calculates the cost for logistic regression based on provided data, weights, and bias.

    This endpoint takes the feature matrix X, target array y, weight parameters w,
    and bias b in the request body, and returns the computed logistic cost.
    Authentication is required.

    Args:
        request (ComputeCostLogisticRequest): A Pydantic model containing X, y, w, and b.
        current_user (str): The authenticated user's identifier (injected by dependency).

    Returns:
        float: The calculated logistic regression cost.

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'User: {current_user} requested logistic cost calculation.'
    logger.info(message)
    return await calculating_cost_logistic(
        x_matrix = request.x_matrix,
        y = request.y,
        w = request.w,
        b = request.b
    )

@router.post(
    '/compute-gradient-logistic',
    response_model = ComputeGradientLogisticResponse,
    summary = "Compute logistic regression gradient",
    description = '''Calculates the gradient for logistic regression based on
        provided data, weights, and bias.'''
)
async def compute_gradient_logistic_algorithm(request: ComputeGradientLogisticRequest,
    current_user: str = Depends(get_current_user)):
    '''
    Calculates the gradient for logistic regression based on provided data, weights, and bias.

    This endpoint takes the feature matrix X, target array y, weight parameters w,
    and bias b in the request body, and returns the computed logistic gradient (dj_db, dj_dw).
    Authentication is required.

    Args:
        request (ComputeGradientLogisticRequest): A Pydantic model containing X, y, w, and b.
        current_user (str): The authenticated user's identifier (injected by dependency).

    Returns:
        ComputeGradientLogisticResponse: An object containing the calculated dj_db (scalar)
                                         and dj_dw (list of floats).

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'User: {current_user} requested logistic gradient calculation.'
    logger.info(message)
    return await calculating_gradient_logistic(
        x_matrix = request.x_matrix,
        y = request.y,
        w = request.w,
        b = request.b
    )

@router.post(
    '/gradient-descent-logistic',
    response_model = GradientDescentLogisticResponse,
    summary = "Perform logistic regression gradient descent",
    description = '''Performs logistic regression gradient descent to find
        optimal parameters (w, b).'''
)
async def gradient_descent_logistic_algorithm(request: GradientDescentLogisticRequest,
    current_user: str = Depends(get_current_user)):
    '''
    Performs logistic regression gradient descent to find optimal parameters (w, b).

    This endpoint takes the feature matrix X, target array y, initial weights w_in,
    initial bias b_in, learning rate alpha, and number of iterations num_iters
    in the request body. It returns the final weights and bias, and their history.
    Authentication is required.

    Args:
        request (GradientDescentLogisticRequest): A Pydantic model containing
                                                  X, y, w_in, b_in, alpha, and num_iters.
        current_user (str): The authenticated user's identifier (injected by dependency).

    Returns:
        GradientDescentLogisticResponse: An object containing the final w, b,
                                         and the history of cost and parameters.

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'User: {current_user} requested logistic gradient descent.'
    logger.info(message)
    return await performing_gradient_descent_logistic(request)

@router.post(
    '/predict-classification',
    response_model = PredictLogisticResponse,
    summary = "Predict labels using logistic regression",
    description = '''Predicts labels (0 or 1) using learned logistic regression
        parameters (w, b) and new data.'''
)
async def predict_classification_algorithm(request: PredictLogisticRequest,
    current_user: str = Depends(get_current_user)):
    '''
    Predicts labels (0 or 1) using learned logistic regression parameters (w, b) and new data.

    This endpoint takes a feature matrix X, learned weight parameters w, and bias b
    in the request body, and returns a list of predicted labels (0 or 1).
    Authentication is required.

    Args:
        request (PredictLogisticRequest): A Pydantic model containing X, w, and b for prediction.
        current_user (str): The authenticated user's identifier (injected by dependency).

    Returns:
        PredictLogisticResponse: An object containing the list of predicted labels.

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'User: {current_user} requested logistic prediction.'
    logger.info(message)
    return await predicting_logistic_classification(request)
