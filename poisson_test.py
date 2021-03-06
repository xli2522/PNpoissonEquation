from fenics import *

# Create mesh and define function space
mesh = UnitSquareMesh(8, 8)
V = FunctionSpace(mesh, 'P', 1)

#define the boundary condition X_D
X_D = Expression('boundary_condition', degree=?)
def boundary(x, on_boundary):
    return on_boundary

bc = DirichletBC(V, X_D, boundary)

#Define variational problem
X = TrialFunction(V)
v = TestFunction(V)
#f the source term
f = Expression('-2*(G*M)/(2*((epsilon**2+abs(x[0]-x1)**2)**delta)*delta)', 
    degree=2, G = 6.674*10**(-11), M = 2*10**30, epsilon = 0.001, delta = 0.002) 

#define the variation problem
a = dot(grad(X), grad(v))*dx
L = f*v*dx

#compute solution
X = Function(V)
solve(a==L, X, bc)

#plot solution
X.rename('X', 'solution')
plot(X)
plot(mesh)

#save VTK
vtkfile = File('poisson/solution.pvd')
vtkfile << X

# Compute error in L2 norm
error_L2 = errornorm(X_D, X, 'L2')

# Compute maximum error at vertices
vertex_values_X_D = X_D.compute_vertex_values(mesh)
vertex_values_X = X.compute_vertex_values(mesh)
import numpy as np
error_max = np.max(np.abs(vertex_values_X_D - vertex_values_X))

# Print errors
print('error_L2  =', error_L2)
print('error_max =', error_max)