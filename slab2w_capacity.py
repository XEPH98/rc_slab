#import
import math
import slab2w_capacity
pi = math.pi
def sqrt(x):
    return math.sqrt(x)
def rd(x):
    return round(x,2)

#Material Properties
fc = 27       #concrete compressive strength, MPa
fy = 230        #steel yield strength, MPa
fyt = 230       #steel yield strength of ties, MPa
Es = 200000     #Steel Elasticity, GPa
print(f"==== MATERIAL PROPERTIES ====\nfc = {fc}MPa, fy = {fy}MPa, fyt = {fyt}MPa, ")

#Geometry
print("===== BEAM INFO =====")
beam_name = "S1"
bw = 2800      #beam width, mm
h = 175        #beam height, mm
ln = 5400       #beam clear span, mm
print("bw = " + str(bw) + ", h = " + str(h) + ", ln = " + str(ln))

#Tensile Reinforcement Detail
d_main = 12     #diameter of main bars, mm
d_tie = 12      #diameter of tie bars, mm
n_tieleg = 2    #no. of tie legs
s = 200         #spacing of transv. reinf, mm
sc = 25         #steel cover

#Check for max number of bars in a layer
nbar_bot = round((bw-sc*2-d_tie*2+25)/(25+d_main))       #Check for max number of bars in a layer

def MomentCap(bw,layer, n1, n2, Mu):
    if layer > 1:
        As1 = n1*pi*0.25*d_main**2
        As2 = n2*pi*0.25*d_main**2
        As = rd(As1 + As2)
        y = (As1*0 + As2*(d_main + 25))/As
        dt = h - sc - d_tie - d_main/2      #reinforcement farthest from the compression face
        d = rd(dt - y)                          #centroid of steel
        print(f"1. dmain = {d_main} | n1 = {n1}pcs, n2 = {n2}pcs | d = {d}mm")
    else:
        dt = h - sc - d_tie - d_main/2      #reinforcement farthest from the compression face
        d = dt                              #centroid of steel
        As = rd( pi*d_main**2*0.25*n1 )
        print(f"1. dmain = {d_main} | n = {n1}pcs | dt = {dt}mm")
    
    s2 = round((bw-sc*2-d_tie*2)/(n1-1))        #spacing of the long reinf., mm
    print(f"2. As = {As}mm2 | spacing (mainbar) = {s2}mm.")
    #Beta Factor
    if fc <= 28:
        beta1 = 0.85
    elif 28 < fc < 55:
        beta1 = round(0.85 - 0.05*(fc-28)/7,4)
    else:
        beta1 = 0.65
    #Equivalent compression block
    a = As*fy/(0.85*fc*bw)
    c = a/beta1
    #Rho for Balanced Strain Condition
    eu = 0.003      #crushing strain of concrete
    ety = 0.002      #ACI 21.2.2.1, net tensile strain value in the extreme layer of long ten reinf. if compression controlled
    ey = fy/Es     
    rho_b = round(0.85*beta1*fc*eu/(fy*(eu+ety)),5)
    #Rho for Actual Strain Condition
    et = eu*(dt-c)/c    #net tensile strain in extreme layer of long ten reinf.
    rho_act = round(0.85*beta1*fc*dt*eu/(fy*d*(eu+et)),5)
    #Rho for maximum reinforcement ratio for a tension-controlled beam
    rho_ten = round(0.85*beta1*fc*eu/(fy*(eu+0.005)),5)
    print(f"3. rho_bal: {rho_b} | rho_act: {rho_act} | rho_ten: {rho_ten}")
    def phi():
        if et <= ety:
            phi = 0.65
        elif ety < et < 0.005:
            phi = 0.65 + 0.25*(et - ey)/(0.005 - ey)
        else:
            phi = 0.90
        return phi
    print(f"4. phi_flex = {phi()} | beta1 = {beta1}")
    #Bending Capacity
    Mn = rd(0.85*fc*a*bw*(d-a/2)*(0.001**2))      #Bending Capacity, kN-m
    phiMn = rd(phi()*Mn) #kN-m
    if phiMn > Mu:
        print(f"5. phiMn = {phiMn}kN-m > Mu = {Mu}kN-m. SAFE!")
    else:
        print(f"5. phiMn = {phiMn}kN-m < Mu = {Mu}kN-m. UNSAFE!")
        exit("***** PROGRAM TERMINATED *****")
    return Mn, phiMn, d, s2, n1, n2, layer


