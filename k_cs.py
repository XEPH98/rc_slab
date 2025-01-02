from scipy.interpolate import interp1d

def k_eneg_cs(beta_t,a_l2ol1,l2ol1):
    """
    Calculates % of Mo alloted for exterior negative moment for column strip

    Parameters:
    beta_t (float): torsional restraint provided by transv. beams
    a_l2ol1 (float): product of alpha_f and L2/L1
    l2ol1 (float): L2/L1 (specify if LDir(L/W) or SDir(W/L))
    L1 (mm): length of span in direction that moments are being determined, measured c2c of supports
    L2 (mm): length of span in direction perpendicular to L1, c2c of supports
    
    Returns:
    float: Returns % of Mo to be considered as exterior negative moment for column strip
    """
    if beta_t == 0 and a_l2ol1 == 0:
        k_eneg_cs = 1
    elif a_l2ol1 == 0 and beta_t >= 2.5:
        k_eneg_cs = 0.75
    elif a_l2ol1 >= 1 and beta_t == 0:
        k_eneg_cs = 1.0
    else:
        x = [0.50,2.00]
        y = [0.90,0.45]
        f = interp1d(x,y)
        x_interp = l2ol1
        y_interp = f(x_interp)
        k_eneg_cs = round(float(y_interp),2)
    #print(f"k_eneg_cs = {k_eneg_cs} per T8.10.5.2")
    return k_eneg_cs

def k_poss_cs(a_l2ol1,l2ol1):
    """
    Calculates % of Mo alloted for exterior panel positive moment for column strip

    Parameters:
    a_l2ol1 (float): product of alpha_f and L2/L1
    l2ol1 (float): L2/L1
    L1 (mm): length of span in direction that moments are being determined, measured c2c of supports
    L2 (mm): length of span in direction perpendicular to L1, c2c of supports
    
    Returns:
    float: Returns % of Mo alloted for exterior panel positive moment for column strip
    """
    if a_l2ol1 == 0:
        k_poss_cs = 0.60
    else:
        x = [0.50,2.00]
        y = [0.90,0.45]
        f = interp1d(x,y)
        x_interp = l2ol1
        y_interp = f(x_interp)
        k_poss_cs = round(float(y_interp),2)
    #print(f"k_poss_cs = {k_poss_cs} per T8.10.5.5")
    return k_poss_cs

def k_ineg_cs(a_l2ol1,l2ol1):
    """
    Calculates % of Mo alloted for exterior panel interior neg. moment for column strip

    Parameters:
    a_l2ol1 (float): product of alpha_f and L2/L1
    l2ol1 (float): L2/L1
    L1 (mm): length of span in direction that moments are being determined, measured c2c of supports
    L2 (mm): length of span in direction perpendicular to L1, c2c of supports
    
    Returns:
    float: Returns % of Mo alloted for exterior panel interior neg. moment for column strip
    """
    if a_l2ol1 == 0:
        k_ineg_cs = 0.75
    else:
        x = [0.50,2.00]
        y = [0.90,0.45]
        f = interp1d(x,y)
        x_interp = l2ol1
        y_interp = f(x_interp)
        k_ineg_cs = round(float(y_interp),2)
    #print(f"k_ineg_cs = {k_ineg_cs} per T8.10.5.1")
    return k_ineg_cs