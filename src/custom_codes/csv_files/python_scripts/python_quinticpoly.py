import numpy as np
import matplotlib.pyplot as plt

'''
%% q0 = initial position
%% v0 = initial velocity
%% q1 = final position
%% v1 = final velocity
%% t0 = initial time
%% tf = final time

'''

q0, v0, ac0 = 0, 0, 0
q1, v1, ac1 = 20, 0, 0
t0 = 0
tf = 1

t = np.linspace(t0, tf, 100*(tf-t0))
c = np.ones(np.size(t))

M = np.matrix([[1, t0, t0**2,   t0**3,   t0**4,    t0**5],
               [0,  1,  2*t0, 3*t0**2, 4*t0**3,  5*t0**4],
               [0,  0,     2,    6*t0,12*t0**2, 20*t0**3],
               [1, tf, tf**2,   tf**3,   tf**4,    tf**5],
               [0,  1,  2*tf, 3*tf**2, 4*tf**3,  5*tf**4],
               [0,  0,     2,    6*tf,12*tf**2, 20*tf**3]])

print(M)

b = np.array([[q0, v0, ac0, q1, v1, ac1]])
b = np.transpose(b)

a = np.linalg.inv(M)*b
print(a)

'''
% qd = reference position trajectory
% vd = reference velocity trajectory
% ad = reference acceleration trajectory
'''
qd = a[0] * c + a[1]*t + a[2]*t**2 + a[3]*t**3 + a[4]*t**4 + a[5]*t**5
vd = a[1] * c + 2*a[2]*t + 3*a[3]*t**2 + 4*a[4]*t**3 + 5*a[5]*t**4
ad = 2*a[2] * c + 6 * a[3] * t + 12*a[4]*t**2 + 20*a[5]*t**3

# plt.plot(t, qd, label='Cubic Spline')
f, (ax1, ax2, ax3) = plt.subplots(1, 3)
ax1.plot(t, np.transpose(qd), label='Position')
ax2.plot(t, np.transpose(vd), label='Velocity')
ax3.plot(t, np.transpose(ad), label='Acceleration')

ax1.legend(loc='upper right')
ax2.legend(loc='upper right')
ax3.legend(loc='upper right')
plt.show()
