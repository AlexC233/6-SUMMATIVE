import numpy as np
import Main

T = Main.step

class body:
    instance = []
    G = 6.67408e-11

    def __init__(self, mass, radius, xpos, ypos, xvel, yvel):
        self.__class__.instance.append(self)
        self.mass = mass
        self.radius = radius
        self.xpos = xpos # x position
        self.ypos = ypos # y position
        self.xvel = xvel # x velocity
        self.yvel = yvel # y velocity
        self.xacc = 0 # x acceleration
        self.yacc = 0 # y acceleration
        self.xnetforce = 0 # x net force
        self.ynetforce = 0 # y net force

    # calculate the x and y components of the gravitational force between two bodies
    def forces(self, object):
        if self != object:
            x = object.xpos - self.xpos
            y = object.ypos - self.ypos

            r = np.sqrt(x**2 + y**2)

            if r < (self.radius + object.radius):
                self.collide(object)
            elif r != 0:
                force = self.__class__.G * self.mass * object.mass / (r**2)
                self.xnetforce += force * x / r
                self.ynetforce += force * y / r

    def calcAcc(self):
        self.xacc = self.xnetforce / self.mass
        self.yacc = self.ynetforce / self.mass
    
    def calcVel(self):
        self.xvel = self.xvel + T * self.xacc
        self.yvel = self.yvel + T * self.yacc

    def calcPos(self):
        self.xpos = self.xpos + (self.xvel * T - 0.5 * self.xacc * (T ** 2)) # d = v final * t - 0.5 * a * t ^ 2
        self.ypos = self.ypos + (self.yvel * T - 0.5 * self.yacc * (T ** 2))

    def calc(self):
        self.xnetforce = 0
        self.ynetforce = 0
        for i in self.__class__.instance:
            if i != self:
                self.forces(i)
        self.calcAcc()
        self.calcVel()
        self.calcPos()

    def collide(self, object):
        print("ran")
        # Momentum formula
        momentumX = self.mass * self.xvel + object.mass * object.xvel
        momentumY = self.mass * self.yvel + object.mass * object.yvel

        # Center of mass formula
        self.xpos = (self.mass * self.xpos + object.mass * object.xpos) / (self.mass + object.mass)
        self.ypos = (self.mass * self.ypos + object.mass * object.ypos) / (self.mass + object.mass)

        self.mass += object.mass
        self.radius = np.cbrt(self.radius**3 + object.radius**3)

        self.xvel = momentumX / self.mass
        self.yvel = momentumY / self.mass

        self.__class__.instance.remove(object)
        del object

    @classmethod
    def calcAll(cls):
        for i in cls.instance:
            # Pruning
            if i.xpos > 1e10 or i.xpos < 0e10 or i.ypos > 1e10 or i.ypos < 0e10:
                cls.instance.remove(i)
                print("cleaned")
                del i
            else:
                i.calc()

# create 500 random bodies with mass, radius, xpos, ypos, xvel, yvel similar to the Earth
def randomBodies(n):
    for i in range(n):
        #body(np.random.random() * 1e24, np.random.random() * 1e6, np.random.random() * 1e11, np.random.random() * 1e11, np.random.random() * 0*1e3, np.random.random() * 0*1e3)
        mass = np.random.random() * 1e24
        if mass == 0:
            mass = 1e24
        body(mass, np.random.random() * 1e6, np.random.random() * 1e8, np.random.random() * 1e8, np.random.random() * 1*1e3, np.random.random() * 1*1e3)
 
