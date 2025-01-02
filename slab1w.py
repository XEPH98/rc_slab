
#math operations
import math
pi = math.pi
def rd(x):
    return round(x,2)
def roundup(x):
    return math.ceil(x)

#conversions
def mm_to_in(x):
    return round(x/25.4,2)
def kPa_to_psf(x):
    return round(x*144/6.89655172413793,2)
def psf_to_kPa(x):
    return round(x*6.89655172413793/144,2)
def kNm_to_kipft(x):
    """
    Output:
    Converts kN-m to kip-ft
    """
    return rd(x/1.35582)
def kipft_to_kNm(x):
    """
    Output:
    Converts kip-ft to kN-m
    """
    return rd(x*1.35582)

print("""
      References:
      1. ACI318M-14
      2. Design of Concrete Structures, (Darwin-Nelson), 15th Ed.
            Chapter 12, Analysis and Design of One-Way Slabs
      """)

print("=== ANALYSIS PROCEDURE (6.6.2.3)===")
print("> Span lt 3m, may use kinfe edge support analysis.")

class Slab:
    def __init__ (self, name, L, W, thk):
        self.name = name
        self.L = L #The larger dimension
        self.W = W 
        self.thk = thk
    def Ics(self):
        return self.W*self.thk**3/12

S1 = Slab("S1",2000,1000,125)
print(f"Initial Slab Geometric Properties\n L = {S1.L}mm, W = {S1.W}mm, thk = {S1.thk}mm.")
beta = S1.L / S1.W #Ratio of longer to shorter slab dim
print(f"Ratio of longer to shorter slab clear span: {rd(beta)}")

#Geometry & material properties
fc = 27 #MPa
fy = 230 #MPa
Es = 200000 #MPa

#Tensile Reinforcement Detail
d_main = 12     #diameter of main bars, mm
d_tie = 12      #diameter of tie bars, mm
n_tieleg = 2    #no. of tie legs
sc = 25         #steel cover

#Applied Loads
DL = rd(24*S1.thk*.001 + 2.1) #selfweight of slab, kPa
LL = 4.0 #kPa
qa = DL + LL #kPa
qu = 1.2*DL + 1.6*LL #kPa 
Mu = rd(qu*(S1.L*0.001)**2 / 8) #kN-m

print(f"1. DL = {DL}kPa ({kPa_to_psf(DL)}psf) | LL = {LL}kPa ({kPa_to_psf(LL)}psf)")
print(f"2. Service Uniform Pressure, qa = {rd(qa)}kPa ({kPa_to_psf(qa)}psf)")
print(f"3. Factored Uniform Pressure, qu = {rd(qu)}kPa ({kPa_to_psf(qu)}psf)") #kPa
print(f"4. Mu = {Mu}kN-m")

def minThk(slab_type:int,clr_span:int,fy:int):
    """
    Parameters:
    slab_type (none): [1] simply supported [2] one-end cont. [3] cantilever
    clr_span (mm): span of oneWaySlab.
    fy (MPa): yield strength of flexural reinforcement
    Output:
    Prints minimum thickness of slab per code.
    0: rho_min
    1: Chec
    """
    print("=== MIN. THICKNESS (7.3.1)===")
    if slab_type == 1:
        stype = "Simply Supported"
        thk_min = rd((clr_span/20)*(0.40+fy/700)) #mm
    elif slab_type == 2:
        stype = "One-end Continuous"
        thk_min = rd((clr_span/24)*(0.40+fy/700)) #mm
    else:
        stype = "Cantilever"
        thk_min = rd((clr_span/10)*(0.40+fy/700)) #mm

    print(f"1. Slab Type = {stype}")
    print(f"2. Min. Slab Thk = {thk_min}mm")
    if thk_min < S1.thk:
        print(f"3. h ({S1.thk}mm) > minThk ({thk_min}mm). OKAY!")
    else:
        exit(f"3. [h = {S1.thk}mm] vs [minThk = {thk_min}mm]. NOT OKAY!")
    return stype, thk_min

def tempBars(ht:int,bw:int,rho_act:float,spacing):
    """
    Parameters:
    ht (mm): height of beam/slab.
    bw (mm): width of beam/slab.
    rho_act (unitless): reinforcement ratio (bw*d)
    spacing (mm): bar spacing.
    Output:
    Prints rho_min vs. rho_act and bar spacing compliance.
    0: rho_min
    1: Check bar spacing max.
    """
    print("=== TEMP & SHRINK BARS (24.4.3.2-3)===")
    rho_min = 0.002
    d_tns = 10 #mm, dia of temp&shrnk bars
    if rho_min < rho_act:
        print(f"1a. rho_act > rho_min | {rho_act} > {rho_min}")
        print("1b. rho_act above minimum. OKAY!")
    else:
        print(f"1a. rho_act < rho_min | {rho_act} < {rho_min}")
        exit("1b. rho_act below minimum. UNSAFE!")
    
    spacing_max = int(round(5*ht,0))
    if spacing < spacing_max:
        print(f"2. bar spacing ({spacing}) < max spacing ({spacing_max}). OKAY")
    else:
        print(f"2a. spacing > spacing_max ({spacing} > {spacing_max})")
        exit("2b. Change bar diameter to comply with max. allowed spacing.") 
    
    As_tns = 0.002*ht*bw #mm2, steel area for temp&shrnk bars
    A1_tns = pi*0.25*d_tns**2 #mm2, area of 1 tns bar
    n_tns = roundup(As_tns / A1_tns)
    s_tns = roundup(1000/(n_tns))
    print(f"3. Use temperature bars {d_tns}mm dia spcd@{s_tns}mm")
    return rho_min, spacing_max, d_tns, s_tns

def MomentCap(bw,h,layer, n1, n2, Mu):
    print("=== DESIGN FOR FLEXURE ===")
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
        print(f"5. phiMn = {phiMn}kNm ({kNm_to_kipft(phiMn)}kipft) > Mu = {Mu}kNm ({kNm_to_kipft(Mu)}kipft). SAFE!")
        #Check for rho_min
        if 0.002 < rho_act: #rho_min = 0.002
            pass
        else:
            exit("NON COMPLIANT WITH RHO_MIN (0.002)")
        #Check for max spacing
        if s2 < int(min(5*h,450)): #max spacing per  24.4.3.2-3
            pass
        else:
            exit("NON COMPLIANT WITH MAX SPACING (5*h, 450)")
    else:
        print(f"5. phiMn = {phiMn}kNm ({kNm_to_kipft(phiMn)}kipft) < Mu = {Mu}kNm ({kNm_to_kipft(Mu)}kipft). UNSAFE!")
        exit("***** PROGRAM TERMINATED *****")
    return Mn, phiMn, d, s2, n1, n2, layer, rho_act

S1_cap = MomentCap(S1.W,S1.thk,1,5,0,Mu)
S1_temp = tempBars(S1.thk,S1.W,S1_cap[7],S1_cap[3])
S1_minThk = minThk(1,S1.L,fy)

print("=== SUMMARY ===")
print(f"Design of 1Way Slab for max span: {S1.L}mm")
print(f"Governing Slab Thickness: {S1.thk}mm")
print(f"Main reinf. bars: {d_main}mm dia., spaced at {S1_cap[3]}mm")
print(f"Temp. bars: {S1_temp[2]}mm dia., spaced at {S1_temp[3]}mm")