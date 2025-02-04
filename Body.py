import numpy as np


class Body:
    """The class that encapsulates the objects in the simulation"""
    T = None
    instance = []
    G = 6.67408e-11

    def __init__(self, mass, radius, xpos, ypos, xvel, yvel):
        """Initializes the object
        mass: mass of the object in kilograms
        radius: radius of the object in meters
        xpos: x position of the object in meters
        ypos: y position of the object in meters
        xvel: x velocity of the object in meters per second
        yvel: y velocity of the object in meters per second"""
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
        """Calculates the gravitational force between two bodies in the x and y directions in Newtons
        object: the other body"""
        if self != object:
            x = object.xpos - self.xpos
            y = object.ypos - self.ypos

            # Pythagorean Theorem
            r = np.sqrt(x**2 + y**2)

            if r < (self.radius + object.radius):
                self.collide(object)
            elif r != 0:
                force = self.__class__.G * self.mass * object.mass / (r**2)
                # Similar Triangles
                self.xnetforce += force * x / r
                self.ynetforce += force * y / r

    def calcAcc(self):
        """Calculates the acceleration of the object using the formula a = F/m in meters per second squared"""
        self.xacc = self.xnetforce / self.mass
        self.yacc = self.ynetforce / self.mass

    def calcVel(self):
        """Calculates the velocity of the object using the formula v_f = v_i + a * t in meters per second"""
        self.xvel = self.xvel + self.__class__.T * self.xacc
        self.yvel = self.yvel + self.__class__.T * self.yacc

    def calcPos(self):
        """Calculates the position of the object using the formula x_f = x_i + v_i * t + 1/2 * a * t^2 in meters"""
        self.xpos = self.xpos + (self.xvel * self.__class__.T + 0.5 * self.xacc * (
            self.__class__.T ** 2))  # d = v intial * t + 0.5 * a * t ^ 2
        self.ypos = self.ypos + \
            (self.yvel * self.__class__.T + 0.5 *
             self.yacc * (self.__class__.T ** 2))

    def calc(self):
        """Calculates the acceleration, velocity, and position of the object"""
        self.xnetforce = 0
        self.ynetforce = 0
        for i in self.__class__.instance:
            if i != self:
                self.forces(i)
        self.calcAcc()
        self.calcPos()
        self.calcVel()

    def collide(self, object):
        """Handles the collision between two bodies
        object: the other body"""
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
        """Calculates the acceleration, velocity, and position of all the objects"""
        for i in cls.instance:
            i.calc()

    # create 500 random bodies with mass, radius, xpos, ypos, xvel, yvel similar to the Earth
    @classmethod
    def randomBodies(cls, n, xlim, ylim):
        """Creates n random bodies
        n: number of bodies
        xlim: x limit of the simulation
        ylim: y limit of the simulation"""
        for i in cls.instance:

            del i
        cls.instance = []
        for i in range(n):
            #body(np.random.random() * 1e24, np.random.random() * 1e6, np.random.random() * 1e11, np.random.random() * 1e11, np.random.random() * 0*1e3, np.random.random() * 0*1e3)
            radius = np.random.random() * 1e6
            if radius == 0:
                radius = 1e6

            # Based on the density of the Earth
            mass = 4 / 3 * radius ** 3 * np.pi * 5513000

            xpos = np.random.uniform(xlim[0], xlim[1])
            ypos = np.random.uniform(ylim[0], ylim[1])

            Body(mass, radius, xpos, ypos, np.random.random()
                 * 1*1e3, np.random.random() * 1*1e3)

    @classmethod
    def getObjects(cls):
        """Returns the list of objects"""
        objects = []
        for i in cls.instance:
            objects.append(i.__dict__)

        return objects

    @classmethod
    def setT(cls, t):
        """Sets the time step
        t: time step in seconds"""
        cls.T = t

    @classmethod
    def setObjects(cls, objects):
        """Initialize objects from a list of the objects
        objects: list of objects"""
        for i in cls.instance:
            del i
        cls.instance = []
        for i in objects:
            Body(i['mass'], i['radius'], i['xpos'],
                 i['ypos'], i['xvel'], i['yvel'])
