'''
Machine Learning functions for linear regression, multiple linear regression and logistic regression
'''
import math
import copy
import numpy as np

# ----------------------------------------------------------------
# LINEAR REGRESSION
# ----------------------------------------------------------------

def compute_cost(x, y, w, b) :
    '''
    Computes the cost function for linear regression.
    Args:
      x (ndarray (m,)): Data, m examples
      y (ndarray (m,)): target values
      w,b (scalar)    : model parameters

    Returns
        total_cost (float): The cost of using w,b as the parameters for linear regression
        to fit the data points in x and y
    '''
    m = x.shape[0]
    cost = 0

    for i in range(m) :
        fwb = w * x[i] + b
        cost += (fwb - y[i]) ** 2

    cost = cost / (2 * m)

    return cost

def compute_gradient(x, y, w, b) :
    '''
    Computes the gradient for linear regression

    Args:
      x (ndarray (m,)): Data, m examples
      y (ndarray (m,)): target values
      w,b (scalar)    : model parameters

    Returns
      dj_dw (scalar): The gradient of the cost w.r.t. the parameters w
      dj_db (scalar): The gradient of the cost w.r.t. the parameter b
    '''
    m = x.shape[0]
    dj_dw = 0
    dj_db = 0
    for i in range(m) :
        f_wb = w * x[i] + b
        dj_dw += (f_wb - y[i]) * x[i]
        dj_db += f_wb - y[i]

    dj_dw = dj_dw / m
    dj_db = dj_db / m

    return dj_dw, dj_db

def gradient_descent(x, y, w_in, b_in, alpha, num_iters):#pylint: disable=R0913 disable=R0917
    '''
    Performs gradient descent to fit w,b. Updates w,b by taking
    num_iters gradient steps with learning rate alpha

    Args:
      x (ndarray (m,))  : Data, m examples
      y (ndarray (m,))  : target values
      w_in,b_in (scalar): initial values of model parameters
      alpha (float):     Learning rate
      num_iters (int):   number of iterations to run gradient descent
      cost_function:     function to call to produce cost
      gradient_function: function to call to produce gradient

    Returns:
      w (scalar): Updated value of parameter after running gradient descent
      b (scalar): Updated value of parameter after running gradient descent
      J_history (List): History of cost values
      p_history (list): History of parameters [w,b]
    '''

    # An array to store cost J and w's at each iteration primarily for graphing later
    j_history = []
    p_history = []
    b = b_in
    w = w_in
    save_interval = np.ceil(num_iters/10000) # prevent resource exhaustion for long runs

    for i in range(num_iters) :
        # Calculate the gradient and update the parameters using gradient_function
        dj_dw, dj_db = compute_gradient(x, y, w , b)

        # Update Parameters using equation (3) above
        b = b - alpha * dj_db
        w = w - alpha * dj_dw

        # Save cost J at each iteration
        if i == 0 or i % save_interval == 0 :
            j_history.append(compute_cost(x, y, w , b))
            p_history.append([w,b])

        # Print cost every at intervals 10 times or as many iterations if < 10
        if i % math.ceil(num_iters / 10) == 0 :
            print(f'Iteration {i: 9d}:',
                  f'Cost {j_history[-1]: 0.2e} ',
                  f'w: {w: 0.3e}, b:{b: 0.2e}',
                  f'dj_dw: {dj_dw: 0.2e}, dj_db: {dj_db: 0.2e}')

        if i == num_iters - 1 :
            print()
            print(f'Final Iteration {i + 1: 9d}:')
            print('---------------------------------------------------' )
            print(f'Cost:  {j_history[-1]: .2e}')
            print(f'w:     {w: .2e}, b:     {b: .2f}')
            print(f'dj_dw: {dj_dw: .2e}, dj_db: {dj_db: .2e}')
            print('---------------------------------------------------' )
            print()

    #return w and J,w history for graphing
    return w, b, j_history, p_history

# ----------------------------------------------------------------
# MULTIPLE LINEAR REGRESSION
# ----------------------------------------------------------------

def predict_dot(x_matrix, w, b):
    '''
    single predict using linear regression
    Args:
      x (ndarray): Shape (n,) example with multiple features
      w (ndarray): Shape (n,) model parameters
      b (scalar):             model parameter

    Returns:
      p (scalar):  prediction
    '''
    p = np.dot(x_matrix, w) + b
    return p

def compute_cost_matrix(x_matrix, y, w, b):
    '''
    compute cost

    Args:
      x_matrix (ndarray (m,n)): Data, m examples with n features
      y (ndarray (m,)) : target values
      w (ndarray (n,)) : model parameters
      b (scalar)       : model parameter
      
    Returns:
      cost (scalar): cost
    '''
    m, _ = x_matrix.shape

    # calculate f_wb for all examples.
    f_wb = x_matrix @ w + b
    # calculate cost
    cost = np.sum((f_wb - y) ** 2) / (2 * m)

    return cost
    # return(np.squeeze(cost))

def compute_gradient_matrix(x_matrix, y, w, b):
    '''
    Computes the gradient for linear regression 

    Args:
      x_matrix : (ndarray Shape (m,n)) matrix of examples 
      y : (ndarray Shape (m,))  target value of each example
      w : (ndarray Shape (n,))  parameters of the model
      b : (scalar)              parameter of the model

    Returns
      dj_dw : (ndarray Shape (n,)) The gradient of the cost w.r.t. the parameters w.
      dj_db : (scalar)             The gradient of the cost w.r.t. the parameter b.
    '''
    m, _ = x_matrix.shape
    f_wb = x_matrix @ w + b
    err = f_wb - y
    dj_dw = (x_matrix.T @ err) / m
    dj_db = np.sum(err) / m

    return dj_db, dj_dw

def gradient_descent_matrix(x_matrix, y, w_in, b_in, alpha, num_iters):#pylint: disable=R0913 disable=R0917
    '''
    Performs batch gradient descent to learn w and b. Updates w and b by taking 
    num_iters gradient steps with learning rate alpha

    Args:
      x_matrix (ndarray (m,n))   : Data, m examples with n features
      y (ndarray (m,))    : target values
      w_in (ndarray (n,)) : initial model parameters  
      b_in (scalar)       : initial model parameter
      cost_function       : function to compute cost
      gradient_function   : function to compute the gradient
      alpha (float)       : Learning rate
      num_iters (int)     : number of iterations to run gradient descent
      
    Returns:
      w (ndarray (n,)) : Updated values of parameters 
      b (scalar)       : Updated value of parameter 
    '''

    # An array to store cost J and w's at each iteration primarily for graphing later
    w = copy.deepcopy(w_in)  #avoid modifying global w within function
    b = b_in
    save_interval = np.ceil(num_iters/10000) # prevent resource exhaustion for long runs
    hist = {
        'cost' : [],
        'params' : [],
        'grads' : [],
        'iter' : []
    }
    for i in range(num_iters):

        # Calculate the gradient and update the parameters
        dj_db, dj_dw = compute_gradient_matrix(x_matrix, y, w, b)

        # Update Parameters using w, b, alpha and gradient
        w = w - alpha * dj_dw
        b = b - alpha * dj_db

        if i == 0 or i % save_interval == 0 :
            hist['cost'].append(compute_cost_matrix(x_matrix, y, w, b))
            hist['params'].append([w, b])
            hist['grads'].append([dj_dw, dj_db])
            hist['iter'].append(i)

        # Print cost every at intervals 10 times or as many iterations if < 10
        if i % math.ceil(num_iters / 10) == 0 :
            print(f'Iteration {i: 9d}:',
                  f'Cost {hist['cost'][-1]: 0.2e}',
                  f'w: {w}',
                  f'b: {b: 0.2e}',
                  f'dj_dw: {dj_dw}',
                  f'dj_db: {dj_db: 0.2e}')

        if i == num_iters - 1 :
            print()
            print(f'Final Iteration {i + 1: 9d}:')
            print('---------------------------------------------------' )
            print(f'Cost:  {hist['cost'][-1]: 0.2e}')
            print(f'w:     {w}')
            print(f'b:     {b: 0.2f}')
            print(f'dj_dw: {dj_dw}')
            print(f'dj_db: {dj_db: 0.2e}')
            print('---------------------------------------------------' )
            print()

    return w, b, hist

# ----------------------------------------------------------------
# z-score normalization
# ----------------------------------------------------------------
def zscore_normalize_features(x_matrix):
    '''
    computes  x_matrix, zcore normalized by column
    
    Args:
      x_matrix (ndarray (m,n))     : input data, m examples, n features
      
    Returns:
      X_norm (ndarray (m,n)): input normalized by column
      mu (ndarray (n,))     : mean of each feature
      sigma (ndarray (n,))  : standard deviation of each feature
    '''

    # find the mean of each column/feature
    mu = np.mean(x_matrix, axis = 0) # mu will have shape (n,)
    # find the standard deviation of each column/feature
    sigma = np.std(x_matrix, axis = 0) # sigma will have shape (n,)
    # element-wise, subtract mu for that column from each example, divide by std for that column
    x_norm = (x_matrix - mu) / sigma

    return (x_norm, mu, sigma)

# ----------------------------------------------------------------
# LOGISTIC REGRESSION
# ----------------------------------------------------------------

def sigmoid(z) :
    '''
    Compute the sigmoid of z

    Args:
        z (ndarray): A scalar, numpy array of any size.

    Returns:
        g (ndarray): sigmoid(z), with the same shape as z

    '''

    z = np.clip(z, -500, 500)
    g = 1 / (1 + np.exp(-z))

    return g

def compute_cost_logistic(x_matrix, y, w, b) :
    '''
    Computes the cost over all examples
    Args:
      x_matrix : (ndarray Shape (m,n)) data, m examples by n features
      y : (ndarray Shape (m,))  target value
      w : (ndarray Shape (n,))  values of parameters of the model
      b : (scalar)              value of bias parameter of the model
      *argv : unused, for compatibility with regularized version below
    Returns:
      total_cost : (scalar) cost
    '''

    m, _ = x_matrix.shape
    cost = 0

    for i in range(m):
        z = np.dot(x_matrix[i], w) + b
        fwb = sigmoid(z)
        cost += -y[i] * np.log(fwb) - (1 - y[i]) * np.log(1 - fwb)

    cost = cost / m

    return cost

def compute_gradient_logistic(x_matrix, y, w, b) :
    '''
    Computes the gradient for logistic regression
    Args:
      x_matrix : (ndarray Shape (m,n)) data, m examples by n features
      y : (ndarray Shape (m,))  target value
      w : (ndarray Shape (n,))  values of parameters of the model
      b : (scalar)              value of bias parameter of the model
      *argv : unused, for compatibility with regularized version below
    Returns
      dj_dw : (ndarray Shape (n,)) The gradient of the cost w.r.t. the parameters w.
      dj_db : (scalar)             The gradient of the cost w.r.t. the parameter b.
    '''
    m, _ = x_matrix.shape
    dj_dw = np.zeros(w.shape)
    dj_db = 0

    z_wb = sigmoid(x_matrix @ w + b)
    err = z_wb - y

    dj_dw = (x_matrix.T @ err) / m
    dj_db = np.sum(err) / m

    return dj_db, dj_dw


def gradient_descent_logistic(x_matrix, y, w_in, b_in, alpha, num_iters):#pylint: disable=R0917 disable=R0913
    '''
    Performs batch gradient descent to learn theta. Updates theta by taking
    num_iters gradient steps with learning rate alpha

    Args:
      x_matrix :    (ndarray Shape (m, n) data, m examples by n features
      y :    (ndarray Shape (m,))  target value
      w_in : (ndarray Shape (n,))  Initial values of parameters of the model
      b_in : (scalar)              Initial value of parameter of the model
      cost_function :              function to compute cost
      gradient_function :          function to compute gradient
      alpha : (float)              Learning rate
      num_iters : (int)            number of iterations to run gradient descent
      lambda_ : (scalar, float)    regularization constant

    Returns:
      w : (ndarray Shape (n,)) Updated values of parameters of the model after
          running gradient descent
      b : (scalar)                Updated value of parameter of the model after
          running gradient descent
    '''

    # number of training examples
    # m = len(x_matrix)

    # An array to store cost J and w's at each iteration primarily for graphing later
    j_history = []
    w_history = []
    save_interval = np.ceil(num_iters/10000) # prevent resource exhaustion for long runs

    for i in range(num_iters) :

        # Calculate the gradient and update the parameters
        dj_db, dj_dw = compute_gradient_logistic(x_matrix, y, w_in, b_in)

        # Update Parameters using w, b, alpha and gradient
        w_in = w_in - alpha * dj_dw
        b_in = b_in - alpha * dj_db

        # Save cost J at each iteration
        if i == 0 or i % save_interval == 0 :
            j_history.append(compute_cost_logistic(x_matrix, y, w_in, b_in))
            w_history.append([w_in])

        # Print cost every at intervals 10 times or as many iterations if < 10
        if i % math.ceil(num_iters / 10) == 0 :
            w_in_print = [f'{x:.2f}' for x in w_in]
            dj_dw_print = [f'{x:.2f}' for x in dj_dw]
            print(f'Iteration {i: 9d}:',
                  f'Cost {j_history[-1]: 0.2f} ',
                  f'w: {w_in_print}, b:{b_in: 0.2f}',
                  f'dj_dw: {dj_dw_print}, dj_db: {dj_db: 0.2f}')

        if i == num_iters - 1 :
            print()
            print(f'Final Iteration {i + 1: 9d}:')
            print('---------------------------------------------------' )
            print(f'Cost:  {j_history[-1]: 0.2f}')
            print(f'w:     {w_in_print}, b:     {b_in: .2f}')
            print(f'dj_dw: {dj_dw_print}, dj_db: {dj_db: .2f}')
            print('---------------------------------------------------' )
            print()

    return w_in, b_in, j_history, w_history

def predict_logistic(x_matrix, w, b) :
    '''
    Predict whether the label is 0 or 1 using learned logistic
    regression parameters w

    Args:
      x_matrix : (ndarray Shape (m,n)) data, m examples by n features
      w : (ndarray Shape (n,))  values of parameters of the model
      b : (scalar)              value of bias parameter of the model

    Returns:
      p : (ndarray (m,)) The predictions for x_matrix using a threshold at 0.5
    '''
    # number of training examples
    m, n = x_matrix.shape
    p = np.zeros(m)

    for i in range(m) :
        z_wb = 0
        # Loop over each feature
        for j in range(n) :
            # Add the corresponding term to z_wb
            z_wb += x_matrix[i, j] * w[j]

        # Add bias term
        z_wb += b

        # Calculate the prediction for this example
        f_wb = sigmoid(z_wb)

        # Apply the threshold
        p[i] = f_wb >= 0.5

    return p









# def predict_single_loop(x, w, b):
#     '''
#     single predict using linear regression

#     Args:
#       x (ndarray): Shape (n,) example with multiple features
#       w (ndarray): Shape (n,) model parameters
#       b (scalar):  model parameter

#     Returns:
#       p (scalar):  prediction
#     '''
#     n = x.shape[0]
#     p = 0
#     for i in range(n):
#         p_i = x[i] * w[i]
#         p = p + p_i
#     p = p + b
#     return p

# def zscore_normalize_features_pol(X, rtn_ms = False):
#     '''
#     returns z-score normalized X by column
#     Args:
#       X : (numpy array (m,n))
#     Returns
#       X_norm: (numpy array (m,n)) input normalized by column
#     '''
#     mu = np.mean(X, axis = 0)
#     sigma = np.std(X, axis = 0)
#     X_norm = (X - mu)/sigma

#     if rtn_ms :
#         return(X_norm, mu, sigma)
#     else:
#         return(X_norm)

# def compute_cost_reg(x_matrix, y, w, b, lambda_ = 1) :
#     '''
#     Computes the cost over all examples
#     Args:
#       x_matrix : (ndarray Shape (m,n)) data, m examples by n features
#       y : (ndarray Shape (m,))  target value
#       w : (ndarray Shape (n,))  values of parameters of the model
#       b : (scalar)              value of bias parameter of the model
#       lambda_ : (scalar, float) Controls amount of regularization
#     Returns:
#       total_cost : (scalar)     cost
#     '''

#     m, n = x_matrix.shape

#     # Calls the compute_cost function that you implemented above
#     cost_without_reg = compute_cost(x_matrix, y, w, b)

#     # You need to calculate this value
#     reg_cost = 0

#     for j in range(n) :
#         reg_cost_j = w[j] ** 2
#         reg_cost = reg_cost + reg_cost_j

#     reg_cost = (lambda_/(2 * m)) * reg_cost

#     total_cost = cost_without_reg + reg_cost

#     return total_cost

# def compute_gradient_reg(x_matrix, y, w, b, lambda_ = 1) :
#     '''
#     Computes the gradient for logistic regression with regularization

#     Args:
#       x_matrix : (ndarray Shape (m,n)) data, m examples by n features
#       y : (ndarray Shape (m,))  target value
#       w : (ndarray Shape (n,))  values of parameters of the model
#       b : (scalar)              value of bias parameter of the model
#       lambda_ : (scalar,float)  regularization constant
#     Returns
#       dj_db : (scalar)             The gradient of the cost w.r.t. the parameter b.
#       dj_dw : (ndarray Shape (n,)) The gradient of the cost w.r.t. the parameters w.

#     '''
#     m, n = x_matrix.shape

#     dj_db, dj_dw = compute_gradient(x_matrix, y, w, b)

#     for j in range(n) :

#         dj_dw_j_reg = (lambda_ / m) * w[j]

#         # Add the regularization term  to the correspoding element of dj_dw
#         dj_dw[j] = dj_dw[j] + dj_dw_j_reg

#     return dj_db, dj_dw
