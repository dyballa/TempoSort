import numpy as np 

#ZCA whitening adapted from [https://stackoverflow.com/questions/6574782/how-to-whiten-matrix-in-pca]
def zca_whitening(data):
    """
    Function to whiten the input data using ZCA whitening.
    INPUT:  X: [M x N] matrix.
        Rows: Variables
        Columns: Observations
    OUTPUT: ZCAMatrix: [M x M] matrix
    """
    #Convert to numpy array
    data_matrix = np.array(data)
    # Covariance matrix [column-wise variables]: Sigma = (X-mu)' * (X-mu) / N
    sigma = np.cov(data_matrix, rowvar=True) # [M x M]
    # Singular Value Decomposition. X = U * np.diag(S) * V
    U,S,V = np.linalg.svd(sigma)
        # U: [M x M] eigenvectors of sigma.
        # S: [M x 1] eigenvalues of sigma.
        # V: [M x M] transpose of U
    # Whitening constant: prevents division by zero
    epsilon = 1e-5
    # ZCA Whitening matrix: U * Lambda * U'
    ZCAMatrix = np.dot(U, np.dot(np.diag(1.0/np.sqrt(S + epsilon)), U.T)) # [M x M]
    # Data whitening
    data_white = np.dot(ZCAMatrix, data_matrix) # [M x N]
    return data_white
