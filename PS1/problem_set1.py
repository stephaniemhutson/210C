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
T = 500 # time periods

# Note: updated 1 to .999
nus = [ 0.25, 0.5, 0.999, 2, 4]

# exogenous variable: m_hat

# unknowns: consumption, prices, the nominal interest rate

I = sp.sparse.eye(T)
Ip1 = sp.sparse.diags([np.ones(T-1)], [1], (T, T))
Im1 = sp.sparse.diags([np.ones(T-1)], [-1], (T, T))
Z = sp.sparse.csr_matrix((T, T))



# suppose theta = 0.05. Why so small? This means that css is about 1/3, and thus nss is
# about 1/3 which seems empirically reasonable.
theta = 0.05


## Equations ##
"""
market clearing:
y - c = 0


m - p - c + 1/nu * beta/(1-beta)* q = 0
house hold
vphi*n - (w -p) - (nu - gamma)*x + nu*c = 0
(nu - gamma)*x - nu*c + p1 -p - q - (nu - gamma)x1 + nu*c1 = 0
(x - c)*((1-theta * (css**(1-nu))) + (x - m)*(theta * mss**(1-nu)) - theta * p = 0

firm
n = y
p = w

"""

dxdzs = []

def get_blocks(nu):
    css = ((1-theta)/chi)**(1/(vphi + gamma))*((1-theta) + \
        theta*((1-theta)/theta*(1-beta))**((nu-1)/nu))**((nu-gamma)/((1-nu)*(vphi+gamma)))

    # given css, (and pss = 1) we can find mss
    mss = ((1-theta)/theta)**(-1/nu)*css*((beta - 1)/beta)**(-1/nu)

    # given css and mss we can find xss
    xss = ((1-theta)*css**(1-nu) + theta*mss**(1-nu))**(1/(1-nu))

    # variable: m p c q w-p n y x

    # No nu phi vectors
# market clearing block: goods
    phi_gm_m = Z
    phi_gm_p = Z
    phi_gm_c = -I
    phi_gm_q = Z
    phi_gm_w_p = Z
    phi_gm_n = Z
    phi_gm_y = I
    phi_gm_x = Z

    mc_phis = [
        phi_gm_m,
        phi_gm_p,
        phi_gm_c,
        phi_gm_q,
        phi_gm_w_p,
        phi_gm_n,
        phi_gm_y,
        phi_gm_x,
    ]


    # firm block
    phi_f_m = Z
    phi_f_p = Z
    phi_f_c = Z
    phi_f_q = Z
    phi_f_w_p = Z
    phi_f_n = -I
    phi_f_y = I
    phi_f_x = Z

    f_phis = [
        phi_f_m,
        phi_f_p,
        phi_f_c,
        phi_f_q,
        phi_f_w_p,
        phi_f_n,
        phi_f_y,
        phi_f_x,
    ]

    # euler block
    phi_eu_m = Z
    phi_eu_p = Ip1 - I
    phi_eu_c = -nu*I + nu*Ip1
    phi_eu_q = -I
    phi_eu_w_p = Z
    phi_eu_n = Z
    phi_eu_y = Z
    phi_eu_x = (nu - gamma)*I-(nu-gamma)*Ip1

    eu_phis = [
        phi_eu_m,
        phi_eu_p,
        phi_eu_c,
        phi_eu_q,
        phi_eu_w_p,
        phi_eu_n,
        phi_eu_y,
        phi_eu_x,
    ]

    # money trade off
    phi_mc_m = nu* I
    phi_mc_p = -nu * I
    phi_mc_c = -nu * I
    phi_mc_q = (beta/(1-beta))*I
    phi_mc_w_p = Z
    phi_mc_n = Z
    phi_mc_y = Z
    phi_mc_x = Z

    mon_phis = [
        phi_mc_m,
        phi_mc_p,
        phi_mc_c,
        phi_mc_q,
        phi_mc_w_p,
        phi_mc_n,
        phi_mc_y,
        phi_mc_x,
    ]

    # labor leisure
    # vphi*n - (w -p) - (nu - gamma)*x + nu*c = 0
    phi_ll_m = Z
    phi_ll_p = I
    phi_ll_c = nu*I
    phi_ll_q = Z
    phi_ll_w_p = -I
    phi_ll_n = vphi*I
    phi_ll_y = Z
    phi_ll_x = -(nu - gamma)*I

    ll_phis = [
        phi_ll_m,
        phi_ll_p,
        phi_ll_c,
        phi_ll_q,
        phi_ll_w_p,
        phi_ll_n,
        phi_ll_y,
        phi_ll_x,
    ]

    # (x - c)*(1-theta) * (css**(1-nu)) + (x - m)*(theta * mss**(1-nu)) - theta * p = 0
    phi_x_m = -(theta * mss**(1-nu))*I
    phi_x_p = -theta*I
    phi_x_c = -(1-theta) * (css**(1-nu))*I
    phi_x_q = Z
    phi_x_w_p = Z
    phi_x_n = Z
    phi_x_y = Z
    phi_x_x = (1-theta) * (css**(1-nu))*I + theta*mss**(1-nu) * I


    x_phis = [
        phi_x_m,
        phi_x_p,
        phi_x_c,
        phi_x_q,
        phi_x_w_p,
        phi_x_n,
        phi_x_y,
        phi_x_x
    ]

    # dHdY = sp.sparse.bmat([mc_phis, f_phis, eu_phis, mon_phis])
    # assert dHdY.shape == (4*T, 8*T)


    return [
        x_phis,
        mon_phis,
        f_phis,
        eu_phis,
        mc_phis,
        ll_phis,
    ]



for nu in nus:

    (
        x_phis,
        mon_phis,
        f_phis,
        eu_phis,
        mc_phis,
        ll_phis,
    ) = get_blocks(nu)

    # unknowns = [n, p]
    # exogenous = [m]

    # firm_block = sp.sparse.bmat([f_phis])

    # hh_block = sp.sparse.bmat([ll_phis, x_phis])

    # bond_block = sp.sparse.bmat([eu_phis])

    # market_block = sp.sparse.bmat([mc_phis, mon_phis])


    # y = [m, p, c, q]
    # h = [mc mon]


    dHdY = sp.sparse.bmat([
            [mc_phis[0], mc_phis[1], mc_phis[2], mc_phis[3]],
            [mon_phis[0], mon_phis[1], mon_phis[2], mon_phis[3]]
        ])

    dYFdU = sp.sparse.bmat([[f_phis[1], f_phis[6]]])
    dYHdU = sp.sparse.bmat(
        [
            [ll_phis[1], ll_phis[6]],
            [x_phis[1], x_phis[6]],
            [eu_phis[1], eu_phis[6]]
        ])

    dYFdZ = sp.sparse.bmat([[f_phis[0]]])
    dYHdZ = sp.sparse.bmat(
        [
            [ll_phis[0]],
            [x_phis[0]],
            [eu_phis[0]]
        ])

    dYdU = sp.sparse.bmat([[dYFdU],[dYHdU]])
    dYdZ = sp.sparse.bmat([[dYFdZ],[dYHdZ]])

    dHdU = dHdY @ dYdU
    dHdZ = dHdY @ dYdZ


    dUdZ = -sp.sparse.linalg.spsolve(dHdU, dHdZ)
    dYdZ = dYdU @ dUdZ + dYdZ


    dXdZ = sp.sparse.bmat([[dUdZ],
                          [dYdZ]])


    ###########
    #### After I figure out what the things that need to be done will be done...

    dHdU = dHdY @ dYdU

    # compute dHdZ using the chain rule dHdZ = dHdY @ dYdZ (@ is the python matrix multiplication operator)
    dHdZ = dHdY @ dYdZ

    assert sp.sparse.issparse(dHdZ) == True
    assert sp.sparse.issparse(dHdU) == True

    # compute the Jacobian of the model
    dUdZ = - sp.sparse.linalg.spsolve(dHdU, dHdZ)
    dYdZ = dYdU @ dUdZ + dYdZ

    dXdZ = sp.sparse.bmat([[dUdZ],
                          [dYdZ]])

    dxdzs.append(dXdZ)


Xs = []
ones = []
twos = []
threes = []
fours = []
fives = []
sixes = []

colors = ['r', 'b', 'g', 'y', 'k']

shocks = np.random.normal(size=T)

# In class we said that there is only one shock but this really doesn't
# make any sense to me in this context.
ms = []


# plot IRFs to Money supply shock with persistence rho
for i, dXdZ in enumerate(dxdzs):
    m = np.zeros((T, 1))

    m[0] = 1
    for t in range(1, T):
        m[t] = rho_m * m[t-1]
    #
    ms.append(m)

    # compute impulse response functions
    X = dXdZ @ m

    Xs.append(X)

    # To be completely honest, I don't know which set of data is associated with which unknown.

    # subtracting 5 from T and adding 2 to avoid weird edge effects.
    ones.append(X[0+2:T-5])
    twos.append(X[T+2:2*T-10])
    threes.append(X[2*T+2:3*T-5])
    fours.append(X[3*T+2:4*T-5])
    fives.append(X[4*T+2:5*T-5])
    sixes.append(X[5*T+2:6*T-5])

# plot impulse response functions
fig, ax = plt.subplots(2, 4, figsize=(16, 8))


fig.suptitle("Impact of money shock on endogenous variables.")
for i, nu in enumerate(nus):
    ax[0, 0].plot(ms[i], label='m')
    ax[0, 0].set_title('Money Shock')
    ax[0, 1].plot(ones[i], label=nu, color=colors[i])
    ax[0, 1].set_title('First one (Prices?)')
    ax[0, 2].plot(twos[i], label=nu, color=colors[i])
    ax[0, 2].set_title('Second one')

    ax[0,3].set_title("Intentially left blank")

    ax[1, 0].plot(threes[i], label=nu, color=colors[i])
    ax[1, 0].set_title('Thrid one')

    ax[1, 1].plot(fours[i], label=nu, color=colors[i])
    ax[1, 1].set_title('Fourth one')

    ax[1, 2].plot(fives[i], label=nu, color=colors[i])
    ax[1, 2].set_title('Fifth one (Consumption?)')

    ax[1, 3].plot(sixes[i], label=nu, color=colors[i])
    ax[1, 3].set_title('Sixth one')
    ax[1, 3].legend()



# plt.savefig('./PS1/IRFs.png')
plt.show()



