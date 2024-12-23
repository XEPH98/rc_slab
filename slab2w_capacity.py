#import
import math
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
bw = 2500         #beam width, mm
h = 125        #beam height, mm
ln = 5400       #beam clear span, mm
print("bw = " + str(bw) + ", h = " + str(h) + ", ln = " + str(ln))
#Tensile Reinforcement Detail
d_main = 12     #diameter of main bars, mm
d_tie = 12      #diameter of tie bars, mm
n_tieleg = 2    #no. of tie legs
s = 200         #spacing of transv. reinf, mm
sc = 25         #steel cover
print(f"rsb dia = {d_main}mm")
#Check for max number of bars in a layer
nbar_bot = round((bw-sc*2-d_tie*2+25)/(25+d_main))       #Check for max number of bars in a layer
print("===== START FLEXURE DESIGN - SRB =====")
print("1. Max number of bars in a layer:", nbar_bot,"pcs")
layer = 1
if layer > 1:
    n1 = int(input("2a. No. of bars in the first layer: "))
    n2 = int(input("2b. No. of bars in the second layer:"))
    As1 = n1*pi*0.25*d_main**2
    As2 = n2*pi*0.25*d_main**2
    As = As1 + As2
    y = (As1*0 + As2*(d_main + 25))/As
    dt = h - sc - d_tie - d_main/2      #reinforcement farthest from the compression face
    d = dt - y                          #centroid of steel
    print("2c. location of reinforcement farthest from comp. face, dt = " + str(dt) + "mm")
else:
    n1 = int(input("2a. No. of bars in the first layer: "))  #number of bottom bars, pcs   
    dt = h - sc - d_tie - d_main/2      #reinforcement farthest from the compression face
    d = dt                              #centroid of steel
    As = round( pi*d_main**2*0.25*n1 ,2 )
    print("2b. location of reinforcement farthest from comp. face, dt = " + str(dt) + "mm")
    print("2c. actual steel area, As = {}mm2".format(As))
s2 = round((bw-sc*2-d_tie*2)/(n1-1))        #spacing of the long reinf., mm
print("3. " + str(n1) + "pcs long bars spaced at " + str(s2) + "mm per layer")
#Beta Factor
if fc <= 28:
    beta1 = 0.85
elif 28 < fc < 55:
    beta1 = round(0.85 - 0.05*(fc-28)/7,4)
else:
    beta1 = 0.65
print("4. beta1 = " + str(beta1))
#Equivalent compression block
a = As*fy/(0.85*fc*bw)
c = a/beta1
#Rho for Balanced Strain Condition
eu = 0.003      #crushing strain of concrete
ety = 0.002      #ACI 21.2.2.1, net tensile strain value in the extreme layer of long ten reinf. if compression controlled
ey = fy/Es     
rho_b = round(0.85*beta1*fc*eu/(fy*(eu+ety)),5)
print("5. Balanced reinforcement ratio: " + str(rho_b))
#Rho for Actual Strain Condition
et = eu*(dt-c)/c    #net tensile strain in extreme layer of long ten reinf.
rho_act = round(0.85*beta1*fc*dt*eu/(fy*d*(eu+et)),5)
print("6. Actual reinforcement ratio: " + str(rho_act))
#Rho for maximum reinforcement ratio for a tension-controlled beam
rho_ten = round(0.85*beta1*fc*eu/(fy*(eu+0.005)),5)
print("7. Maximum reinforcement ratio: " + str(rho_ten))
def phi():
    if et <= ety:
        phi = 0.65
    elif ety < et < 0.005:
        phi = 0.65 + 0.25*(et - ey)/(0.005 - ey)
    else:
        phi = 0.90
    return phi
print("8. Reduction factor for flexure, phi = " + str(phi()))
#Bending Capacity
Mn = 0.85*fc*a*bw*(d-a/2)*(0.001**2)      #Bending Capacity, kN-m
print("9. Nominal moment strength:", round(Mn,2),"kN-m")
print("10. Ultimate moment strength:", round(phi()*Mn,2),"kN-m")