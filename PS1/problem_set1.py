# Problem set 1
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

# problem g

# globals
gamma = 1
vphi = 1
chi = 1
beta = 0.99
rho_m = 0.99
p_star = 1
a = 1
T = 100 # time periods

# Note: updated 1 to .999
nus = [ 0.25, 0.5, 0.999, 2, 4]

# exogenous variable: m_hat

# unknowns: consumption, prices, the nominal interest rate

I = sp.sparse.eye(T)
Ip1 = sp.sparse.diags([np.ones(T-1)], [1], (T, T))
Im1 = sp.sparse.diags([np.ones(T-1)], [-1], (T, T))
Z = sp.sparse.csr_matrix((T, T))



# suppose theta = 0.05

theta = 0.05

# No nu phi vectors
# market clearing block: goods
phi_gm_m = Z
phi_gm_p = Z
phi_gm_c = I
phi_gm_q = Z
phi_gm_w = Z
phi_gm_n = Z
phi_gm_y = I
phi_gm_x = Z

mc_phis = [
    phi_gm_m,
    phi_gm_p,
    phi_gm_c,
    phi_gm_q,
    phi_gm_w,
    phi_gm_n,
    phi_gm_y,
    phi_gm_x,
]

# firm block
phi_f_m = Z
phi_f_p = Z
phi_f_c = Z
phi_f_q = Z
phi_f_w = Z
phi_f_n = -I
phi_f_y = I
phi_f_x = Z

f_phis = [
    phi_f_m,
    phi_f_p,
    phi_f_c,
    phi_f_q,
    phi_f_w,
    phi_f_n,
    phi_f_y,
    phi_f_x,
]


for nu in nus:
    css = ((1-theta)/chi)**(1/(vphi + gamma))*((1-theta) + \
        theta*((1-theta)/theta*(1-beta))**((nu-1)/nu))**((nu-gamma)/((1-nu)*(vphi+gamma)))

    # given css, (and pss = 1) we can find mss
    mss = ((1-theta)/theta)**(-1/nu)*css*((beta - 1)/beta)**(-1/nu)

    # given css and mss we can find xss
    xss = ((1-theta)*css**(1-nu) + theta*mss**(1-nu))**(1/(1-nu))


    # variable: m p c q w n y x

    # euler block
    phi_eu_m = Z
    phi_eu_p = Ip1 - I
    phi_eu_c = -nu*I + nu*Ip1
    phi_eu_q = -I
    phi_eu_w = Z
    phi_eu_n = Z
    phi_eu_y = Z
    phi_eu_x = (nu - gamma)*I-(nu-gamma)*Ip1

    eu_phis = [
        phi_eu_m,
        phi_eu_p,
        phi_eu_c,
        phi_eu_q,
        phi_eu_w,
        phi_eu_n,
        phi_eu_y,
        phi_eu_x,
    ]

    # money trade off
    phi_mc_m = nu* I
    phi_mc_p = -nu * I
    phi_mc_c = -nu * I
    phi_mc_q = (beta/(1-beta))*I
    phi_mc_w = Z
    phi_mc_n = Z
    phi_mc_y = Z
    phi_mc_x = Z

    mon_phis = [
        phi_mc_m,
        phi_mc_p,
        phi_mc_c,
        phi_mc_q,
        phi_mc_w,
        phi_mc_n,
        phi_mc_y,
        phi_mc_x,
    ]


    dHdY = sp.sparse.bmat([mc_phis, f_phis, eu_phis, mon_phis])
    assert dHdY.shape == (4*T, 8*T)



###########
#### After I figure out what the things that need to be done will be done...

dHdU = dHdY @ dYdU

# compute dHdZ using the chain rule dHdZ = dHdY @ dYdZ (@ is the python matrix multiplication operator)
dHdZ = dHdY @ dYdZ

assert sp.sparse.issparse(dHdZ) == True
assert sp.sparse.issparse(dHdU) == True

assert dHdU.shape == (2*T, 2*T)
assert dHdZ.shape == (2*T, T)

# compute the Jacobian of the model
dUdZ = - sp.sparse.linalg.spsolve(dHdU, dHdZ)
dYdZ = dYdU @ dUdZ + dYdZ

dXdZ = sp.sparse.bmat([[dUdZ],
                      [dYdZ]])

assert dUdZ.shape == (2*T, T)
assert dYdZ.shape == (5*T, T)
assert dXdZ.shape == (7*T, T)


# plot IRFs to Money supply shock with persistence rho

shocks = np.random.normal(size=T)

m = np.zeros((T, 1))
m[0] = 1
for t in range(1, T):
    m[t] = rho_m * m[t-1] + shocks(t)

# compute impulse response functions
X = dXdZ @ a

# unpack X into its components k,n,c,inv,y,wp,rk
k = X[0:T]
n = X[T:2*T]
c = X[2*T:3*T]
inv = X[3*T:4*T]
y = X[4*T:5*T]
wp = X[5*T:6*T]
rk = X[6*T:7*T]

# plot impulse response functions
fig, ax = plt.subplots(4, 2, figsize=(12, 10))
ax[0, 0].plot(a, label='a')
ax[0, 0].set_title('Technology Shock')
ax[0, 1].plot(k, label='k')
ax[0, 1].set_title('Capital')
ax[1, 0].plot(n, label='n')
ax[1, 0].set_title('Labor')
ax[1, 1].plot(c, label='c')
ax[1, 1].set_title('Consumption')
ax[2, 0].plot(inv, label='inv')
ax[2, 0].set_title('Investment')
ax[2, 1].plot(y, label='y')
ax[2, 1].set_title('Output')
ax[3, 0].plot(rk, label='rk')
ax[3, 0].set_title('Return to Capital')
ax[3, 1].plot(wp, label='wp')
ax[3, 1].set_title('Real Wage')
plt.savefig('IRFs.png')



