import numpy as np
import multiprocessing as mp

## 
def make_func_chunk(vec, func):
    """
    Return a function that takes a vector of arguments and applies the given function to each of them.
    
    Parameters
    ----------
    vec : iterable
        Vector of arguments to be passed to the function.
    func : callable
        Function to be applied to each of the arguments in vec.
    
    Returns
    -------
    func_chunk : callable
        A function that takes a vector of arguments and applies func to each of them.
    """
    def func_chunk(vec):
        return(list(map(func, vec)))

    return(func_chunk)


def par_chunks(func, data, n_chunks=False):
    """
    Parallelize a function by splitting the data into chunks and processing each chunk in a separate process.

    Parameters
    ----------
    func : callable
        The function to be parallelized. It should take a single argument and return a single value.
    data : iterable
        The data to be processed. It should be iterable and can be split into chunks (a list or a numpy array).
    n_chunks : int
        The number of chunks to split the data into. If not specified, the number of chunks is set to the number of cores.

    Returns
    -------
    result : list
        The result of the function applied to each element of data.
    """

    ## set the chunk size to number of cores if not specified
    n_chunks = n_chunks if n_chunks else mp.cpu_count()
    # print(n_chunks)

    ## split the data into chunks
    chunks = np.array_split(data, n_chunks)
    # print(chunks)

    func_chunk = make_func_chunk(chunks, func)
    # print(func_chunk(chunks[1]))

    ## parallelize the loop
    with mp.Pool(n_chunks) as p:
        result = p.map(func, chunks)

    return np.concatenate(result)


if __name__ == '__main__':
    # example function
    def func_sqr(x):
        return(x**2)

    def func_sum(x):
        return(sum(x))
    
    result = par_chunks(func_sqr, range(11), 3)
    print(result)
    