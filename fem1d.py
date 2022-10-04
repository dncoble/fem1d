'''
Library for running FEM1D processes. 

Author: Daniel Coble
Copyright (c) 2022
MIT License
'''
import subprocess
import os
'''
FEMProblem contains all the variables used for
'''
class FEM1DProblemData():
    
    '''
    templates autofill some dict values based on known problem structure
    allowed templates:
        'beam'
        
    **kwargs are name, values to fill card
    card format:
        ----- card 1
        title
        ----- card 2
        model
        ntype
        item
        ----- card 3
        ielem
        nem \ generated automatically
        ----- card 4
        icont = 0 \ generated automatically
        nprnt
        ----- card 10
        nnm \ generated automatically
        ----- card 11 cards 11-15 are read for each element
        nod \ generated automatically
        glx
        ----- card 12
        ax0
        ax1
        ----- card 13
        bx0
        bx1
        ----- card 14
        cx0
        cx1
        ----- card 15
        fx0
        fx1
        fx2
        ----- card 16 cards 16-23 are only for truss/frame problems
        nnm
        ----- card 17 skip cards 17-19 for truss problems. cards 17-21 are read
              for each element
        pr
        se
        sl
        sa
        si
        cs
        sn
        ----- card 18
        hf
        vf
        pf
        xb
        cnt
        snt
        ----- card 19
        nod \ generated automatically
        ----- card 20 skip cards 20-21 for frame problems.
        se
        sl
        sa
        cs
        sn
        hf
        ----- card 21
        nod \ generated automatically
        ----- card 22
        ncon \ generated automatically
        ----- card 23 repeat ncon times. skip card 23 if ncon=0
        icon
        vcon
        ----- card 24
        nspv \ generated automatically
        ----- card 25 repeat nspv times. skip card 25 if nspv=0
        ispv1
        ispv2
        vspv
        ----- card 26 skip card 26 for eigenvalue problems
        nssv \ generated automatically
        ----- card 27 repeat nssv times. skip card 27 if nssv=0
        issv1
        issv2
        vssv
        ----- card 28
        nnbc \ generated automatically
        ----- card 29 repeat nnbc times. skip card 29 if nnbc=0
        inbc1
        inbc2
        vnbc
        uref
        ----- card 30
        nmpc \ generated automatically
        ----- card 31 repeat nmpc times. skip card 31 if nmpc=0
        imc11
        imc12
        imc21
        imc22
        vmpc
        vmpc4
        ----- card 32 skip card 32 if item=0
        ct0
        ct1
        ----- card 33 skip cards 33-36 if item=0 or item=3
        dt
        alfa
        gama
        ----- card 34
        incond
        ntime
        intvl
        ----- card 35 skip cards 35-36 if incond=0
        guo
        ----- card 36 skip card 36 if item=1
        gui
        
    '''
    # equal nodes for every element
    def __init__(elements, nodes_per_element, template=None, **kwargs):
        self.vars = kwargs
        self.card = ''
        self.local_nodes = [nodes_per_element]*elements
        
        
        # generating all autogenerated variables
        # nem icont nnm ncon nspv nssv nnbc nmpc nod
        self.vars['nem'] = elements
        self.vars['icont'] = 0
        self.vars['nnm'] = elements*nodes_per_element - (elements - 1)
        self.vars['ncon'] = len(self.vars['icon'])
        self.vars['nspv'] = len(self.vars['ispv1'])
        self.vars['nssv'] = len(self.vars['issv1'])
        self.vars['nnbc'] = len(self.vars['inbc1'])
        self.vars['nmpc'] = len(self.vars['imc11'])
        c = 1; nod = []
        for i in range(elements):
            *l, = range(c, nodes_per_element + c)
            nod.append(l)
            c = l[-1]
        self.vars['nod'] = nod
        
    def __init__(nodes_per_element, template=None, **kwargs):
        self.vars = kwargs
        self.card = ''
        self.local_nodes = nodes_per_element
        
        # generating all autogenerated variables
        # nem icont nnm ncon nspv nssv nnbc nmpc nod
        self.vars['nem'] = len(nodes_per_element)
        self.vars['icont'] = 0
        self.vars['nnm'] = sum(nodes_per_element) - (len(nodes_per_element) - 1)
        self.vars['ncon'] = len(self.vars['icon'])
        self.vars['nspv'] = len(self.vars['ispv1'])
        self.vars['nssv'] = len(self.vars['issv1'])
        self.vars['nnbc'] = len(self.vars['inbc1'])
        self.vars['nmpc'] = len(self.vars['imc11'])
        c = 1; nod = []
        for n in nodes_per_element:
            *l, = range(c, n+c)
            nod.append(l)
            c = l[-1]
        self.vars['nod'] = nod
        
    def add_card(*args):
        for arg in card:
            self.card += str(arg) + ' '
        self.card += '\n'
    
    def build_cards():
        self.card = '' # clear card
        ############ cards 1-4, 10
        self.add_card(self.vars['title'])
        self.add_card(self.vars['model'], self.vars['ntype'], self.vars['item'])
        self.add_card(self.vars['ielem'], self.vars['nem'])
        self.add_card(self.vars['icont'], self.vars['nprnt'])
        self.add_card(self.vars['nnm'])
        ############ cards 11-15
        for e in range(self.vars['nem']):
            self.add_card(self.vars['nod'][e], self.vars['glx'][e])
            self.add_card(self.vars['ax0'][e], self.vars['ax1'][e])
            self.add_card(self.vars['bx0'][e], self.vars['bx1'][e])
            self.add_card(self.vars['cx0'][e], self.vars['cx1'][e])
            self.add_card(self.vars['fx0'][e], self.vars['fx1'][e], self.vars['fx2'][e])
        ############ cards 16-23
        if(self.vars['model'] == 4):
            self.add_card(self.vars['nnm'])
            for e in range(self.vars['nem']):
                if(self.vars['ntype'] != 0):
                    self.add_card(self.vars['pr'][e], self.vars['se'][e], self.vars['sl'][e],
                                  self.vars['sa'][e], self.vars['si'][e], self.vars['cs'][e],
                                  self.vars['sn'][e])
                    self.add_card(self.vars['hf'][e], self.vars['vf'][e], self.vars['pf'][e],
                                  self.vars['xb'][e], self.vars['cnt'][e], self.vars['snt'][e])
                else:
                    self.add_card(self.vars['se'][e], self.vars['sl'][e], self.vars['sa'][e],
                                  self.vars['cs'][e], self.vars['sn'][e], self.vars['hf'][e])
                self.add_card(self.vars['nod'])
            self.add_card(self.vars['ncon'])
            for i in range(self.vars['ncon']):
                self.add_card(self.vars['icon'][i], self.vars['vcon'][i])
        ############ cards 24-25
        self.add_card(self.vars['nspv'])
        for i in range(self.vars['nspv']):
            self.add_card(self.vars['ispv1'][i], self.vars['ispv2'][i], self.vars['vspv'][i])
        ############ cards 26-27
        self.add_card(self.vars['nssv'])
        for i in range(self.vars['nssv']):
            self.add_card(self.vars['issv1'][i], self.vars['issv2'][i], self.vars['vssv'][i])
        ############ cards 28-29
        self.add_card(self.vars['nnbc'])
        for i in range(self.vars['nnbc']):
            self.add_card(self.vars['inbc1'][i], self.vars['inbc2'][i], self.vars['vnbc'][i],
                          self.vars['uref'][i])
        ############ cards 30-31
        self.add_card(self.vars['nmpc'])
        for i in range(self.vars['nmpc']):
            self.add_card(self.vars['imc11'][i], self.vars['imc12'][i], self.vars['imc21'][i],
                          self.vars['imc22'][i], self.vars['vmpc'][i], self.vars['vmpc4'][i])
        ############ card 32-36
        if(self.vars['item'] != 0):
            self.add_card(self.vars['ct0'], self.vars['ct1'])
            if(self.vars['item'] != 3):
                self.add_card(self.vars['dt'], self.vars['alfa'], self.vars['gama'])
                self.add_card(self.vars['incond'], self.vars['ntime'], self.vars['intvl'])
                if(self.vars['incond'] != 0):
                    self.add_card(self.vars['guo'])
                    if(self.vars['item'] != 1):
                        self.add_card(self.vars('gui'))
        return self.card
    
    def save_card(filename):
        with open(filename, 'w') as f:
            f.write(self.card)
    
    #returns an FEMSolution object
    def solve():
        self.build_card()
        self.save_card('tempcard.inp')
        # solve with subprocess
        
        with open('solved_card.txt', 'w') as f:
            solved_card = f.read(self.card)
        os.remove('tempcard.inp')
        os.remove('solved_card.txt')
        return FEMSolution(solved_card)

'''
Contains solution data and supports certain postprocessing operations
'''
class FEMSolution:
    
    def __init__(solved_card):
        
    