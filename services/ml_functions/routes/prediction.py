'''
    Prediction: routes handler
'''
from fastapi import APIRouter, Depends
from services.security import get_current_user
from services.logger_config import custom_logger as logger
from controllers.prediction import (
    compute_cost_linear_regression,
    compute_gradient_linear_regression,
    train_linear_regression,
    predict_linear_regression,
    compute_cost_single_linear_regression,
    compute_gradient_single_linear_regression,
    train_single_linear_regression,
    compute_cost_matrix_controller,
    compute_gradient_matrix_controller,
    gradient_descent_matrix_controller
)
from schemas.prediction import (
    ComputeCostLinearRequest,
    ComputeCostLinearResponse,
    ComputeGradientLinearRequest,
    ComputeGradientLinearResponse,
    TrainLinearRegressionRequest,
    TrainLinearRegressionResponse,
    PredictLinearRequest,
    PredictLinearResponse,
    ComputeCostSingleLinearRequest,
    ComputeCostSingleLinearResponse,
    ComputeGradientSingleLinearRequest,
    ComputeGradientSingleLinearResponse,
    TrainSingleLinearRegressionRequest,
    TrainSingleLinearRegressionResponse,
    ComputeCostMatrixRequest,
    ComputeCostMatrixResponse,
    ComputeGradientMatrixRequest,
    ComputeGradientMatrixResponse,
    GradientDescentMatrixRequest,
    GradientDescentMatrixResponse
)

router = APIRouter(prefix = '/v1/prediction', tags = ['ML Prediction'])

@router.post(
    '/compute-cost',
    response_model = ComputeCostLinearResponse, # Changed
    summary = 'Compute linear regression cost',
    description = '''Calculates the cost (J) for a given linear regression
        model (X, y, w, b).'''
)
async def compute_cost_linear_regression_route(
    request: ComputeCostLinearRequest, # Changed
    current_user: str = Depends(get_current_user)
):
    '''
    Calculates the cost for linear regression based on provided data, weights, and bias.

    This endpoint takes the feature matrix X, target array y, weight parameters w,
    and bias b in the request body, and returns the computed linear regression cost.
    Authentication is required.

    Args:
        request (ComputeCostLinearRequest): A Pydantic model containing
                                                      X_matrix, y, w, and b.
        current_user (str): The authenticated user's identifier
                            (dependency-injected).

    Returns:
        ComputeCostLinearResponse: An object containing the calculated
                                             linear regression cost as a float.

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'''User: {current_user} requested linear regression cost
        calculation.'''
    logger.info(message)
    return await compute_cost_linear_regression(request)


@router.post(
    '/compute-gradient',
    response_model = ComputeGradientLinearResponse, # Changed
    summary = 'Compute linear regression gradient',
    description = '''Calculates the gradients (dj_dw, dj_db) for a given linear
        regression model (X, y, w, b).'''
)
async def compute_gradient_linear_regression_route(
    request: ComputeGradientLinearRequest, # Changed
    current_user: str = Depends(get_current_user)
):
    '''
    Calculates the gradient for linear regression based on provided data, weights, and bias.

    This endpoint takes the feature matrix X, target array y, weight parameters w,
    and bias b in the request body, and returns the computed linear regression
    gradient (dj_db, dj_dw). Authentication is required.

    Args:
        request (ComputeGradientLinearRequest): A Pydantic model containing
                                                          X_matrix, y, w, and b.
        current_user (str): The authenticated user's identifier
                            (dependency-injected).

    Returns:
        ComputeGradientLinearResponse: An object containing dj_db (float)
                                                 and dj_dw (list of floats).

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'''User: {current_user} requested linear regression gradient
        calculation.'''
    logger.info(message)
    return await compute_gradient_linear_regression(request)


@router.post(
    '/train-linear-regression',
    response_model = TrainLinearRegressionResponse,
    summary = 'Train linear regression model using gradient descent',
    description = '''Performs batch gradient descent to train a linear regression
        model and returns the final parameters (w, b) and training history.'''
)
async def train_linear_regression_route(
    request: TrainLinearRegressionRequest,
    current_user: str = Depends(get_current_user)
):
    '''
    Performs linear regression gradient descent to find optimal parameters (w, b).

    This endpoint takes the feature matrix X, target array y, initial weights w_in,
    initial bias b_in, learning rate alpha, and number of iterations num_iters
    in the request body. It returns the final weights and bias, and their history.
    Authentication is required.

    Args:
        request (TrainLinearRegressionRequest): A Pydantic model containing
                                                X_matrix, y, initial w, initial b,
                                                alpha, and num_iters.
        current_user (str): The authenticated user's identifier
                            (dependency-injected).

    Returns:
        TrainLinearRegressionResponse: An object containing the final w, b,
                                       and the history of cost and parameters.

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'''User: {current_user} requested linear regression training
        using gradient descent.'''
    logger.info(message)
    return await train_linear_regression(request)


@router.post(
    '/predict-linear-regression',
    response_model = PredictLinearResponse, # Changed
    summary = 'Make predictions using a trained linear regression model',
    description = '''Uses a trained linear regression model (w, b) to predict
        output for new input features (X_test).'''
)
async def predict_linear_regression_route(
    request: PredictLinearRequest, # Changed
    current_user: str = Depends(get_current_user)
):
    '''
    Predicts values using learned linear regression parameters (w, b) and new data.

    This endpoint takes a feature matrix X_test, learned weight parameters w,
    and bias b in the request body, and returns a list of predicted values.
    Authentication is required.

    Args:
        request (PredictLinearRequest): A Pydantic model containing
                                                  X_test, w, and b for prediction.
        current_user (str): The authenticated user's identifier
                            (dependency-injected).

    Returns:
        PredictLinearResponse: An object containing the list of predicted values.

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'''User: {current_user} requested linear regression prediction
        for new data.'''
    logger.info(message)
    return await predict_linear_regression(request)

@router.post(
    '/compute-cost-single-feature',
    response_model = ComputeCostSingleLinearResponse,
    summary = 'Compute single-feature linear regression cost',
    description = '''Calculates the cost (J) for a given single-feature linear
        regression model (x, y, w, b).'''
)
async def compute_cost_single_linear_regression_route(
    request: ComputeCostSingleLinearRequest,
    current_user: str = Depends(get_current_user)
):
    '''
    Calculates the cost for single-feature linear regression based on provided
    data, weight, and bias.

    This endpoint takes the feature vector x, target array y, weight parameter w,
    and bias b in the request body, and returns the computed single-feature
    linear regression cost. Authentication is required.

    Args:
        request (ComputeCostSingleLinearRequest): A Pydantic model containing
                                                  x, y, w, and b.
        current_user (str): The authenticated user's identifier
                            (dependency-injected).

    Returns:
        ComputeCostSingleLinearResponse: An object containing the calculated
                                         single-feature linear regression cost as a float.

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'''User: {current_user} requested single-feature linear regression
        cost calculation.'''
    logger.info(message)
    return await compute_cost_single_linear_regression(request)


@router.post(
    '/compute-gradient-single-feature',
    response_model = ComputeGradientSingleLinearResponse,
    summary = 'Compute single-feature linear regression gradient',
    description = '''Calculates the gradients (dj_dw, dj_db) for a given single-feature
        linear regression model (x, y, w, b).'''
)
async def compute_gradient_single_linear_regression_route(
    request: ComputeGradientSingleLinearRequest,
    current_user: str = Depends(get_current_user)
):
    '''
    Calculates the gradient for single-feature linear regression based on provided
    data, weight, and bias.

    This endpoint takes the feature vector x, target array y, weight parameter w,
    and bias b in the request body, and returns the computed single-feature
    linear regression gradient (dj_dw, dj_db). Authentication is required.

    Args:
        request (ComputeGradientSingleLinearRequest): A Pydantic model containing
                                                      x, y, w, and b.
        current_user (str): The authenticated user's identifier
                            (dependency-injected).

    Returns:
        ComputeGradientSingleLinearResponse: An object containing dj_dw (float)
                                             and dj_db (float).

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'''User: {current_user} requested single-feature linear regression
        gradient calculation.'''
    logger.info(message)
    return await compute_gradient_single_linear_regression(request)


@router.post(
    '/train-single-linear-regression',
    response_model = TrainSingleLinearRegressionResponse,
    summary = 'Train single-feature linear regression model using gradient descent',
    description = '''Performs batch gradient descent to train a single-feature linear
        regression model and returns the final parameters (w, b) and training history.'''
)
async def train_single_linear_regression_route(
    request: TrainSingleLinearRegressionRequest,
    current_user: str = Depends(get_current_user)
):
    '''
    Performs single-feature linear regression gradient descent to find optimal
    parameters (w, b).

    This endpoint takes the feature vector x, target array y, initial weight w_in,
    initial bias b_in, learning rate alpha, and number of iterations num_iters
    in the request body. It returns the final weight and bias, and their history.
    Authentication is required.

    Args:
        request (TrainSingleLinearRegressionRequest): A Pydantic model containing
                                                      x, y, initial w, initial b,
                                                      alpha, and num_iters.
        current_user (str): The authenticated user's identifier
                            (dependency-injected).

    Returns:
        TrainSingleLinearRegressionResponse: An object containing the final w, b,
                                             and the history of cost and parameters.

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'''User: {current_user} requested single-feature linear regression
        training using gradient descent.'''
    logger.info(message)
    return await train_single_linear_regression(request)

@router.post(
    '/compute-cost-matrix',
    response_model = ComputeCostMatrixResponse,
    summary = 'Compute cost for multi-feature linear regression (matrix ops)',
    description = '''Calculates the cost (J) for a given multi-feature linear
        regression model using matrix operations (X_matrix, y, w, b).'''
)
async def compute_cost_matrix_route(
    request: ComputeCostMatrixRequest,
    current_user: str = Depends(get_current_user)
):
    '''
    Calculates the cost for multi-feature linear regression based on provided
    data, weights, and bias using matrix operations.

    This endpoint takes the feature matrix X, target array y, weight parameters w,
    and bias b in the request body, and returns the computed linear regression
    cost. Authentication is required.

    Args:
        request (ComputeCostMatrixRequest): A Pydantic model containing
                                            x_matrix, y, w, and b.
        current_user (str): The authenticated user's identifier
                            (dependency-injected).

    Returns:
        ComputeCostMatrixResponse: An object containing the calculated
                                   linear regression cost as a float.

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'''User: {current_user} requested cost calculation for multi-
        feature linear regression using matrix operations.'''
    logger.info(message)
    return await compute_cost_matrix_controller(request)


@router.post(
    '/compute-gradient-matrix',
    response_model = ComputeGradientMatrixResponse,
    summary = 'Compute gradient for multi-feature linear regression (matrix ops)',
    description = '''Calculates the gradients (dj_dw, dj_db) for a given multi-
        feature linear regression model using matrix operations (X_matrix, y, w, b).'''
)
async def compute_gradient_matrix_route(
    request: ComputeGradientMatrixRequest,
    current_user: str = Depends(get_current_user)
):
    '''
    Calculates the gradient for multi-feature linear regression based on provided
    data, weights, and bias using matrix operations.

    This endpoint takes the feature matrix X, target array y, weight parameters w,
    and bias b in the request body, and returns the computed linear regression
    gradient (dj_db, dj_dw). Authentication is required.

    Args:
        request (ComputeGradientMatrixRequest): A Pydantic model containing
                                                x_matrix, y, w, and b.
        current_user (str): The authenticated user's identifier
                            (dependency-injected).

    Returns:
        ComputeGradientMatrixResponse: An object containing dj_db (float)
                                       and dj_dw (list of floats).

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'''User: {current_user} requested gradient calculation for
        multi-feature linear regression using matrix operations.'''
    logger.info(message)
    return await compute_gradient_matrix_controller(request)


@router.post(
    '/train-matrix-linear-regression',
    response_model = GradientDescentMatrixResponse,
    summary = 'Train multi-feature linear regression model using gradient descent (matrix ops)',
    description = '''Performs batch gradient descent to train a multi-feature
        linear regression model using matrix operations and returns final parameters
        (w, b) and training history.'''
)
async def gradient_descent_matrix_route(
    request: GradientDescentMatrixRequest,
    current_user: str = Depends(get_current_user)
):
    '''
    Performs multi-feature linear regression gradient descent to find optimal
    parameters (w, b) using matrix operations.

    This endpoint takes the feature matrix X, target array y, initial weights w_in,
    initial bias b_in, learning rate alpha, and number of iterations num_iters
    in the request body. It returns the final weights and bias, and their history.
    Authentication is required.

    Args:
        request (GradientDescentMatrixRequest): A Pydantic model containing
                                                x_matrix, y, initial w, initial b,
                                                alpha, and num_iters.
        current_user (str): The authenticated user's identifier
                            (dependency-injected).

    Returns:
        GradientDescentMatrixResponse: An object containing the final w, b,
                                       and the history of cost and parameters.

    Raises:
        UnauthorizedError: If authentication fails.
        ServiceUnavailableError: If an internal server error occurs during calculation.
    '''
    message = f'''User: {current_user} requested training for multi-feature
        linear regression using matrix operations.'''
    logger.info(message)
    return await gradient_descent_matrix_controller(request)
