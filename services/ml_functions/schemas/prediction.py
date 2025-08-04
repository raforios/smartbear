'''
    Prediction Schemas (Request/Response)
'''
from typing import Union, List, Dict, Any
from pydantic import BaseModel, Field

class ComputeCostLinearRequest(BaseModel):
    '''
        Request model for calculating linear regression (multi-feature) cost.
    '''
    x_matrix: List[List[float]] = Field(
        ...,
        description = 'Feature matrix X for multi-feature linear regression cost calculation.'
    )
    y: List[float] = Field(
        ...,
        description = 'Target vector y for multi-feature linear regression cost calculation.'
    )
    w: List[float] = Field(
        ...,
        description = 'Weight parameters w for multi-feature linear regression cost calculation.'
    )
    b: float = Field(
        ...,
        description = 'Bias parameter b for multi-feature linear regression cost calculation.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'x_matrix': [[1.0, 2.0], [3.0, 4.0]],
                    'y': [5.0, 7.0],
                    'w': [1.0, 1.0],
                    'b': 1.0
                }
            ]
        }
    }

class ComputeCostLinearResponse(BaseModel):
    '''
        Response model for linear regression (multi-feature) cost.
    '''
    cost: float = Field(
        ...,
        description = 'Calculated cost for the multi-feature linear regression model.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'cost': 0.0
                }
            ]
        }
    }

class ComputeGradientLinearRequest(BaseModel):
    '''
        Request model for calculating linear regression (multi-feature) gradient.
    '''
    x_matrix: List[List[float]] = Field(
        ...,
        description = 'Feature matrix X for multi-feature linear regression gradient calculation.'
    )
    y: List[float] = Field(
        ...,
        description = 'Target vector y for multi-feature linear regression gradient calculation.'
    )
    w: List[float] = Field(
        ...,
        description = 'Weight parameters w for multi-feature linear regression gradient calculation'
    )
    b: float = Field(
        ...,
        description = 'Bias parameter b for multi-feature linear regression gradient calculation.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'x_matrix': [[1.0, 2.0], [3.0, 4.0]],
                    'y': [5.0, 7.0],
                    'w': [1.0, 1.0],
                    'b': 1.0
                }
            ]
        }
    }

class ComputeGradientLinearResponse(BaseModel):
    '''
        Response model for linear regression (multi-feature) gradient.
    '''
    dj_db: float = Field(
        ...,
        description = 'Gradient of cost with respect to bias (b) for multi-feature model.'
    )
    dj_dw: List[float] = Field(
        ...,
        description = 'Gradient of cost with respect to weights (w) for multi-feature model.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'dj_db': 0.0,
                    'dj_dw': [0.0, 0.0]
                }
            ]
        }
    }

class TrainLinearRegressionRequest(BaseModel):
    '''
        Request model for performing linear regression (multi-feature) training
        (gradient descent).
    '''
    x_matrix: List[List[float]] = Field(
        ...,
        description = 'Feature matrix X for multi-feature linear regression training.'
    )
    y: List[float] = Field(
        ...,
        description = 'Target vector y for multi-feature linear regression training.'
    )
    w_in: List[float] = Field(
        ...,
        description = 'Initial weight parameters w for multi-feature linear regression.'
    )
    b_in: float = Field(
        ...,
        description = 'Initial bias parameter b for multi-feature linear regression.'
    )
    alpha: float = Field(
        ...,
        description = 'Learning rate (alpha) for multi-feature linear regression training.'
    )
    num_iters: int = Field(
        ...,
        description = 'Number of iterations for multi-feature linear regression training.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'x_matrix': [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
                    'y': [3.0, 7.0, 11.0],
                    'w_in': [0.0, 0.0],
                    'b_in': 0.0,
                    'alpha': 0.01,
                    'num_iters': 1000
                }
            ]
        }
    }

class TrainLinearRegressionResponse(BaseModel):
    '''
        Response model for linear regression (multi-feature) training results.
    '''
    w_final: List[float] = Field(
        ...,
        description = 'Final weight parameters w after multi-feature training.'
    )
    b_final: float = Field(
        ...,
        description = 'Final bias parameter b after multi-feature training.'
    )
    J_history: List[float] = Field(
        ...,
        description = 'History of cost function J during multi-feature training.'
    )
    p_history: List[List[Union[List[float], float]]] = Field(
        ...,
        description = 'History of [w_epoch, b_epoch] during multi-feature training.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'w_final': [1.0, 2.0],
                    'b_final': 0.0,
                    'J_history': [10.0, 5.0, 1.0, 0.0],
                    'p_history': [[[0.0, 0.0], 0.0], [[0.5, 1.0], 0.0], [[0.8, 1.5], 0.0]]
                }
            ]
        }
    }

class PredictLinearRequest(BaseModel):
    '''
        Request model for linear regression (multi-feature) prediction.
    '''
    x_test: List[List[float]] = Field(
        ...,
        description = 'Test feature matrix X for multi-feature prediction.'
    )
    w: List[float] = Field(
        ...,
        description = 'Weight parameters w (from trained multi-feature model).'
    )
    b: float = Field(
        ...,
        description = 'Bias parameter b (from trained multi-feature model).'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'x_test': [[7.0, 8.0], [9.0, 10.0]],
                    'w': [1.0, 2.0],
                    'b': 0.0
                }
            ]
        }
    }

class PredictLinearResponse(BaseModel):
    '''
        Response model for linear regression (multi-feature) prediction.
    '''
    predictions: List[float] = Field(
        ...,
        description = 'List of predicted numerical values for new inputs.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'predictions': [23.0, 29.0]
                }
            ]
        }
    }

class ComputeCostSingleLinearRequest(BaseModel):
    '''
        Request model for calculating single-feature linear regression cost.
    '''
    x: List[float] = Field(
        ...,
        description = 'Feature vector x for single-feature linear regression cost calculation.'
    )
    y: List[float] = Field(
        ...,
        description = 'Target vector y for single-feature linear regression cost calculation.'
    )
    w: float = Field(
        ...,
        description = 'Weight parameter w for single-feature linear regression cost calculation.'
    )
    b: float = Field(
        ...,
        description = 'Bias parameter b for single-feature linear regression cost calculation.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'x': [1.0, 2.0, 3.0],
                    'y': [2.0, 4.0, 6.0], # y = 2x
                    'w': 2.0,
                    'b': 0.0
                }
            ]
        }
    }

class ComputeCostSingleLinearResponse(BaseModel):
    '''
        Response model for single-feature linear regression cost.
    '''
    cost: float = Field(
        ...,
        description = 'Calculated cost for the single-feature linear regression model.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'cost': 0.0
                }
            ]
        }
    }

class ComputeGradientSingleLinearRequest(BaseModel):
    '''
        Request model for calculating single-feature linear regression gradient.
    '''
    x: List[float] = Field(
        ...,
        description = 'Feature vector x for single-feature linear regression gradient calculation.'
    )
    y: List[float] = Field(
        ...,
        description = 'Target vector y for single-feature linear regression gradient calculation.'
    )
    w: float = Field(
        ...,
        description = 'Weight parameter w for single-feature linear regression gradient calculation'
    )
    b: float = Field(
        ...,
        description = 'Bias parameter b for single-feature linear regression gradient calculation.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'x': [1.0, 2.0, 3.0],
                    'y': [2.0, 4.0, 6.0],
                    'w': 1.0,
                    'b': 0.0
                }
            ]
        }
    }

class ComputeGradientSingleLinearResponse(BaseModel):
    '''
        Response model for single-feature linear regression gradient.
    '''
    dj_db: float = Field(
        ...,
        description = 'Gradient of cost with respect to bias (b) for single-feature model.'
    )
    dj_dw: float = Field(
        ...,
        description = 'Gradient of cost with respect to weight (w) for single-feature model.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'dj_db': 0.0,
                    'dj_dw': 0.0
                }
            ]
        }
    }

class TrainSingleLinearRegressionRequest(BaseModel):
    '''
        Request model for performing single-feature linear regression training
        (gradient descent).
    '''
    x: List[float] = Field(
        ...,
        description = 'Feature vector x for single-feature linear regression training.'
    )
    y: List[float] = Field(
        ...,
        description = 'Target vector y for single-feature linear regression training.'
    )
    w_in: float = Field(
        ...,
        description = 'Initial weight parameter w for single-feature linear regression.'
    )
    b_in: float = Field(
        ...,
        description = 'Initial bias parameter b for single-feature linear regression.'
    )
    alpha: float = Field(
        ...,
        description = 'Learning rate (alpha) for single-feature linear regression training.'
    )
    num_iters: int = Field(
        ...,
        description = 'Number of iterations for single-feature linear regression training.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'x': [1.0, 2.0, 3.0, 4.0],
                    'y': [3.0, 5.0, 7.0, 9.0], # y = 2x + 1
                    'w_in': 0.0,
                    'b_in': 0.0,
                    'alpha': 0.01,
                    'num_iters': 1000
                }
            ]
        }
    }

class TrainSingleLinearRegressionResponse(BaseModel):
    '''
        Response model for single-feature linear regression training results.
    '''
    w_final: float = Field(
        ...,
        description = 'Final weight parameter w after single-feature training.'
    )
    b_final: float = Field(
        ...,
        description = 'Final bias parameter b after single-feature training.'
    )
    J_history: List[float] = Field(
        ...,
        description = 'History of cost function J during single-feature training.'
    )
    p_history: List[List[float]] = Field(
        ...,
        description = 'History of [w_epoch, b_epoch] during single-feature training.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'w_final': 2.0,
                    'b_final': 1.0,
                    'J_history': [10.0, 5.0, 1.0, 0.0],
                    'p_history': [[0.0, 0.0], [0.5, 0.2], [1.5, 0.8], [2.0, 1.0]]
                }
            ]
        }
    }

class ComputeCostMatrixRequest(BaseModel):
    '''
        Request model for the direct compute_cost_matrix function.
    '''
    x_matrix: List[List[float]] = Field(
        ...,
        description = 'Data, m examples with n features'
    )
    y: List[float] = Field(
        ...,
        description = 'Target values'
    )
    w: List[float] = Field(
        ...,
        description = 'Model parameters w'
    )
    b: float = Field(
        ...,
        description = 'Model parameter b'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'x_matrix': [[1.0, 2.0], [3.0, 4.0]],
                    'y': [5.0, 7.0],
                    'w': [1.0, 1.0],
                    'b': 1.0
                }
            ]
        }
    }

class ComputeCostMatrixResponse(BaseModel):
    '''
        Response model for the direct compute_cost_matrix function.
    '''
    cost: float = Field(
        ...,
        description = 'The cost of using w,b as the parameters for linear regression.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'cost': 0.0
                }
            ]
        }
    }

class ComputeGradientMatrixRequest(BaseModel):
    '''
        Request model for the direct compute_gradient_matrix function.
    '''
    x_matrix: List[List[float]] = Field(
        ...,
        description = 'Matrix of examples (m,n)'
    )
    y: List[float] = Field(
        ...,
        description = 'Target value of each example'
    )
    w: List[float] = Field(
        ...,
        description = 'Parameters of the model w'
    )
    b: float = Field(
        ...,
        description = 'Parameter of the model b'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'x_matrix': [[1.0, 2.0], [3.0, 4.0]],
                    'y': [5.0, 7.0],
                    'w': [1.0, 1.0],
                    'b': 1.0
                }
            ]
        }
    }

class ComputeGradientMatrixResponse(BaseModel):
    '''
        Response model for the direct compute_gradient_matrix function.
    '''
    dj_db: float = Field(
        ...,
        description = 'The gradient of the cost w.r.t. the parameter b.'
    )
    dj_dw: List[float] = Field(
        ...,
        description = 'The gradient of the cost w.r.t. the parameters w.'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'dj_db': 0.0,
                    'dj_dw': [0.0, 0.0]
                }
            ]
        }
    }

class GradientDescentMatrixRequest(BaseModel):
    '''
        Request model for the direct gradient_descent_matrix function.
    '''
    x_matrix: List[List[float]] = Field(
        ...,
        description = 'Data, m examples with n features'
    )
    y: List[float] = Field(
        ...,
        description = 'Target values'
    )
    w_in: List[float] = Field(
        ...,
        description = 'Initial model parameters w'
    )
    b_in: float = Field(
        ...,
        description = 'Initial model parameter b'
    )
    alpha: float = Field(
        ...,
        description = 'Learning rate'
    )
    num_iters: int = Field(
        ...,
        description = 'Number of iterations to run gradient descent'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'x_matrix': [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
                    'y': [3.0, 7.0, 11.0],
                    'w_in': [0.0, 0.0],
                    'b_in': 0.0,
                    'alpha': 0.01,
                    'num_iters': 1000
                }
            ]
        }
    }

class GradientDescentMatrixResponse(BaseModel):
    '''
        Response model for the direct gradient_descent_matrix function.
    '''
    w_final: List[float] = Field(
        ...,
        description = 'Updated values of parameters w after running gradient descent'
    )
    b_final: float = Field(
        ...,
        description = 'Updated value of parameter b after running gradient descent'
    )
    J_history: List[float] = Field(
        ...,
        description = 'History of cost values'
    )
    # Note: 'hist_details' captures all the historical data (cost, w, b, dj_dw, dj_db)
    # as returned by the gradient_descent_matrix function in services/machine_learning.py
    hist_details: Dict[str, Any] = Field(
        ...,
        description = 'Detailed history including costs, parameters, gradients, and iterations'
    )

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'w_final': [1.0, 2.0],
                    'b_final': 0.0,
                    'J_history': [10.0, 5.0, 1.0, 0.0],
                    'hist_details': {
                        'iter': [0, 1, 2],
                        'cost': [10.0, 5.0, 1.0],
                        'w': [[0.0, 0.0], [0.5, 1.0], [0.8, 1.5]],
                        'b': [0.0, 0.0, 0.0],
                        'dj_dw': [[1.0, 1.0], [0.5, 0.5], [0.1, 0.1]],
                        'dj_db': [1.0, 0.5, 0.1]
                    }
                }
            ]
        }
    }
