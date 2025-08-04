'''
    Common controller
'''
import numpy as np
from services.logger_config import custom_logger as logger
from services.machine_learning import (
    zscore_normalize_features
)
from services.exceptions import ServiceUnavailableError
from schemas.common import (
    NormalizeFeaturesRequest,
    NormalizeFeaturesResponse
)

async def normalize_features(
    request: NormalizeFeaturesRequest
) -> NormalizeFeaturesResponse:
    '''
    Normalizes a feature matrix X using Z-score normalization.

    Args:
    request (NormalizeFeaturesRequest): A Pydantic model containing the matrix X to normalize.

    Returns:
    NormalizeFeaturesResponse: An object containing the normalized matrix (x_norm),
    the means (mu), and the standard deviations (sigma).

    Raises:
        ServiceUnavailableError: If an internal server error occurs during processing.
    '''
    try:
        # Convert incoming Python lists back to NumPy arrays
        x_matrix_np = np.array(request.x_matrix, dtype=np.float64)

        message = f'''Normalizing features for x_matrix of shape:
            {x_matrix_np.shape}'''
        logger.info(message)

        # Calling the normalization function from machine_learning
        x_norm_np, mu_np, sigma_np = zscore_normalize_features(x_matrix_np)

        # Convert NumPy array results back to Python list for JSON serialization
        x_norm_list = x_norm_np.tolist()
        mu_list = mu_np.tolist()
        sigma_list = sigma_np.tolist()

        message = f'''Feature normalization completed. X_norm shape:
            {x_norm_np.shape}, Mu: {mu_list}, Sigma: {sigma_list}'''
        logger.info(message)

        logger.info(message)

        return NormalizeFeaturesResponse(x_norm = x_norm_list, mu = mu_list, sigma = sigma_list)
    except Exception as e:
        error_msg = f'Internal server error while performing feature normalization: {e}'
        logger.error(error_msg, exc_info = True)
        raise ServiceUnavailableError(
            detail = error_msg
        ) from e
