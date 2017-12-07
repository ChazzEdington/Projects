#Arena and main
#Works on the assumption that two sets of creatures are passed and one set
#of lights, as seen in the example configuration cases. If that is not the
#Case, may break code

import turtle
import math
import random
import entities
import TestConfiguration

turtle.hideturtle()
turtle.speed(0)

class Arena:


    def __init__(self, Test):

        #Creature information
        self.creatures1 = Test[0]
        self.creatures2 = Test[1]
        self.lights = Test[2]

        #hold dictionary. More information passed to it in initialize
        #graphics. Passed to entities at times for information
        self.hold = {'Creatures':[],'Lights':[],
                     'current_creature':'', 'current_light': ''}

        self.InitializeEntities()

        #Variables dealing with Arena. All set in InitializeGraphics.
        self.sides = None
        self.radius = None
        self.side_lengtht = None
        self.apothem = None

        

    #Creates arena objects
    def InitializeEntities(self):

    #Initializes all arena items
        for item in range(self.creatures1.count):
            if self.creatures1.attract == True:
                self.hold['Creatures'].append(entities.Attracted(self.creatures1.speed,
                                                              self.creatures1.attract,
                                                              self.creatures1.space))
            else:
                self.hold['Creatures'].append(entities.Repelled(self.creatures1.speed,
                                                              self.creatures1.attract,
                                                              self.creatures1.space))
        for item in range(self.creatures2.count):
            if self.creatures2.attract == True:
                self.hold['Creatures'].append(entities.Attracted(self.creatures2.speed,
                                                              self.creatures2.attract,
                                                              self.creatures2.space))
            else:
                self.hold['Creatures'].append(entities.Repelled(self.creatures2.speed,
                                                             self.creatures2.attract,
                                                             self.creatures2.space))

        for item in range(self.lights.count): 
            self.hold['Lights'].append(entities.Light(self.lights.speed,
                                                           self.lights.random))

    def InitializeGraphics(self):

        #if running on smaller than 13 inch screen, decrease screen_size
        #or increase buffer
        screen_size = 940
        buffer = 100
        
        screen = turtle.getscreen()
        screen.setup(screen_size, screen_size)
        
        #Sides of Arena, drawn as regular polygons
        self.sides = 5#random.randint(6, 15)
        
        #fits arena into circle on screen
        self.radius = (screen_size - buffer)/2
        theta = (math.pi*2)/self.sides
        self.apothem = abs(self.radius*math.cos(.5*theta))
        self.side_length = abs(2*self.radius*math.sin(.5*theta))

        #lift pen and set position of turtle to draw
        turtle.pu()
        turtle.setpos(-(.5*self.side_length), -self.apothem)

        #call function that draws regular polygons given sides and length
        draw_polygon(self.sides, self.side_length)

        self.hold['apothem'] = self.apothem
        self.hold['sides'] = self.sides

    def Update(self):

        for i in range(2):
            for creature in self.hold['Creatures']:
                if i == 0:
                    self.hold['current_creature'] = creature
                    creature.move(self.hold)
                else:
                    creature.update_XY()

            for light in self.hold['Lights']:
                if i == 0:
                    self.hold['current_light'] = light
                    light.move(self.hold)
                else:
                    light.update_XY()

        
#draws a regular polygon given sides a length
def draw_polygon(sides, length):

    angle = 360/sides

    #Choose color to fill polygon
    colors = ['light blue', 'light green', 'violet', 'orange']
    color = colors[random.randint(0,3)]
    turtle.color(color)
    
    turtle.pd()
    turtle.begin_fill()
    
    for i in range(sides):

        turtle.forward(length)
        turtle.left(angle)

    turtle.end_fill()
    turtle.pu()


def main():
    
    turtle.tracer(0,0)

    test_case = 1
    
    arena = Arena(TestConfiguration.example[test_case])
    arena.InitializeGraphics()

    print('control c to quit simulation')
    
    try:
        while True:
            arena.Update()
            turtle.update()
            
    except KeyboardInterrupt:
        print('Done swarming.')

main()
