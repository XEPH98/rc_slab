#Temperature and Shrinkage
print("""
      References:
      1. ACI318M-14
      2. Design of Concrete Structures, (Darwin-Nelson), 15th Ed.
            Chapter 12, Analysis and Design of One-Way Slabs
      """)

print("=== TEMP & SHRINK BARS (24.4.3.2-3)===")
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
    rho_min = 0.002
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
    return rho_min, spacing_max

tempBars(100,1000,0.003,200)