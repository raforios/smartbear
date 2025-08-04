'''
    Classification controller
'''
from typing import Union, List
import numpy as np
from services.logger_config import custom_logger as logger
from services.machine_learning import (
    sigmoid,
    compute_cost_logistic,
    compute_gradient_logistic,
    gradient_descent_logistic,
    predict_logistic
)
from services.exceptions import ServiceUnavailableError
from schemas.classification import (
    GradientDescentLogisticRequest,
    PredictLogisticRequest,
    PredictLogisticResponse
)

async def calculating_sigmoid(z_value: Union[float, int,
    List[Union[float, int]]]) -> Union[float, np.ndarray]:
    '''
    Calculates the sigmoid function for a given input value or array of values.

    This function takes a numeric scalar or a list of numeric values,
    applies the sigmoid transformation, and logs the operation.
    It's designed to be robust to different input types that can be converted to NumPy.

    Args:
        z_value (Union[float, int, List[Union[float, int]]]): The input value(s) for which to
        calculate the sigmoid. Can be a single float/int or a list of floats/ints.

    Returns:
        Union[float, numpy.ndarray]: The result of the sigmoid calculation.
                                     Returns a float if z_value was a scalar,
                                     or a NumPy array if z_value was a list.

    Raises:
        ServiceUnavailableError: If an internal server error occurs during processing.
    '''
    try:
        # Convert incoming Python lists back to NumPy arrays if it's the case
        z_input = np.array(z_value) if isinstance(z_value, list) else z_value

        response = sigmoid(z_input)
        message = f'''{z_value} z_values generated the following values after calculating
        the sigmoid: {response}.'''
        logger.info(message)
        return response
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'Internal server error while processing the sigmoid calculation: {e}'
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e

async def calculating_cost_logistic(
    x_matrix: List[List[float]],
    y: List[float],
    w: List[float],
    b: float
) -> float:
    '''
    Calculates the logistic regression cost using the compute_cost_logistic.

    Args:
        x_matrix (List[List[float]]): Feature matrix X as a list of lists.
        y (List[float]): Target array y as a list.
        w (List[float]): Weight parameters w as a list.
        b (float): Bias parameter b.

    Returns:
        float: The calculated logistic regression cost.

    Raises:
        ServiceUnavailableError: If an internal server error occurs during processing.
    '''
    try:
        # Convert incoming Python lists back to NumPy arrays
        x_matrix_np = np.array(x_matrix, dtype = np.float64)
        y_np = np.array(y, dtype = np.float64)
        w_np = np.array(w, dtype = np.float64)


        # Call the logistic cost function from machine_learning
        cost = compute_cost_logistic(x_matrix_np, y_np, w_np, b)
        message = f'Logistic cost calculated: {cost}'
        logger.info(message)
        return float(cost)
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'Internal server error while processing logistic cost calculation: {e}'
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e

async def calculating_gradient_logistic(
    x_matrix: List[List[float]],
    y: List[float],
    w: List[float],
    b: float
) -> dict:
    '''
    Calculates the logistic regression gradient using the compute_gradient_logistic.

    Args:
        x_matrix (List[List[float]]): Feature matrix X as a list of lists.
        y (List[float]): Target array y as a list.
        w (List[float]): Weight parameters w as a list.
        b (float): Bias parameter b.

    Returns:
        dict: A dictionary containing 'dj_db' (float) and 'dj_dw' (List[float]).

    Raises:
        ServiceUnavailableError: If an internal server error occurs during processing.
    '''
    try:
        # Convert incoming Python lists back to NumPy arrays
        x_matrix_np = np.array(x_matrix, dtype = np.float64)
        y_np = np.array(y, dtype = np.float64)
        w_np = np.array(w, dtype = np.float64)


        # Call the logistic gradient function from machine_learning
        dj_dw, dj_db = compute_gradient_logistic(x_matrix_np, y_np, w_np, b)
        message = f'Logistic gradient calculated: dj_db = {dj_db}, dj_dw = {dj_dw.tolist()}'
        logger.info(message)

        dj_db_out = float(dj_db)
        dj_dw_out = dj_dw.tolist()

        return {"dj_db": dj_db_out, "dj_dw": dj_dw_out}
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'Internal server error while processing logistic gradient calculation: {e}'
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e

async def performing_gradient_descent_logistic(
    request: GradientDescentLogisticRequest
) -> dict:
    '''
    Performs logistic regression gradient descent using gradient_descent_logistic.

    Args:
        request (GradientDescentLogisticRequest): A Pydantic model containing
        x_matrix, y, w_in, b_in, alpha, and num_iters.

    Returns:
        dict: A dictionary containing 'w' (final weights), 'b' (final bias),
        'J_history' (list of costs), and 'p_history' (list of [w, b] pairs).

    Raises:
        ServiceUnavailableError: If an internal server error occurs during processing.
    '''
    try:
        # Convert incoming Python lists back to NumPy arrays
        x_matrix_np = np.array(request.x_matrix, dtype = np.float64)
        y_np = np.array(request.y, dtype = np.float64)
        w_in_np = np.array(request.w_in, dtype=np.float64)


        # Call the logistic gradient descent function from machine_learning
        w_final, b_final, j_history, p_history = gradient_descent_logistic(
            x_matrix_np, y_np, w_in_np, request.b_in, request.alpha, request.num_iters)


        # Convert NumPy arrays in results back to Python lists for JSON serialization
        # p_history is List[List[w, b]] where w is np.ndarray, so convert each w to list
        p_history_serializable = []
        for w_val, b_val in p_history:
            p_history_serializable.append([w_val.tolist(), float(b_val)])

        response_data = {
            'w': w_final.tolist(),
            'b': float(b_final),
            'J_history': [float(cost) for cost in j_history],
            'p_history': p_history_serializable
        }
        message = f'Logistic gradient descent completed. Final w: {w_final.tolist()}, b: {b_final}'
        logger.info(message)
        return response_data
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'Internal server error while performing logistic gradient descent: {e}'
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e

async def predicting_logistic_classification(
    request: PredictLogisticRequest
) -> PredictLogisticResponse:
    '''
    Performs logistic regression prediction using predict_logistic.

    Args:
        request (PredictLogisticRequest): A Pydantic model containing
                                          x_matrix, w, and b for prediction.

    Returns:
        PredictLogisticResponse: An object containing the list of predicted labels (0 or 1).

    Raises:
        ServiceUnavailableError: If an internal server error occurs during processing.
    '''
    try:
        # Convert incoming Python lists back to NumPy arrays
        x_matrix_np = np.array(request.x_matrix, dtype=np.float64)
        w_np = np.array(request.w, dtype=np.float64)

        # Call the logistic prediction function from machine_learning
        predictions_np = predict_logistic(x_matrix_np, w_np, request.b)

        # Convert NumPy array results back to Python list for JSON serialization
        predictions_list = predictions_np.tolist()

        message = f'Logistic prediction completed. Predicted labels: {predictions_list}'
        logger.info(message)

        return PredictLogisticResponse(predictions=predictions_list)
    # pylint: disable=R0801
    except Exception as e:
        error_msg = f'Internal server error while performing logistic prediction: {e}'
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e
