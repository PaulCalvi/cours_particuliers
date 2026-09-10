#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:01:54 2020

@author: paulcalvi
"""

import numpy as np
import matplotlib.pyplot as plt
import sympy
#from matplotlib.widgets import Slider 



#MY OBJECTS-------------------------------------------------------------------- 
#------------------------------------------------------------------------------

class Mirror :
    """
    class which creats a mirror object with it own shape caracteristics
    centred around 0. 
    
    diam_ouv : miroor highter. (float)
    type_m : mirror types.(*) (str)
    r : radius of the caracteristic cercle of the mirror.(float) 
    
    (*)mirror types : - convcave
                      - convexe
                   
                   
    #Attention :  pour le moment, le nombre de rayon correspind à la moitier du
    nombre de rayons final et si l'on selectionne un diam_ouv inférieur à la 
    largeur du faisceau ou un faisceau trop large par rapport à la taille du 
    cercle  on a des problèmes que je n'ai pas eu le temps de régler 

    """
    
    def __init__(self, r = 4, diam_ouv = 6,type_m = 'concave'):
        
        self.diam_ouv = diam_ouv 
        self.r = r
        self.type_m = type_m

        
    def shape(self):
        """
        shape of mirror always centred around O(0,0) 
        """
        if self.type_m  == 'concave':
            self.name = 'mirroir concave'
            angle_ouv = np.arcsin((self.diam_ouv)/(2*self.r))
            theta = np.linspace((np.pi/2)-angle_ouv, (np.pi/2)+angle_ouv)
            self.Yc = -self.r*np.cos(theta)
            self.Xc = self.r*np.sin(theta)

        if  self.type_m == 'convexe' : 
            self.name = 'mirroir convexe'
            angle_ouv = np.arcsin((self.diam_ouv)/(2*self.r))
            theta = np.linspace(-np.pi/2-angle_ouv, -np.pi/2+angle_ouv)
            self.Yc = -self.r*np.cos(theta)
            self.Xc = self.r*np.sin(theta)
   
        else :
           return 'error'

#------------------------------------------------------------------------------       
       
class Lent:
    """
    class which permits to creat a lentil with it own caracteristics
    
    H_lent : how long is the lentile. (float)
    L_lent : how large is the lentille. (float)
    coef : marerial caracteristic. (float)
    type_l : lentile types.(*) (str)
    
    
    (*) lentile types : - convergent
                    - divergent
    
    #Attention :  pour le moment, cette classe n'a pas d'utilité dans le 
    programme, je n'ai pas eu le temps de finir la mise en équation des 
    rayons dans la classe Beam et j'ai un problème pour les solutions de mon 
    équation entre mon faisceau et mon Ellipse (solutions complexes soit- disant)
    
    """
    
    def __init__(self, H_lent, L_lent, type_l = 'convergent'):
        self.H_lent = H_lent
        self.L_lent = L_lent
        self.type_l = type_l

    
    def shape(self):
        """
        shape of lentille 
        """
        self.Yd = []
        if self.type_l == 'convergente':
            theta = np.linspace(0,2*np.pi,1000)     #paramétrisation d'une Ellipse 
            self.Xe = self.L_lent/2*np.cos(theta)   #de hauteur H_lent et de
            self.Ye = self.H_lent /2*np.sin(theta)  #largeur L_lent
            
        if self.type_l == 'divergent':
            pass 
            
        else : 
            return 'error' 
            
 
        
#RAYS -------------------------------------------------------------------------
#------------------------------------------------------------------------------
            
class Beam: 
    """
    Beam creat N rays in a L_beam interval centred in 0. 
    Space : x space. (array)
    Nb : Number of ray in one beam. (int) # plutôt la moitier du nombre de rayons
    L_beam : Beam's larger. (float)
    color : color of the beam. (str)
    """
    
    def __init__(self, L_beam=4, objet = Mirror(),  Nb = 3, color = 'green'):
        
        self.L_beam = L_beam
        self.objet = objet
        if isinstance(self.objet, Mirror):
            self.type_m = self.objet.type_m
            self.r = self.objet.r
        if isinstance(self.objet, Lent):
            self.type_l = self.objet.type_l
            self.H_lent = self.objet.H_lent
            self.L_lent = self.objet.L_lent
        self.Nb = Nb
        self.Xo = np.linspace(-10,10,100)
        self.color = color


    def ray(self):

#dans le cas où mirroir -------------------------------------------------------
        if  isinstance(self.objet, Mirror):
            
            
#dans le cas où mirroir concave -----------------------------------------------
            if self.type_m =='concave':
                self.Ray_i = []
                self.Ray_r = []
                self.lst_sol = []
                self. X_bef_lst = []
                for n in range(self.Nb):
                    x, y = sympy.symbols('x y')
                    eq1 = x**2+y**2-self.r**2
                    eq2 = -y+n*(self.L_beam/self.Nb)
                    sol = sympy.solve([eq1,eq2], [x,y])
                    self.lst_sol.append(sol) #liste de solution [[(x1,y1),(x2,y2)],...,[(x, y),(x, y)]]
                    
                    self.x_sol = float(self.lst_sol[n][1][0]) 
                    self.y_sol = float(self.lst_sol[n][1][1]) 
                    
                    self.X_bef = np.linspace(np.min(self.Xo),float(self.lst_sol[n][1][0]) ,100) 
                    self.X_bef_lst.append(self.X_bef)
                    
                    
                    ray_i = self.X_bef_lst[n]*0+(self.L_beam/self.Nb)*n
                    ray_r = self.X_bef_lst[n]*2*(self.y_sol/self.x_sol)-(self.L_beam/self.Nb)*n
     
                    self.Ray_i.append([ray_i, -ray_i])
                    self.Ray_r.append([ray_r, -ray_r])
                    
#dans le cas où mirroir concave -----------------------------------------------
            if self.type_m =='convexe':
                self.Ray_i = []
                self.Ray_r = []
                self.Ray_v = []
                self.lst_sol = []
                self. X_bef_lst = []
                self.X_aft_lst = []
                for n in range(self.Nb):
                    x, y = sympy.symbols('x y')
                    eq1 = x**2+y**2-self.r**2
                    eq2 = -y+n*(self.L_beam/self.Nb)
                    sol = sympy.solve([eq1,eq2], [x,y])
                    self.lst_sol.append(sol) #liste de solution [[(x1,y1),(x2,y2)],...,[(x, y),(x, y)]]
                    
                    self.x_sol = float(self.lst_sol[n][0][0]) 
                    self.y_sol = float(self.lst_sol[n][0][1]) 
                    
                    
                    self.X_bef = np.linspace(np.min(self.Xo),float(self.lst_sol[n][0][0]) ,100) 
                    self.X_aft = np.linspace(float(self.lst_sol[n][0][0]),0,100) 
                    self.X_bef_lst.append(self.X_bef)
                    self.X_aft_lst.append(self.X_aft)
                    
                    
                    ray_i = self.X_bef_lst[n]*0+(self.L_beam/self.Nb)*n
                    ray_r = self.X_bef_lst[n]*2*(self.y_sol/self.x_sol)-(self.L_beam/self.Nb)*n
                    ray_v = self.X_aft*2*(self.y_sol/self.x_sol)-(self.L_beam/self.Nb)*n
    
    
                    self.Ray_i.append([ray_i, -ray_i])
                    self.Ray_r.append([ray_r, -ray_r])
                    self.Ray_v.append([ray_v, -ray_v])
                
                
                

#dans le cas où lentille ------------------------------------------------------  
        if isinstance(self.objet, Lent):
#dans le cas où lentille convergeante -----------------------------------------
            if self.type_l == 'convergent':
                self.lst_sol = []
                self.X_1_lst = []
                self.X_2_lst = []
                self.X_3_lst = []
            
                for n in range(self.Nb):
                    x, y = sympy.symbols('x y')
                    eq1 = ((x**2)/self.L_lent)+((y**2)/self.H_lent)-1
                    eq2 = -y+n*(self.L_beam/self.Nb)
                    sol = sympy.solve([eq1,eq2], [x,y])
                    self.lst_sol.append(sol)
                    
                    self.x_sol = float(self.lst_sol[n][0][0]) 
                    self.y_sol = float(self.lst_sol[n][0][1]) 
                    
                    self.X_1 = np.linspace(np.min(self.Xo),float(self.lst_sol[n][0][0]) ,100) 
                    self.X_1_lst.append(self.X_1)
                    self.X_2 = np.linspace(float(self.lst_sol[n][0][0]),float(self.lst_sol[n][1][0]) ,10) 
                    self.X_2_lst.append(self.X_2)
                    self.X_3 = np.linspace(float(self.lst_sol[n][1][0]),np.max(self.Xo),100) 
                    self.X_3_lst.append(self.X_3)
                    
                    
                    #ray_1 = self.X_bef_lst[n]*0+(self.L_beam/self.Nb)*n
                    #ray_2 = 
                    #ray_3 =
    
    
                    #self.Ray_1.append([])
                    #self.Ray_2.append([])
                    #self.Ray_2.append([])
                    
                    
  
                     
        
           
#MY FIGURE---------------------------------------------------------------------
#------------------------------------------------------------------------------
        
class Fig :
    """
    permit to creat a fig with the stuff we need 
    
    objet = Mirror() or Lent()
    beam = Beam()    
    """
    
    
    def __init__(self, objet, beam ):
        if isinstance(objet, Mirror):
            self.objet = objet
        if isinstance(beam, Beam):
            self.beam = beam
            
    def plot(self):
        fig, ax = plt.subplots()
        ax.set_xlim(np.min(self.beam.Xo), np.max(self.beam.Xo))
        ax.set_ylim(-10, 10)
        ax.set_title("Effets d'un {} sur des rayons à l'infini".format(self.objet.name))


#dans le cas où mirroir -------------------------------------------------------       
        if isinstance(self.objet, Mirror): 
            ax.plot(self.objet.Xc,self.objet.Yc , color = 'black')
            ax.plot(self.beam.Xo, 0*self.beam.Xo,  '--', color = 'gray')
            ax.plot(0, 0, '|', color = 'black', label = 'Centre du miroir')

            ax.set_yticks([0])
            ax.set_yticklabels([' '])
            
            
            if self.beam.Nb<15:      #change la transparence en fonction du 
                self.alpha = 0.5     #nombre de rayons. Slider_alpha serait une
            if self.beam.Nb >= 15:   #bonne idée.
                self.alpha = 0.3
            if self.beam.Nb >= 50:
                self.alpha = 0.1
                
                
            for i in range(self.beam.Nb):
                ax.plot(self.beam.X_bef_lst[i],self.beam.Ray_i[i][0], color = self.beam.color, alpha = self.alpha)
                ax.plot(self.beam.X_bef_lst[i],self.beam.Ray_i[i][1], color = self.beam.color, alpha = self.alpha)
                ax.plot(self.beam.X_bef_lst[i],self.beam.Ray_r[i][0], color = self.beam.color, alpha = self.alpha)
                ax.plot(self.beam.X_bef_lst[i],self.beam.Ray_r[i][1], color = self.beam.color, alpha = self.alpha)
                if self.objet.type_m =='convexe':
                    ax.set_xlim(np.min(self.beam.Xo), 0)
                    ax.set_ylim(np.min(self.beam.Xo)/2,-np.min(self.beam.Xo)/2)
                    ax.plot(self.beam.X_aft_lst[i],self.beam.Ray_v[i][0],'--',  color = 'gray', alpha = self.alpha) #rayons
                    ax.plot(self.beam.X_aft_lst[i],self.beam.Ray_v[i][1],'--',  color = 'gray', alpha = self.alpha) #virtuels
                
                
#dans le cas où lentille ------------------------------------------------------
        if isinstance(self.objet, Lent): 
            ax.plot(self.objet.Xe,self.objet.Ye, color = 'blue', alpha = 0.2)
            ax.fill_between(self.objet.Xe, self.objet.Ye, facecolor='blue', alpha=0.05)
        #ax.legend()
        

        plt.show()
        
        
#TESTS--------------------------------------------------------------------------
#------------------------------------------------------------------------------          
        
if __name__ == "__main__":
    #obj =  Lent(H_lent = 5, L_lent = 2)
    obj = Mirror(type_m = 'convexe')
    obj.shape()
    beam = Beam(0.5, obj, 10)
    beam.ray()
    fig = Fig(obj, beam)
    fig.plot()
    
    

