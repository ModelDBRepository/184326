'''
Defines a class, Neuron473862421, of neurons from Allen Brain Institute's model 473862421

A demo is available by running:

    python -i mosinit.py
'''
class Neuron473862421:
    def __init__(self, name="Neuron473862421", x=0, y=0, z=0):
        '''Instantiate Neuron473862421.
        
        Parameters:
            x, y, z -- position offset
            
        Note: if name is not specified, Neuron473862421_instance is used instead
        '''
             
        self._name = name
        # load the morphology
        from load_swc import load_swc
        load_swc('Pvalb-IRES-Cre_Ai14_IVSCC_-169125.03.01.01_469628681_m.swc', self,
                 use_axon=False, xshift=x, yshift=y, zshift=z)

        # custom axon (works because dropping axon during import)
        from neuron import h
        self.axon = [h.Section(cell=self, name='axon[0]'),
                     h.Section(cell=self, name='axon[1]')]
        for sec in self.axon:
            sec.L = 30
            sec.diam = 1
            sec.nseg = 1
        self.axon[0].connect(self.soma[0](0.5))
        self.axon[1].connect(self.axon[0](1))
        self.all += self.axon
   
        self._insert_mechanisms()
        self._discretize_model()
        self._set_mechanism_parameters()
    
    def __str__(self):
        if self._name is not None:
            return self._name
        else:
            return "Neuron473862421_instance"
                
    def _insert_mechanisms(self):
        from neuron import h
        for sec in self.all:
            sec.insert("pas")
        for mech in [u'CaDynamics', u'Ca_HVA', u'Ca_LVA', u'Ih', u'Im_v2', u'K_T', u'Kd', u'Kv2like', u'Kv3_1', u'NaV', u'SK']:
            self.soma[0].insert(mech)
    
    def _set_mechanism_parameters(self):
        from neuron import h
        for sec in self.all:
            sec.Ra = 138.99
            sec.e_pas = -88.2336349487
        
        for sec in self.axon:
            sec.cm = 1.94
            sec.g_pas = 0.000961798232139
        for sec in self.dend:
            sec.cm = 1.94
            sec.g_pas = 4.16908384089e-07
        for sec in self.soma:
            sec.cm = 1.94
            sec.ena = 53.0
            sec.ek = -107.0
            sec.gbar_Ih = 0.00030357
            sec.gbar_NaV = 0.0521615
            sec.gbar_Kd = 0.00331265
            sec.gbar_Kv2like = 0.0192063
            sec.gbar_Kv3_1 = 1.21289
            sec.gbar_K_T = 1.4016e-05
            sec.gbar_Im_v2 = 0.00111537
            sec.gbar_SK = 0.0481527
            sec.gbar_Ca_HVA = 0
            sec.gbar_Ca_LVA = 0
            sec.gamma_CaDynamics = 0.0460903
            sec.decay_CaDynamics = 574.749
            sec.g_pas = 0.000586894
    
    def _discretize_model(self):
        for sec in self.all:
            sec.nseg = 1 + 2 * int(sec.L / 40)

