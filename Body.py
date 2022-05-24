import numpy as np


class Body:
    T = None
    instance = []
    G = 6.67408e-11

    def __init__(self, mass, radius, xpos, ypos, xvel, yvel):
        self.__class__.instance.append(self)
        self.mass = mass
        self.radius = radius
        self.xpos = xpos  # x position
        self.ypos = ypos  # y position
        self.xvel = xvel  # x velocity
        self.yvel = yvel  # y velocity
        self.xacc = 0  # x acceleration
        self.yacc = 0  # y acceleration
        self.xnetforce = 0  # x net force
        self.ynetforce = 0  # y net force

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
        self.xvel = self.xvel + self.__class__.T * self.xacc
        self.yvel = self.yvel + self.__class__.T * self.yacc

    def calcPos(self):
        self.xpos = self.xpos + (self.xvel * self.__class__.T + 0.5 * self.xacc * (
            self.__class__.T ** 2))  # d = v intial * t + 0.5 * a * t ^ 2
        self.ypos = self.ypos + \
            (self.yvel * self.__class__.T + 0.5 *
             self.yacc * (self.__class__.T ** 2))

    def calc(self):
        self.xnetforce = 0
        self.ynetforce = 0
        for i in self.__class__.instance:
            if i != self:
                self.forces(i)
        self.calcAcc()
        self.calcPos()
        self.calcVel()

    def collide(self, object):
        print("ran")
        # Momentum formula
        momentumX = self.mass * self.xvel + object.mass * object.xvel
        momentumY = self.mass * self.yvel + object.mass * object.yvel

        # Center of mass formula
        self.xpos = (self.mass * self.xpos + object.mass *
                     object.xpos) / (self.mass + object.mass)
        self.ypos = (self.mass * self.ypos + object.mass *
                     object.ypos) / (self.mass + object.mass)

        self.mass += object.mass
        self.radius = np.sqrt(self.radius**2 + object.radius**2)

        self.xvel = momentumX / self.mass
        self.yvel = momentumY / self.mass

        self.__class__.instance.remove(object)
        del object

    @classmethod
    def calcAll(cls):
        for i in cls.instance:
            i.calc()

    # create 500 random bodies with mass, radius, xpos, ypos, xvel, yvel similar to the Earth
    @classmethod
    def randomBodies(cls, n, xlim, ylim):
        for i in cls.instance:
            cls.instance.remove(i)
            del i
        for i in range(n):
            #body(np.random.random() * 1e24, np.random.random() * 1e6, np.random.random() * 1e11, np.random.random() * 1e11, np.random.random() * 0*1e3, np.random.random() * 0*1e3)
            radius = np.random.random() * 1e6
            if radius == 0:
                radius = 1e6

            mass = 4 / 3 * radius ** 3 * np.pi * 5513000

            xpos = np.random.uniform(xlim[0], xlim[1])
            ypos = np.random.uniform(ylim[0], ylim[1])

            Body(mass, radius, xpos, ypos, np.random.random()
                 * 1*1e3, np.random.random() * 1*1e3)

    @classmethod
    def getObjects(cls):
        objects = []
        for i in cls.instance:
            objects.append(i.__dict__)

        return objects

    @classmethod
    def setT(cls, t):
        cls.T = t

    @classmethod
    def setObjects(cls, objects):
        for i in cls.instance:
            cls.instance.remove(i)
            del i
        for i in objects:
            Body(i['mass'], i['radius'], i['xpos'],
                 i['ypos'], i['xvel'], i['yvel'])
