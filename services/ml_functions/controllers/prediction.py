'''
    Prediction controller
'''

import numpy as np
from services.logger_config import custom_logger as logger

from services.machine_learning import (
    compute_cost_matrix,
    compute_gradient_matrix,
    gradient_descent_matrix,
    predict_dot,
    compute_cost,
    compute_gradient,
    gradient_descent
)
from services.exceptions import ServiceUnavailableError
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

async def compute_cost_linear_regression(
    request: ComputeCostLinearRequest
) -> ComputeCostLinearResponse:
    '''
    Controller to calculate the cost of linear regression.

    This function receives the feature matrix X, target vector y, weights w,
    and bias b, converts them to NumPy arrays, and computes the cost using
    `compute_cost_matrix` from the machine learning service.
    It handles potential errors by raising an ServiceUnavailableError.

    Args:
        request (ComputeCostLinearRequest): A Pydantic model containing
                                                    x_matrix, y, w, and b.

    Returns:
        ComputeCostLinearResponse: An object containing the calculated
                                            linear regression cost as a float.

    Raises:
        ServiceUnavailableError: If an internal server error occurs during processing.
    '''
    try:
        # Convert incoming Python lists/scalars to NumPy arrays for computation
        x_matrix_np = np.array(request.x_matrix, dtype = np.float64)
        y_np = np.array(request.y, dtype = np.float64)
        w_np = np.array(request.w, dtype = np.float64)
        b_val = request.b
        message = f'''Calculating linear regression cost for x_matrix shape:
            {x_matrix_np.shape}, w shape: {w_np.shape}'''
        logger.info(message)

        # Call the cost function from machine_learning
        cost = compute_cost_matrix(x_matrix_np, y_np, w_np, b_val)

        message = f'Linear regression cost calculated: {cost}'
        logger.info(message)
        return ComputeCostLinearResponse(cost = float(cost))
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'''Internal server error while processing linear regression
            cost calculation: {e}'''
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e


async def compute_gradient_linear_regression(
    request: ComputeGradientLinearRequest
) -> ComputeGradientLinearResponse:
    '''
    Controller to calculate the gradient of linear regression.

    This function takes the feature matrix X, target vector y, weights w,
    and bias b, converts them to NumPy arrays, and computes the gradients
    dj_dw and dj_db using `compute_gradient_matrix` from the machine learning service.
    It handles potential errors by raising an ServiceUnavailableError.

    Args:
        request (ComputeGradientLinearRequest): A Pydantic model containing
                                                        x_matrix, y, w, and b.

    Returns:
        ComputeGradientLinearResponse: An object containing dj_db (float)
                                                and dj_dw (list of floats).

    Raises:
        ServiceUnavailableError: If an internal server error occurs during processing.
    '''
    try:
        # Convert incoming Python lists/scalars to NumPy arrays for computation
        x_matrix_np = np.array(request.x_matrix, dtype = np.float64)
        y_np = np.array(request.y, dtype = np.float64)
        w_np = np.array(request.w, dtype = np.float64)
        b_val = request.b
        message = f'''Calculating linear regression gradient for x_matrix shape:
            {x_matrix_np.shape}, w shape: {w_np.shape}'''
        logger.info(message)

        # Call the gradient function from machine_learning
        dj_dw, dj_db  = compute_gradient_matrix(x_matrix_np, y_np, w_np, b_val)

        # Convert NumPy array results back to Python lists for JSON serialization
        dj_dw_list = dj_dw.tolist()

        message = f'Linear regression gradient calculated: dj_db = {dj_db}, dj_dw = {dj_dw_list}'
        logger.info(message)
        return ComputeGradientLinearResponse(
            dj_db = float(dj_db),
            dj_dw = dj_dw_list
        )
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'''Internal server error while processing linear regression
            gradient calculation: {e}'''
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e


async def train_linear_regression(
    request: TrainLinearRegressionRequest
) -> TrainLinearRegressionResponse:
    '''
    Controller for training linear regression using gradient descent.

    This function performs batch gradient descent to learn the optimal
    parameters (w, b) for a linear regression model. It takes initial parameters,
    learning rate, and number of iterations, then calls `gradient_descent_matrix`
    from the machine learning service. It returns the final parameters and
    the history of cost and parameters during training.
    It handles potential errors by raising an ServiceUnavailableError.

    Args:
        request (TrainLinearRegressionRequest): A Pydantic model containing
                                                x_matrix, y, initial w (w_in),
                                                initial b (b_in), alpha (learning rate),
                                                and num_iters (number of iterations).

    Returns:
        TrainLinearRegressionResponse: An object containing the final weights (w_final),
                                    final bias (b_final), history of costs (J_history),
                                    and history of parameters (p_history).

    Raises:
        ServiceUnavailableError: If an internal server error occurs during processing.
    '''
    try:
        # Convert incoming Python lists/scalars to NumPy arrays for computation
        x_matrix_np = np.array(request.x_matrix, dtype = np.float64)
        y_np = np.array(request.y, dtype = np.float64)
        w_in_np = np.array(request.w_in, dtype = np.float64)
        message = f'''Starting linear regression training for x_matrix shape:
            {x_matrix_np.shape} with {request.num_iters} iterations.'''
        logger.info(message)

        # Call the gradient descent function from machine_learning
        w_final_np, b_final_val, hist_dict = gradient_descent_matrix(
            x_matrix_np, y_np, w_in_np, request.b_in, request.alpha, request.num_iters
        )

        # Convert history results back to Python lists for JSON serialization
        j_history_list = [float(cost) for cost in hist_dict['cost']]

        # p_history (parameters history) is List[List[w, b]] where w is np.ndarray, b is scalar
        p_history_serializable = []
        for params_pair in hist_dict['params']:
            w_hist = (params_pair[0].tolist() if isinstance(params_pair[0], np.ndarray)
                      else params_pair[0])
            b_hist = float(params_pair[1])
            p_history_serializable.append([w_hist, b_hist])

        message = f'''Linear regression training completed. Final w:
            {w_final_np.tolist()}, b: {b_final_val}'''
        logger.info(message)
        return TrainLinearRegressionResponse(
            w_final = w_final_np.tolist(),
            b_final = float(b_final_val),
            J_history = j_history_list,
            p_history = p_history_serializable
        )
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'''Internal server error while performing linear regression
            training: {e}'''
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e


async def predict_linear_regression(
    request: PredictLinearRequest
) -> PredictLinearResponse:
    '''
    Controller for making predictions with a trained linear regression model.

    This function takes new input features (x_test) along with trained
    model parameters (w, b), converts them to NumPy arrays, and
    generates predictions using `predict_dot` from the machine learning service.
    It handles potential errors by raising an ServiceUnavailableError.

    Args:
        request (PredictLinearRequest): A Pydantic model containing
                                                  x_test (matrix of new examples),
                                                  trained w (weights), and trained b (bias).

    Returns:
        PredictLinearResponse: An object containing a list of
                                         predicted values for the input examples.

    Raises:
        ServiceUnavailableError: If an internal server error occurs during processing.
    '''
    try:
        # Convert incoming Python lists/scalars to NumPy arrays for computation
        x_test_np = np.array(request.x_test, dtype = np.float64)
        w_np = np.array(request.w, dtype = np.float64)
        b_val = request.b
        message = f'''Making predictions for x_test of shape:
            {x_test_np.shape} using trained w and b.'''
        logger.info(message)

        # Call the prediction function from machine_learning
        predictions_np = predict_dot(x_test_np, w_np, b_val)

        # Convert NumPy array results back to Python list for JSON serialization
        predictions_list = predictions_np.tolist()

        message = f'''Linear regression prediction completed.
            Predicted values for {x_test_np.shape[0]} samples.'''
        logger.info(message)
        return PredictLinearResponse(predictions = predictions_list)
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'''Internal server error while performing linear regression
            prediction: {e}'''
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e

async def compute_cost_single_linear_regression(
    request: ComputeCostSingleLinearRequest
) -> ComputeCostSingleLinearResponse:
    '''
    Controller to calculate the cost of single-feature linear regression.
    '''
    try:
        x_np = np.array(request.x, dtype = np.float64)
        y_np = np.array(request.y, dtype = np.float64)
        w_val = request.w
        b_val = request.b
        message = f'''Calculating single-feature linear regression cost for x shape:
            {x_np.shape}, w: {w_val}'''
        logger.info(message)

        cost = compute_cost(x_np, y_np, w_val, b_val)

        message = f'Single-feature linear regression cost calculated: {cost}'
        logger.info(message)
        return ComputeCostSingleLinearResponse(cost=float(cost))
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'''Internal server error while processing single-feature linear regression
            cost calculation: {e}'''
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e


async def compute_gradient_single_linear_regression(
    request: ComputeGradientSingleLinearRequest
) -> ComputeGradientSingleLinearResponse:
    '''
    Controller to calculate the gradient of single-feature linear regression.
    '''
    try:
        x_np = np.array(request.x, dtype = np.float64)
        y_np = np.array(request.y, dtype = np.float64)
        w_val = request.w
        b_val = request.b
        message = f'''Calculating single-feature linear regression gradient for x shape:
            {x_np.shape}, w: {w_val}'''
        logger.info(message)

        dj_dw, dj_db = compute_gradient(x_np, y_np, w_val, b_val)

        message = f'''Single-feature linear regression gradient calculated:
        dj_dw = {dj_dw}, dj_db = {dj_db}'''
        logger.info(message)
        return ComputeGradientSingleLinearResponse(
            dj_dw = float(dj_dw),
            dj_db = float(dj_db)
        )
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'''Internal server error while processing single-feature linear regression
            gradient calculation: {e}'''
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e

async def train_single_linear_regression(
    request: TrainSingleLinearRegressionRequest
) -> TrainSingleLinearRegressionResponse:
    '''
    Controller for training single-feature linear regression using gradient descent.
    '''
    try:
        x_np = np.array(request.x, dtype = np.float64)
        y_np = np.array(request.y, dtype = np.float64)
        message = f'''Starting single-feature linear regression training for x shape:
            {x_np.shape} with {request.num_iters} iterations.'''
        logger.info(message)

        w_final, b_final, j_history, p_history = gradient_descent(
            x_np, y_np, request.w_in, request.b_in, request.alpha, request.num_iters
        )

        j_history_list = [float(cost) for cost in j_history]
        p_history_serializable = []
        for params_pair in p_history:
            w_hist = float(params_pair[0])
            b_hist = float(params_pair[1])
            p_history_serializable.append([w_hist, b_hist])

        message = f'''Single-feature linear regression training completed. Final w:
            {w_final}, b: {b_final}'''
        logger.info(message)
        return TrainSingleLinearRegressionResponse(
            w_final = float(w_final),
            b_final = float(b_final),
            J_history = j_history_list,
            p_history = p_history_serializable
        )
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'''Internal server error while performing single-feature linear regression
            training: {e}'''
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e

async def compute_cost_matrix_controller(
    request: ComputeCostMatrixRequest
) -> ComputeCostMatrixResponse:
    '''
    Controller for calculating the cost in multi-feature linear regression.

    This function takes a feature matrix X, target vector y, weight vector w,
    and bias b, converts them to NumPy arrays, and computes the cost using
    the `compute_cost_matrix` function from the machine learning service.
    It handles potential errors by raising an ServiceUnavailableError.

    Args:
        request (ComputeCostMatrixRequest): A Pydantic model containing
                                            x_matrix, y, w, and b.

    Returns:
        ComputeCostMatrixResponse: An object containing the calculated cost
                                   as a float.

    Raises:
        ServiceUnavailableError: If an internal server error occurs during processing.
    '''
    try:
        x_matrix_np = np.array(request.x_matrix, dtype = np.float64)
        y_np = np.array(request.y, dtype = np.float64)
        w_np = np.array(request.w, dtype = np.float64)
        b_val = request.b
        message = f'''Calculating cost for matrix operation. x_matrix shape:
            {x_matrix_np.shape}, w shape: {w_np.shape}'''
        logger.info(message)

        cost = compute_cost_matrix(x_matrix_np, y_np, w_np, b_val)

        message = f'Matrix cost calculation completed: {cost}'
        logger.info(message)
        return ComputeCostMatrixResponse(cost=float(cost))
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'''Internal server error during matrix cost calculation:
            {e}'''
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e


async def compute_gradient_matrix_controller(
    request: ComputeGradientMatrixRequest
) -> ComputeGradientMatrixResponse:
    '''
    Controller for calculating gradients in multi-feature linear regression.

    This function takes a feature matrix X, target vector y, weight vector w,
    and bias b, converts them to NumPy arrays, and computes the gradients
    dj_dw and dj_db using the `compute_gradient_matrix` function from the
    machine learning service. It handles potential errors by raising an
    ServiceUnavailableError.

    Args:
        request (ComputeGradientMatrixRequest): A Pydantic model containing
                                                x_matrix, y, w, and b.

    Returns:
        ComputeGradientMatrixResponse: An object containing dj_db (float)
                                       and dj_dw (list of floats).

    Raises:
        ServiceUnavailableError: If an internal server error occurs during processing.
    '''
    try:
        x_matrix_np = np.array(request.x_matrix, dtype = np.float64)
        y_np = np.array(request.y, dtype = np.float64)
        w_np = np.array(request.w, dtype = np.float64)
        b_val = request.b
        message = f'''Calculating gradient for matrix operation. x_matrix shape:
            {x_matrix_np.shape}, w shape: {w_np.shape}'''
        logger.info(message)

        dj_dw, dj_db = compute_gradient_matrix(
            x_matrix_np, y_np, w_np, b_val
        )

        dj_dw_list = dj_dw.tolist()
        message = f'''Matrix gradient calculation completed: dj_db = {dj_db},
                dj_dw = {dj_dw_list}'''
        logger.info(message)
        return ComputeGradientMatrixResponse(
            dj_db = float(dj_db),
            dj_dw = dj_dw_list
        )
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'''Internal server error during matrix gradient calculation:
            {e}'''
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e


async def gradient_descent_matrix_controller(
    request: GradientDescentMatrixRequest
) -> GradientDescentMatrixResponse:
    '''
    Controller for performing gradient descent in multi-feature linear
    regression.

    This function executes batch gradient descent to optimize the parameters
    (w, b) for a linear regression model. It receives initial parameters,
    learning rate, and number of iterations, then calls the
    `gradient_descent_matrix` function from the machine learning service.
    It returns the final optimized parameters and a detailed history of the
    training process, including costs, parameters, and gradients at each
    iteration. It handles potential errors by raising an ServiceUnavailableError.

    Args:
        request (GradientDescentMatrixRequest): A Pydantic model containing
                                                x_matrix, y, initial w (w_in),
                                                initial b (b_in), alpha
                                                (learning rate),
                                                and num_iters (number of
                                                iterations).

    Returns:
        GradientDescentMatrixResponse: An object containing the final
                                       weights (w_final), final bias (b_final),
                                       history of costs (J_history), and
                                       detailed history including parameters
                                       and gradients (hist_details).

    Raises:
        ServiceUnavailableError: If an internal server error occurs during processing.
    '''
    try:
        x_matrix_np = np.array(request.x_matrix, dtype = np.float64)
        y_np = np.array(request.y, dtype = np.float64)
        w_in_np = np.array(request.w_in, dtype = np.float64)
        message = f'''Starting gradient descent for matrix operation with
            {request.num_iters} iterations.'''
        logger.info(message)

        w_final_np, b_final_val, hist_dict = gradient_descent_matrix(
            x_matrix_np, y_np, w_in_np, request.b_in, request.alpha,
            request.num_iters
        )

        j_history_list = [float(cost) for cost in hist_dict['cost']]

        # Convert historical NumPy arrays/scalars to serializable Python lists
        hist_details_serializable = {
            'iter': hist_dict['iter'],
            'cost': [float(c) for c in hist_dict['cost']],
            'params': [
                [p[0].tolist(), float(p[1])]
                for p in hist_dict['params']
            ],
            'grads': [
                [g[0].tolist(), float(g[1])]
                for g in hist_dict['grads']
            ]
        }

        message = f'''Matrix gradient descent completed. Final w:
            {w_final_np.tolist()}, b: {b_final_val}'''
        logger.info(message)
        return GradientDescentMatrixResponse(
            w_final = w_final_np.tolist(),
            b_final = float(b_final_val),
            J_history = j_history_list,
            hist_details = hist_details_serializable
        )
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'''Internal server error during matrix gradient descent:
            {e}'''
        logger.error(error_msg, exc_info=True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e
