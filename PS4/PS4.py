import numpy as np
import matplotlib.pyplot as plt

# globals

beta = 0.99
sigma = 1
kappa = 0.1
rho = 0.8
phi_pi = 1.5

# We dont know what varphi and gamma are here...
varphi = 0.5
gamma = 1
v = 0

T = 25


psi_ya = (kappa *(1+varphi)*(1-beta*rho)*(sigma*phi_pi + rho))/((gamma + varphi)*(1-beta*rho)*(rho -1) - kappa*(sigma *phi_pi + rho))
psi_pia = (kappa*(1+varphi)*(1-beta*rho)*(rho-1))/((gamma + varphi)*(1-beta*rho)*(rho -1) - kappa*(sigma *phi_pi + rho))

def y_hat(a):
    return psi_ya * a

def pi_hat(a):
    return psi_pia * a

def y_flex(a):
    return (1 + varphi)* a/(gamma + varphi)

def i_hat(a):
    return phi_pi * pi_hat(a) + v

def a_hat_t(t):
    return rho**t

def a_hat_plus(a):
    return a * rho

def r_hat(i, a):
    return i - pi_hat(a_hat_plus(a))

def n_hat(y, a):
    return y - a


a_s = []
y_hats = []
i_hats = []
pi_hats = []
y_flexes = []
time = []
diff_ys = []
r_hats = []
n_hats = []

# kappa = (lambda (gamma + varphi))

# lambda = (1 - theta)*(1-beta*theta)/theta
# but theta isn't defined here.

for t in range(T):
    time.append(t)
    a = a_hat_t(t)
    a_s.append(a)

    pi_h = pi_hat(a)
    pi_hats.append(pi_h)

    i_h = i_hat(a)

    i_hats.append(i_h)

    y_h = y_hat(a)
    y_f = y_flex(a)

    y_hats.append(y_h)
    y_flexes.append(y_f)
    diff_ys.append(y_h - y_f)
    r_hats.append(r_hat(i_h, a))
    n_hats.append(n_hat(y_h, a))

fig, ax = plt.subplots(3, 3, figsize=(16, 8))

ax[0,0].plot(time, a_s)
ax[0,0].set_title("A")
ax[0,1].plot(time, y_hats)
ax[0,1].set_title("y_hat")
ax[1,0].plot(time, pi_hats)
ax[1,0].set_title("pi")
ax[1,1].plot(time, i_hats)
ax[1,1].set_title("I")
ax[0,2].plot(time, y_flexes)
ax[0,2].set_title("y_flex")

ax[1,2].plot(time, diff_ys)
ax[1,2].set_title("y_hat - y_flex")
ax[2,0].plot(time, r_hats)
ax[2,0].set_title("r")
ax[2,1].plot(time, n_hats)
ax[2,1].set_title("n")

plt.show()



