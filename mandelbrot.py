import numpy as np
from fractal import Fractal
import cv2

class mandelbrot(Fractal):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def updateparams(self, **kwargs):
        keys = kwargs.keys()
        for key, val in kwargs.items():
            self.config[key] = val
        if any(x in keys for x in ['SET_X', 'SET_Y', 'SET_SIZE', 'IMAGE_SIZE']):
            self.setImageParams()
    
    def setImageParams(self):
        x = np.linspace(self.config['SET_X'], self.config['SET_X'] + self.config['SET_SIZE'], num=self.config['IMAGE_SIZE'])
        y = np.linspace(self.config['SET_Y'], self.config['SET_Y'] + self.config['SET_SIZE'], num=self.config['IMAGE_SIZE'])

        self.constant = x[:,None] + 1j*y[None,:]
        
        self.z = np.zeros((self.config['IMAGE_SIZE'], self.config['IMAGE_SIZE']), dtype=complex)
        print("z and constant set with these config:",self.config,end='\n')
    
    def genImage(self):
         return self.Colored()

    def Black(self):
        # Disabled warnings because of NAN and INF values
        with np.warnings.catch_warnings():
            np.warnings.simplefilter("ignore")
            
            for i in range(self.config['ITERS']):
                self.z = self.z * self.z + self.constant
            
            #Map true to 255 and false to 0
            gray = ( np.abs(self.z) < 2 ) * 255

            #Make 3 channels
            self.image = np.stack((gray,)*3, axis=-1)
            
            #Rotate the image cause numpy treats axis the opposite way then convert to uint8
            self.image = np.uint8( np.rot90(self.image) )
            
            return self.image
    
    def Colored(self):
        mask = np.ones_like(self.constant, dtype=bool)
        itercounts = np.zeros((self.config['IMAGE_SIZE'], self.config['IMAGE_SIZE']), np.uint8)
        
        for i in range(self.config['ITERS']):
            self.z[mask] = self.z[mask] * self.z[mask] + self.constant[mask]
            mask[np.abs(self.z) > 2] = False
            itercounts[mask] = i

        quotient = itercounts/self.config['ITERS']*255
        
        factor = np.power(itercounts/self.config['ITERS'], 0.5)*255

        r = np.where(quotient>0.5*255, factor, 0)
        g = np.where(quotient>0.5*255, 1, factor)
        b = np.where(quotient>0.5*255, factor, 0)

        r[itercounts == self.config['ITERS']-1] = 0
        g[itercounts == self.config['ITERS']-1] = 0
        b[itercounts == self.config['ITERS']-1] = 0

        self.image = np.stack((r,g,b),-1)

        self.image = np.uint8(np.rot90(self.image))

        return self.image

        
        

if __name__=="__main__":
    params = {'IMAGE_SIZE': 1080, 'SET_X': -2, 'SET_Y': -2, 'SET_SIZE': 4, 'ITERS': 100}
    m = mandelbrot(**params)
    m.genImage()
    m.saveimage("out.png")
    