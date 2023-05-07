from simple_pid import PID
import matplotlib.pyplot as plt
import numpy as np
setpoint = 5
pid = PID(0, 0, 0, setpoint=setpoint)
#set sample time to 0 to allow us to directly control the update frequency of the PID
pid.sample_time = 0
#p variables to test
pVariables = [5,10,15]
pid.output_limits = (-10, 10)


speed = 0
cycles = 1
control = 0
VERBOSE = False
def update(controlDrive):    
    #acceleration based on driven value. divided by the "time" value of a cycle
    return speed + (controlDrive * 0.2)/1000

# Assume we have a system we want to control in update()
v = update(0)
for pVar in pVariables:
    pid.Kp = pVar
    speed = 0
    cycles = 1
    controlVector = []
    processVariable = []
    while cycles < 10000:
        #only update PID every 150 cycles. This simulates the fact that the PID's update time
        if(cycles % 150 == 0):
            
            if(len(processVariable) > 300):
                # Compute new output from the PID according to the systems previous value 
                # this simulates the idea of a delay between the real system and what the sensors detect
                control = pid(processVariable[-300])
            if(VERBOSE):
                print("New Control: " + str(control))
            
        # Feed the PID output to the system and get its current value
        v = update(control)
        if(VERBOSE):
            print(v)
        speed = v
        processVariable.append(v)
        controlVector.append(control)
        cycles += 1
    plt.plot(processVariable, label="P = " + str(pVar))


    


print("Plotting...")
#plt.plot(controlVector, label="Control Signal")
plt.axhline(setpoint, color = "black", label="Setpoint")

legend = plt.legend(loc=4, shadow=True, fontsize='x-large')
legend.get_frame().set_facecolor('#00FFCC')
legend.get_frame().set_linewidth(3.0)
plt.title("PID P variable comparison", fontsize="x-large")
plt.xlabel("Time", fontsize="x-large")
plt.ylabel("Process Variable", fontsize="x-large")
plt.show()
