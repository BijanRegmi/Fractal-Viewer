import cv2

class Fractal:
    def __init__(self, **kwargs):
        self.config = {
            'IMAGE_SIZE': 1080,
            'SET_X': -2,
            'SET_Y': -2,
            'SET_SIZE': 4,
            'ITERS': 100
        }
        self.updateparams(**kwargs)
        
        if all(x not in kwargs.keys() for x in ['SET_X', 'SET_Y', 'SET_SIZE', 'IMAGE_SIZE']):
            self.setImageParams()
    
    def updateparams(self, **kwargs):
        '''Redefine this updateparams method in derived class to take in the parameters defining the fractal'''
        print(self.updateparams.__doc__)

    def setImageParams(self):
        '''Redefine this setImageParams method in derived class to create extra necessary params using raw params'''
        print(self.setImageParams.__doc__)

    def genImage(self):
        '''Redefine this genImage method in derived class to generate the image(Usually this will store the formula how the fractal is generated)'''
        print(self.genImage.__doc__)

    def saveimage(self, name):
        try:
            cv2.imwrite(name, self.image)
        except:
            print("Please create an image first!")