from random import randint, choice, seed
from math import *
from PIL import Image, ImageDraw, ImageFont

class PolyFriendGenerator:
    def __init__(self, size, width, names, font_name, save_name, seed=""):
        if seed != "":
            seed(seed)
        self.image = Image.new("HSV",size,self.rand_pastel())
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype(font_name, 75)
        self.name = choice([s.replace('\n','') for s in names.readlines()])
        self.pixels = self.image.load()
        self.size = size
        self.width = width
        self.c = (size[0]/2, size[1]/2)

        # Sizes and lengths are ratios of the image dimensions to preserve the same look.
        x, y = size[0], size[1]
        self.b_size = randint(int(x/17), int(y/9))
        self.h_size = randint(int(x/10), int(size[1]/5.5))

        self.b_length = randint(int(-y/18),int(y/10))
        self.leg_length = randint(int(y/14),int(y/10))
        self.arm_length = self.leg_length
        self.feet_length = randint(15,40)

        self.arm_angles = (randint(-60, 75), randint(-60, 75))
        self.eye_angles = [(-90, 90), (90, -90)]
        self.finger_angles = [0,50,-50]
        self.leg_angle = randint(75,90)
        
        self.stroke = (randint(0,255),255,90)
        self.arm_y = int(self.c[1]+size[1]/18)
        self.border_width = 40

        c1, c2 = cos(2*pi/5), -cos(pi/5)
        s1, s2 = sin(2*pi/5), sin(4*pi/5)
        h, b = self.h_size, self.b_size
        self.head_shapes = [
            # Squares
            lambda x,y: [(x-h,y-h), (x+h,y-h), (x+h,y+h), (x-h,y+h)],
            lambda x,y: [(x,y-h), (x+h,y), (x,y+h), (x-h,y)],
            # Triangle
            lambda x,y: [(x,y-h), (x-h,y+h), (x+h,y+h)],
            # Upside down Triangle
            lambda x,y: [(x,y+h), (x-h*1.5,y-h), (x+h*1.5,y-h)],
            # Trapezoid
            lambda x,y: [(x-h/1.5,y-h/1.5), (x+h/1.5,y-h/1.5), (x+h,y+h), (x-h,y+h)],
            # Upside down Pentagon
            lambda x,y: [(x,y+h), (x+h*s1,y+h*c1), (x+h*s2,y+h*c2), (x-h*s2,y+h*c2), (x-h*s1,y+h*c1)],
            # Rhombus
            lambda x,y: [(x,y-h), (x+h*1.5,y), (x,y+h), (x-h*1.5,y)],
        ]
        self.body_shapes = [
            # Trapezoid
            lambda x,y,l: [(x-b/4,y), (x+b/4,y), (x+b,y+b*2+l), (x-b,y+b*2+l)],
            # Upside down trapezoid
            lambda x,y,l: [(x-b/1.5,y), (x+b/1.5,y), (x+b/4,y+b*2+l), (x-b/4,y+b*2+l)],
            # Square
            lambda x,y,l: [(x-b/2,y), (x+b/2,y), (x+b/2,y+b*2+l), (x-b/2,y+b*2+l)],
            # Kite
            lambda x,y,l: [(x-b/4,y), (x+b/4,y), (x+b/2,y+b*1.5+l), (x,y+b*2+l), (x-b/2,y+b*1.5+l)],
            # Diamond
            lambda x,y,l: [(x,y+b*2+l), (x+b*s1,y+b*c1), (x+b*s2,y), (x-b*s2,y), (x-b*s1,y+b*c1)]
        ]
        self.eyebrows = [
            lambda x,y: [[],[]],
            lambda x,y: [[(x-h/10,y-h/15),(x+h/10,y+h/20)],[(x-h/10,y+h/20),(x+h/10,y-h/15)]],
            lambda x,y: [[(x-h/10,y+h/15),(x+h/10,y-h/20)],[(x-h/10,y-h/20),(x+h/10,y+h/15)]],
            lambda x,y: [[(x-h/10,y),(x+h/10,y)],[(x-h/10,y),(x+h/10,y)]]
        ]
        self.h_points = choice(self.head_shapes)(self.c[0], self.c[1]-h)
        self.b_points = choice(self.body_shapes)(self.c[0], self.c[1], 100)

    def save_image(self):
        self.image = self.image.convert(mode="RGB")
        self.image.save("img.png", "PNG")
    
    def generate_image(self):   
        self.draw_head()
        self.draw_body()
        self.draw_border()

        self.draw.text((self.border_width,self.border_width), self.name, self.stroke, self.font)

    # Draw functions
    def draw_head(self):
        self.draw.polygon(self.h_points, self.rand_pastel(), self.stroke)
        self.polygon(self.h_points, self.stroke, self.width)
        self.draw_eyes((self.c[0], self.c[1] - self.h_size))

    def draw_body(self):
        self.draw.polygon(self.b_points,self.rand_pastel(),self.stroke)
        self.polygon(self.b_points,self.stroke, self.width)
        self.draw_limbs()

    def draw_eyes(self, loc):
        eye_r = self.h_size/5.25
        left = (loc[0] - self.h_size/5, loc[1])
        right = (loc[0] + self.h_size/5, loc[1])

        self.ellipse(left, eye_r)
        self.ellipse(right, eye_r)

        l_angles, r_angles = choice(self.eye_angles), choice(self.eye_angles)
        self.draw.chord(self.bound(left, eye_r-5), l_angles[0], l_angles[1], (0,0,0))
        self.draw.chord(self.bound(right, eye_r-5), r_angles[0], r_angles[1], (0,0,0))

        self.draw_eyebrows(left, right)

    def draw_eyebrows(self, left, right):
        eyebrows = choice(self.eyebrows)
        self.draw.line(eyebrows(left[0],left[1]-self.h_size/3.5)[0],self.stroke, self.width)
        self.draw.line(eyebrows(right[0],right[1]-self.h_size/3.5)[1],self.stroke, self.width)

    def draw_limbs(self):
        # Arms
        l_arm = self.arm_points(range(self.size[0]-1), self.arm_angles[0], self.arm_length, self.arm_y, False)
        r_arm = self.arm_points(reversed(range(self.size[0]-1)), self.arm_angles[1], self.arm_length, self.arm_y, True)
        self.draw.line(l_arm,self.stroke, self.width)
        self.draw.line(r_arm,self.stroke, self.width)

        # Fingers
        for i in range(0,3):
            self.draw.line([l_arm[1],self.limb_point(l_arm[1],self.arm_angles[0]+self.finger_angles[i],15,False)], self.stroke, self.width-1)
            self.draw.line([r_arm[1],self.limb_point(r_arm[1],self.arm_angles[1]+self.finger_angles[i],15,True)], self.stroke, self.width-1)

        # Legs
        l_leg = self.leg_points(self.leg_angle, self.leg_length, self.c[0]-self.b_size/8, False)
        r_leg = self.leg_points(self.leg_angle, self.leg_length, self.c[0]+self.b_size/8, True)
        self.draw.line(l_leg, self.stroke, self.width)
        self.draw.line(r_leg, self.stroke, self.width)
        self.draw.line([l_leg[1], self.limb_point(l_leg[1],self.leg_angle-90,self.feet_length,False)], self.stroke, self.width)
        self.draw.line([r_leg[1], self.limb_point(r_leg[1],self.leg_angle-90,self.feet_length,True)], self.stroke, self.width)

    def arm_points(self, range, angle, length, arm_y, right):
        for x in range:
            if self.pixels[x, arm_y] == self.stroke:
                return [(x, arm_y), self.limb_point((x, arm_y), angle, length, right)]

    def leg_points(self, angle, length, leg_x, right):
        for y in reversed(range(self.size[1]-1)):
            if self.pixels[leg_x, y] == self.stroke:
                return [(leg_x, y), self.limb_point((leg_x, y), angle, length, right)]

    def draw_border(self):
        self.draw.line([(0,0), (self.size[0],0)], self.stroke, self.border_width)
        self.draw.line([(self.size[0],0), (self.size[0],self.size[1])], self.stroke, self.border_width)
        self.draw.line([(self.size[0],self.size[1]), (0,self.size[1])], self.stroke, self.border_width)
        self.draw.line([(0,self.size[1]), (0,0)], self.stroke, self.border_width)

    
    # Helper functions
    def ellipse(self, c, r):
        self.draw.ellipse(self.bound(c, r), (0,0,255), self.stroke, self.width-2)

    def bound(self, c, r):
        return [(c[0] - r, c[1] - r), (c[0] + r, c[1] + r)]

    def polygon(self, points, fill, width):
        self.draw.line([points[0],points[len(points)-1]],fill,width)
        for i in range(len(points)-1):
            self.draw.line([points[i],points[i+1]],fill,width)

    def limb_point(self, p, deg, dis, right):
        x, y = cos(radians(deg)), sin(radians(deg))
        return (int(dis*x)+p[0] if right else -int(dis*x)+p[0], int(dis*y)+p[1])

    def rand_pastel(self):
        return (randint(0,255),80,255)