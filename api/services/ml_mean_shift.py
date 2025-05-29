'''
    ML Mean Shift Algorithm
'''
import numpy as np

# ----------------------------------------------------------------
# Euclidean distance function
# ----------------------------------------------------------------
def euclidean_distance(x, center) -> float:
    ''' 
        Euclidean distance between two points
    '''
    return np.sqrt(np.sum((x - center) ** 2))

# ----------------------------------------------------------------
# Gaussian kernel function
# ----------------------------------------------------------------
def gaussian_kernel(distance, epsilon) -> float:
    ''' 
        Gaussian kernel function
    '''
    return (1/(epsilon * np.sqrt(2 * np.pi)))  * np.exp(-0.5 * np.sum((distance/epsilon) ** 2))


# ----------------------------------------------------------------
# Neighborhood function
# ----------------------------------------------------------------
def neighborhood(x_matrix, x_center, epsilon) -> list:
    ''' 
        Neighborhood function
    '''
    in_neighborhood = []

    for x in x_matrix :
        distance = euclidean_distance(x, x_center)

        if distance <= epsilon :
            in_neighborhood.append(x)

    return in_neighborhood

# ----------------------------------------------------------------

class MeanShift():
    ''' 
        Mean shift algorithm
    '''
    def __init__(self, epsilon, iterations = 100) :
        self.epsilon = epsilon
        self.iterations = iterations
        self.centers = []

    def fit(self, x_matrix) :
        ''' 
            Fit the model
        '''
        fit_matrix = np.copy(x_matrix)

        for _ in range(self.iterations) :
            for i, x in enumerate(fit_matrix) :
                neighbors = neighborhood(fit_matrix, x, self.epsilon)

                m_num = 0
                m_den = 0

                for neighbor in neighbors :
                    distance = euclidean_distance(neighbor, fit_matrix[i])
                    weight = gaussian_kernel(distance, self.epsilon)
                    m_num += (weight * neighbor)
                    m_den += weight

                fit_matrix[i] = m_num / m_den

        self.centers = np.copy(fit_matrix)

    def predict(self, x_matrix) :
        ''' 
            Predict labels for the input data
        '''
        labels = []

        for x in x_matrix :
            distances = [euclidean_distance(x, center) for center in self.centers]
            labels.append(np.argmin(distances))

        return labels
