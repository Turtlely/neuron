'''
The neuron cell membrane can be treated as an RC circuit.

System of Differential Equations:
I_ion = g_ion(V) * (E_ion - V)

I_total = I_Na + I_K + I_leak
I_K(V) = g_K n^4 (E_K - V)
I_Na(V) = g_Na hm^3 (E_Na - V)

I_total = g_K n^4 (E_K - V) + g_Na hm^3 (E_Na - V)

CV' = I_total


CV' = g_K n^4 (E_K - V) + g_Na hm^3 (E_Na - V)

n' = a(1-n) - bn
m' = c(1-n) - dn
h' = e(1-n) - fn

'''
import numpy as np
import matplotlib.pyplot as plt

# Parameters
g_K = 36     # Conductance for K+ (mS/cm²)
g_Na = 120   # Conductance for Na+ (mS/cm²)
g_leak = 0.3 # Conductance for leak channels (mS/cm²)
E_K = -77    # Potassium equilibrium potential (mV)
E_Na = 50   # Sodium equilibrium potential (mV)
E_leak = -54.387 # Leak equilibrium potential (mV)
C = 1        # Membrane capacitance (µF/cm²)
V_rest = -65

# Initial Conditions
V = -65  # Membrane potential (in millivolts)
n = 0.317   # Potassium channel activation
m = 0.0529  # Sodium channel activation
h = 0.5961  # Sodium channel inactivation
I_K = g_K * n**4 * (E_K-V)
I_Na = g_Na * m**4 * h * (E_Na-V)
I_leak = g_leak * (E_leak - V)
I_inject = 0

# Simulation parameters
dt=0.01
time=250
steps = int(time/dt)
print(steps)
t = 0
n_t=[]
m_t=[]
h_t=[]
t_t=[]
v_t=[]
i_na_t=[]
i_k_t=[]
i_leak_t=[]
i_inject_t=[]

# Action Potential parameters
pulse_duration = 1 # Duration of current injection (ms)
pulse_magnitude = 25 # Current to inject (mA)
pulse_period = 50 # Period of current injection (ms)


# Rate constants for K+ gates
def a_n(V):
	return 0.01*(V+10)/(np.exp((V+10)/10)-1)
def b_n(V):
	return 0.125*np.exp(V/80)

# Rate constants for Na+ gates
def a_m(V):
	return 0.1*(V+25)/(np.exp((V+25)/10)-1)
def b_m(V):
	return 4*np.exp(V/18)
def a_h(V):
	return 0.07*np.exp(V/20)
def b_h(V):
	return 1/(np.exp((V+30)/10)+1)

# Change in probability that a K+ gate is open over time
def dndt(n, V):
	return a_n(V)*(1-n) - b_n(V)*n

# Change in probability that a Na+ gate is open over time
def dmdt(m, V):
	return a_m(V)*(1-m) - b_m(V)*m
def dhdt(h, V):
	return a_h(V)*(1-h) - b_h(V)*h

# Change in voltage over time
def dvdt():
	return (I_K + I_Na + I_leak + I_inject)/C

'''
print(a_n(0))
print(b_n(0))
print(n)
print(dndt(0,0))
print()

print(a_m(0))
print(b_m(0))
print(m)
print(dmdt(0,0))
print()

print(a_h(0))
print(b_h(0))
print(h)
print(dhdt(0,0))
print()

print(I_K, I_Na, I_leak)
quit()
'''

'''
# Ion currents
I_K = g_K * n**4 * (E_K-V)
I_Na = g_Na * m**4 * h * (E_Na-V)
I_leak = g_leak * (E_leak - V)

dVdt = (I_K + I_Na + I_leak)/C

print(I_K, I_Na, I_leak)
'''

for step in range(steps):
	# Trigger an action potential
	if (step-pulse_period/dt) % (pulse_duration/dt + pulse_period/dt) < pulse_duration/dt:
		I_inject = pulse_magnitude
	else:
		I_inject = 0

	# Calculate new nmh
	n += dndt(n,V_rest-V)*dt
	m += dmdt(m,V_rest-V)*dt
	h += dhdt(h,V_rest-V)*dt

	# Calculate ion currents
	I_K = g_K * n**4 * (E_K-V)
	I_Na = g_Na * m**4 * h * (E_Na-V)
	I_leak = g_leak * (E_leak - V)

	# Update voltage
	V += dvdt()*dt

	# Simulation logging
	t+=dt
	n_t.append(n)
	m_t.append(m)
	h_t.append(h)
	t_t.append(t)
	v_t.append(V)
	i_na_t.append(I_Na)
	i_k_t.append(I_K)
	i_leak_t.append(I_leak)
	i_inject_t.append(I_inject)


# First plot: values of n, m, h over time
plt.figure(figsize=(10, 5))
plt.plot(t_t, n_t, label="n (K+)")
plt.plot(t_t, m_t, label="m (Na+)")
plt.plot(t_t, h_t, label="h (Na+)")
#plt.plot(t_t, np.power(n_t,4), label="K+ Channels")
#plt.plot(t_t, np.power(m_t,3)*np.array(h_t), label="Na+ Channels")

plt.legend()
plt.xlabel("Time (ms)")
plt.ylabel("Proportion of gates open")
plt.title("Ion Channel Gates Over Time")

# Second plot: membrane voltage over time
plt.figure(figsize=(10, 5))
plt.plot(t_t, v_t, label="Membrane Voltage")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Voltage (mV)")
plt.title("Membrane Voltage Over Time")
plt.legend()

# Third plot: membrane currents over time
plt.figure(figsize=(10, 5))
plt.plot(t_t, i_na_t, label="Na+")
plt.plot(t_t, i_k_t, label="K+")
plt.plot(t_t, i_leak_t, label="Leak")
plt.plot(t_t, i_inject_t, label="Injected")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Current (mA)")
plt.title("Membrane Current Over Time")
plt.legend()
plt.show()