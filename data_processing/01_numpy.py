import numpy as np

arr= np.array([1,2,3,4,5])  # 1-D
arr = np.array([[1,2,3,4,5],[6,7,8,9,10]])  # 2-D
print(arr)


# Properties
print(arr.shape)
print(arr.ndim)

# Generating Special Arrays
print(np.ones((2,3)))
print(np.full((2,3),8))

# NumPy Operations

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(A+2)
print(A*5)

print(A+B)
print(A-B)
print(A@B)
print(A.T)

print(np.mean(arr))
print(np.median(arr))
print(np.std(arr))
print(np.sum(arr))
print(np.min(arr))
print(np.max(arr))

# Indexing and Slicing
print(arr[1:3]) 1-D
print(arr[-4:-2])

print(arr[0:1,2:4]) # 2-D first para for rwo and second for column

# random generattion
print(np.random.rand(3,3)) # return 3*3 & 0 decimal
print(np.random.randint(1,100,(3,3)))

# Analyzing Student Scores
score = np.random.randint(50,100,(10,5))
print(score)
print(np.mean(score,axis=1))
