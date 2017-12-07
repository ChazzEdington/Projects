#Entities

import turtle
import random
import math

turtle.ht()
turtle.tracer(0,0)


#-------------------------------Object-Class-------------------------------
#Creatures and lights all have many commonalities in methods and
#variables. The top super class will be object that holds these commonalities
class Object:

    def __init__(self, speed = 3):

        #makes self turtle object that can be called throughout
        self.object = turtle.Turtle()
        self.object.ht()
        self.object.pu()

        #distance is velocity*time. Since time is not used elsewhere
        #not made into a variable that will be saved
        time = 1
        self.speed = speed
        self.distance = speed*time

        #random start position within the arena. If arena size or buffer
        #changed, may have to be altered. Hard coded for ease and since not
        #part of the stated requirments. Will not actually start in this
        #position since it will be alter in move in initialization
        self.X = random.randint(-200, 200)
        self.Y = random.randint(-200, 200)
        #exists a current x&y along with a next x&y. Reason being is to keep
        #from updating some invidivuals before others. When determing where
        #to next go, nextx/y will be set. When other objects determing their
        #positional relationship to objects, they will call the last visualized
        #position, currentX/Y, of other objects.
        self.nextX = self.X
        self.nextY = self.Y

        #angle from (0,0) looking down the x axis to the object.
        #used for determining objects screen location
        self.zero_theta = 0

        #heading will be the direction the object is facing.
        #0 equivalent to looking directly down the x-axis
        self.heading = random.uniform(0, 2*math.pi)

        #size object will be when drawn
        self.size = 20

        #used in different creatures to determine how far away
        #it should notice the light (scales apothem length)
        #in object because all moving matter affect by light (I think)
        self.scale = 1

        self.draw()


    #updates last visualized x and y position
    def update_XY(self):
        self.X = self.nextX
        self.Y = self.nextY

  #------------------------Move----------------------------
        #all move functions follow same functionality, only with added
        #functionality to alter heading
    def move(self, apothem, sides):

        #moves object some distance determined by its speed.
        #object will move some amount in x and y direction
        #depending on heading direction
        deltaX = self.distance*math.cos(self.heading)
        deltaY = self.distance*math.sin(self.heading)

        self.nextX += deltaX
        self.nextY += deltaY

        #Determine if is in Arena before continuing
        hits_wall = self.InArena(apothem, sides)
            
        if hits_wall:
            #set X and Y back to last visualized
            self.nextX = self.X
            self.nextY = self.Y
            self.impact(hits_wall)



        #normalize function sets angles between 0 and 2pi
        #for consistency. 0/2pi stares down x axis
        self.normalize_angle(self.heading)


        self.object.setpos(self.nextX, self.nextY)
        self.draw()


  #------------------------Draw----------------------------   
    def draw(self):

        #make sure old object erased
        self.object.clear()
        self.object.dot(self.size)

  #------------------------Track-Zero-Angle----------------
    def update_zero_theta(self):

        #determine angle calculates angle from object to item. Want from item
        #(0,0) to object which will always be difference of pi
        self.zero_theta = math.pi + self.determine_angle(0, 0)
        self.normalize_angle(self.zero_theta)

          
  #------------------------Determin-Angle-------------------       
    #determines angle compared to some item. Used for various purpuses
    def determine_angle(self, *args):

        #allows it to be used for some other object
        if len(args) == 1:
            itemX = args[0].X
            itemY = args[0].Y
            
        #or for some point
        else:
            itemX = args[0]
            itemY = args[1]

        Xdist = abs(self.nextX - itemX)
        Ydist = abs(self.nextY - itemY)

        #prevents division error
        if Xdist == 0:
            
            if self.nextY > itemY:
                theta = -math.pi/2
                return theta
            elif self.nextY < itemY:
                theta = math.pi/2
                return theta

            else:
                #objects are on top of each other
                return self.heading

        theta = abs(math.atan(Ydist/Xdist))

        #item is in quadrants II or III in relation to self
        if self.nextX > itemX:
            theta = math.pi - theta

        #item in quadrants I or II in relation to self
        if self.nextY < itemY:
            return theta

        #item in quadrants III or IV in relation to self
        if self.nextY > itemY:
            return -theta

        #item is on same y value in 0 or pi direction
        return theta       


  #---------------------Determine-Distance----------------------
    #Similar to determine angle. Used to find distance from some object or
    #point.
    def determine_distance(self, *args):

        #if calculating from some object
        if len(args) == 1:
            itemX = args[0].X
            itemY = args[0].Y

        #if calculating from some point
        else:
            itemX = args[0]
            itemY = args[1]

        distance = ((self.nextX - itemX)**2 + (self.nextY - itemY)**2)**(.5)

        return distance
    
  #-----------Determin-Quadrant-Relationship-to-self-----------
    def quadrant_relation(self, *args):

        #if calculating from some object
        if len(args) == 1:
            itemX = args[0].X
            itemY = args[0].Y

        #if calculating from some point
        else:
            itemX = args[0]
            itemY = args[1]

        quadrants = {'XY':1, '-XY':2,'-X-Y':3,'X-Y':4}
        key = ''

        if self.X > itemX:
            key += '-X'
        else:
            key += 'X'

        if self.Y > itemY:
            key += '-Y'
        else:
            key += 'Y'

        return quadrants[key]
            

  #----------------Set-Angle-witin-0-and-2pi------------------     
    def normalize_angle(self, angle):

        while angle > 2*math.pi or angle < 0:
            
            if angle < 0:   
                angle += 2*math.pi

            if angle > 2*math.pi:
                angle -= 2*math.pi

        return angle
    
  #---------------------Check-in-Arena------------------------
    #need to know apothem length and number of sides of arena to calculate
    def InArena(self, apothem, sides):

        #make sure angle from zero is current
        self.update_zero_theta()

        #distance from center
        zero_distance = self.determine_distance(0, 0)

        #apothem is the shortest distance in the arena from the center. If less
        #than, will always be in the arena
        if (zero_distance) < apothem:
            return None

        direct = 1
        #determines which way to 'turn' apothem to determine what
        #area of the polygon object is. Makes finding position faster
        if self.zero_theta > math.pi/2 and self.zero_theta < 3*math.pi/2:
            direct = -1

        #Changes apothem angle by radian distance between each apothem
        dist_between = 2*math.pi/sides
        
        #first apothem is directly down y axis, due to how arena is drawn
        apothem_angle = 3*math.pi/2

        #begin determing object location
        count = 0
        
        while True:

            #Checks if current apothem_angle is weakly the nearest
            #many statements to check if apothem and heading in
            #quadrants I and IV since switches from 2pi to zero at X axis
            #so need to account fo that
            if self.zero_theta >= (apothem_angle-(dist_between/2)) and self.zero_theta <= (apothem_angle+(dist_between/2)):
                break;

            elif (self.zero_theta + 2*math.pi) >= (apothem_angle-(dist_between/2)) and (self.zero_theta + 2*math.pi)  <= (apothem_angle+(dist_between/2)):
                break;
            
            elif (self.zero_theta - 2*math.pi) >= (apothem_angle-(dist_between/2)) and (self.zero_theta - 2*math.pi)  <= (apothem_angle+(dist_between/2)):
                break;
            
            apothem_angle += dist_between*direct

            apothem_angle = self.normalize_angle(apothem_angle)

            #prevent infinite loop in case of error
            if count > sides:
                print('Error InArena', apothem_angle, self.zero_theta)
                break;
                
            count +=1

        #Determine if within arena
        #theta_OI (of interset) Difference betweeen the apothem angle and
        #angle from 0
        theta_OI = abs(self.zero_theta - apothem_angle)

        #if less than zero_distance, object will be on edge. If greater,
        #will be out of arena
        comparative_distance = apothem/math.cos(theta_OI)

        #subtract size so that edge of object won't go out of arena
        if comparative_distance < zero_distance + self.size:
            #info needed to calculate proper collision
            return apothem_angle

        #if in arena return none
        return None

  #------------------If-hits-wall,reflect-properly---------------
    #apothem is length from center perpendicular to side
    def impact(self, apothem_angle):

        self.update_zero_theta()
        apothem_angle = self.normalize_angle(apothem_angle)
        self.normalize_angle(self.heading)

        #90 degree impact with wall
        if apothem_angle == self.heading:
            self.heading += math.pi
            self.normalize_angle(self.heading)
            return

        collision_angle = abs(self.heading - apothem_angle)

        if apothem_angle >= math.pi/2 and apothem_angle <= 3*math.pi/2:
            if self.heading < apothem_angle:
                direct = -1

            else:
                direct = 1

        elif apothem_angle > 3*math.pi/2 and apothem_angle <= 2*math.pi:
            if self.heading < math.pi/2:
                collision_angle = 2*math.pi - collision_angle
                direct = 1
                
            elif self.heading > apothem_angle:
                direct = 1

            elif self.heading < apothem_angle:
                direct = -1
                
        elif apothem_angle < math.pi/2 and apothem_angle >= 0:
            if self.heading > 3*math.pi/2:
                collision_angle = 2*math.pi - collision_angle
                direct = -1
            elif self.heading < apothem_angle:
                direct = -1
            else:
                direct = 1
        else:
            print('Error in impact')



        self.heading += direct*2*(math.pi/2 - collision_angle)
        self.normalize_angle(self.heading)
        
       
        #move forward a space after reflection to avoid
        #getting stuck in place against wall
        deltaX = self.distance*math.cos(self.heading)
        deltaY = self.distance*math.sin(self.heading)
        
        self.nextX += deltaX
        self.nextY += deltaY
        
        return

    
    #finds closest light, passed arena information in kwargs
    #returns light instantiation if sufficiently close
    def find_light(self, **kwargs):

        #if closer than (apothem*self.scale) will notice
        nearest = kwargs['apothem']*self.scale
        nearest_light = None
        
        for light in kwargs['Lights']:
            item_type = self.__str__()
            if item_type == 'Light' and light == kwargs['current_light']:
                continue
            distance = self.determine_distance(light)

            #find closest light
            if distance < nearest:
                nearest = distance
                nearest_light = light
                    
        if nearest_light:
            return nearest_light

        return nearest_light


#---------Creature-Class,-Hold-info-relevant-to-all-creatures------------
class Creatures(Object):

    def __init__(self, speed = 3, attract = True, space = 20):

        Object.__init__(self, speed)
        
        self.space = space
        self.attract = attract
        self.size = 20

    def __str__(self):
        return 'Creature'

    
    #similar to find light, finds closest creature and returns if
    #sufficiently close
    def find_creatures(self, **kwargs):

        #some buffer room to account for object size
        nearest = self.space + self.size/2
        nearest_creature = None
        
        for creature in kwargs['Creatures']:
            #checks that is not finding itself
            if creature == kwargs['current_creature']:
                continue
            distance = self.determine_distance(creature)

            if distance <= nearest:
                nearest = distance
                nearest_creature = creature

        if nearest_creature:
            return nearest_creature
        
        return nearest_creature


    #avoid other objects or a point
    def avoid_item(self, *args):

        quadrant = self.quadrant_relation(*args)
        distance = self.determine_distance(*args)
        angle = self.determine_angle(*args)
        angle = self.normalize_angle(angle)
        self.normalize_angle(self.heading)

        angle_diff = abs(self.heading - angle)
        #take smallest angle difference
        if angle_diff > math.pi:
            angle_diff = 2*math.pi - angle_diff

        direct = 1
        
        #checks relative quadrant of object to decide which way to
        #go to avoid
        if quadrant == 1 or quadrant == 2:
            if self.heading >= angle and self.heading <= angle + math.pi:
                direct = 1
            else:
                direct = -1
        elif quadrant == 3 or quadrant == 4:
            if self.heading <= angle and self.heading >= angle - math.pi:
                direct = -1

            else:
                direct = 1

        #prevents divide by zero error
        if angle_diff == 0:
            angle_diff = 1

        #scale how much objects turn with speed so that they react in
        #time to not collide
        self.heading += direct*8*self.distance/(angle_diff*distance)

        

class Attracted(Creatures):

    def __init__(self, speed = 3, attract = True, space = 20):

        Creatures.__init__(self, speed = 3, attract = True, space = 20)
        
        self.scale = 4/5

        #if gets too close to light, loop away
        self.forget_light = 0
        
    #Attracted creatures approach the light
    def approach_light(self, *args):

        heading = self.heading
        
        distance = self.determine_distance(*args)
        angle = self.determine_angle(*args)
        angle = self.normalize_angle(angle)
        heading = self.normalize_angle(heading)

        angle_diff = abs(heading - angle)
        direct = 1

        #account for if one is in quadrant I and other in quadrant IV
        if (heading - math.pi) < angle or (heading + math.pi) < angle:
            if heading > angle or heading < angle -math.pi:
                direct = -1                 
                                
        self.heading += direct*min(angle_diff*5/distance, angle_diff)
        
    #arena_items is a dictionary of all relevant arena information
    def move(self, arena_items):

        #check for light           
        nearby_light = self.find_light(**arena_items)
        
        #if call returns values
        if nearby_light:

            #if & elif used to avoid sitting on top of light
            #and rather stays around light
            distance = self.determine_distance(nearby_light)
            if self.forget_light > 0:
                pass
            elif distance < 20:
                self.avoid_item(nearby_light)
                self.forget_light = 10
                
            #if not forgetting light, approach              
            else:
                self.approach_light(nearby_light)

        #find nearby creature
        nearby_creature = self.find_creatures(**arena_items)

        #if close, avoid
        if nearby_creature:
            self.avoid_item(nearby_creature)

        #rest similar to Object move function

        #moves object some distance determined by its speed.
        #object will move some amount in x and y direction
        #depending on heading direction
        deltaX = self.distance*math.cos(self.heading)
        deltaY = self.distance*math.sin(self.heading)

        self.nextX += deltaX
        self.nextY += deltaY
        
        #Determine if is in Arena before continuing
        hits_wall = self.InArena(arena_items['apothem'], arena_items['sides'])
            
        if hits_wall:
            self.nextX = self.X
            self.nextY = self.Y
            self.impact(hits_wall)
            self.normalize_angle(self.heading)
        
        self.heading = self.normalize_angle(self.heading)


        self.object.setpos(self.nextX, self.nextY)
        self.forget_light -=1
        self.draw()

    #overide draw function
    def draw(self):

        self.object.clear()
        self.object.color('purple')
        self.object.setheading(math.degrees(self.heading))
        self.object.shape('turtle')
        self.object.stamp()
        self.object.color('dark green')
        self.object.dot(self.size)
        
class Repelled(Creatures):

    def __init__(self, speed = 3, attract = False, space = 20):

        Creatures.__init__(self, speed = 3, attract = False, space = 20)

        self.scale = 3/5

    #overide move, arena_items a dictionary of all relevant arena information      
    def move(self, arena_items):

        nearby_light = self.find_light(**arena_items)

        #similar to attracted only always avoids light if nearby
        if nearby_light:
            #pass info of nearby light
            self.avoid_item(nearby_light)

        #avoid other creatures
        nearby_creature = self.find_creatures(**arena_items)
        if nearby_creature:
            self.avoid_item(nearby_creature)

        #rest similar to Object move

        
        #moves object some distance determined by its speed.
        #object will move some amount in x and y direction
        #depending on heading direction
        deltaX = self.distance*math.cos(self.heading)
        deltaY = self.distance*math.sin(self.heading)

        self.nextX += deltaX
        self.nextY += deltaY

        #Determine if is in Arena before continuing
        hits_wall = self.InArena(arena_items['apothem'], arena_items['sides'])
            
        if hits_wall:
            self.nextX = self.X
            self.nextY = self.Y
            self.impact(hits_wall)
            self.normalize_angle(self.heading)            

        self.heading = self.normalize_angle(self.heading)


        self.object.setpos(self.nextX, self.nextY)
        self.draw()

    #overide draw to draw unique repelled items
    def draw(self):
        
        self.object.clear()
        self.object.color('red')
        self.object.setheading(math.degrees(self.heading))
        self.object.shape('turtle')
        self.object.stamp()
        self.object.color('black')
        self.object.dot(self.size)
                      
#light inherits from object
class Light(Object):

    def __init__(self, speed, random):
        
        Object.__init__(self, speed)
        self.random = random
        self.object.color('yellow', 'red')
        self.size = 30

        #will be changed in move
        self.scale = 1/20

        #moves are small so keep randomize rate low
        #is in tens of a percent (5 = .5% chance of randomly moving
        #per move)
        self.randomize_rate = 5

    def __str__(self):
        return 'Light'

    #overide object move function
    def move(self, arena_items):

        #only redirect light if at edge of other light
        self.scale = self.size/arena_items['apothem']

        if self.random == True:

            self.randomize_rate = 5
               
            if random.randint(1,1000) < self.randomize_rate:
                self.heading = random.uniform(0, 2*math.pi)

        #rest similar to object move

        #moves object some distance determined by its speed.
        #object will move some amount in x and y direction
        #depending on heading direction
        deltaX = self.distance*math.cos(self.heading)
        deltaY = self.distance*math.sin(self.heading)
        
        self.nextX += deltaX
        self.nextY += deltaY

        #Determine if is in Arena before continuing

        hits_wall = self.InArena(arena_items['apothem'], arena_items['sides'])

        #if hits wall, priority over hitting light, return           
        if hits_wall:
            self.nextX = self.X
            self.nextY = self.Y
            self.impact(hits_wall)
            self.object.setpos(self.nextX, self.nextY)
            self.draw()
            return

        nearby_light = self.find_light(**arena_items)

        #act as if wall
        if nearby_light:
            self.nextX = self.X
            self.nextY = self.Y
            angle = self.determine_angle(nearby_light)
            self.impact(angle)       


        self.object.setpos(self.nextX, self.nextY)
        self.draw()

    #overide draw function to draw distinguishable lights       
    def draw(self):

        self.object.clear()
        self.object.ht()
        self.object.pu()
        self.object.dot(self.size)

        




    
        
        
