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
        self.h_size = randint(int(x/10), int(y/5.5))

        self.b_length = randint(int(-y/18),int(y/10))
        self.leg_length = randint(int(y/14),int(y/10))
        self.arm_length = self.leg_length
        self.feet_length = randint(15,40)

        self.arm_angles = (randint(-60, 75), randint(-60, 75))
        self.eye_angles = [(-90, 90), (90, -90)]
        self.finger_angles = [0,50,-50]
        self.leg_angle = randint(75,90)
        
        self.arm_yoff = int(self.c[1]+size[1]/18)
        self.leg_xoff = self.b_size/8
        self.eye_xoff = self.h_size/5
        self.eye_circle = bool(randint(0,3))
        self.stroke = (randint(0,255),255,90)
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
        self.draw_eyes()

    def draw_body(self):
        self.draw.polygon(self.b_points,self.rand_pastel(),self.stroke)
        self.polygon(self.b_points,self.stroke, self.width)
        self.draw_limbs()

    def draw_eyes(self):
        eye_r = self.h_size/5.25
        eyebrows = choice(self.eyebrows)

        for i in range(2):
            eye_x = self.eye_xoff if bool(i) else -self.eye_xoff
            eye_pos = (self.c[0] - eye_x, self.c[1] - self.h_size)
            if self.eye_circle:
                self.ellipse(eye_pos, eye_r)
            else:
                self.draw.rectangle(self.bound(eye_pos, eye_r), (0,0,255), self.stroke, self.width-2)

            # Puplis
            angles = choice(self.eye_angles)
            self.draw.chord(self.bound(eye_pos, eye_r-5), angles[0], angles[1], (0,0,0))

            # Eyebrows
            self.draw.line(eyebrows(eye_pos[0],eye_pos[1]-self.h_size/3.5)[i],self.stroke, self.width)

    def draw_limbs(self):
        # Arms & fingers
        for i in range(2):
            arm = self.arm_points(self.arm_angles[i], self.arm_length, bool(i))
            self.draw.line(arm, self.stroke, self.width)
            for j in range(0,3):
                self.draw.line([arm[1], self.limb_point(arm[1], self.arm_angles[i]+self.finger_angles[j], 15, bool(i))], self.stroke, self.width-1)

        # Legs & feet
        for i in range(2):
            leg = self.leg_points(self.leg_angle, self.leg_length, bool(i))
            self.draw.line(leg, self.stroke, self.width)
            self.draw.line([leg[1], self.limb_point(leg[1], self.leg_angle-90, self.feet_length,bool(i))], self.stroke, self.width)
        
    def draw_border(self):
        self.draw.line([(0,0), (self.size[0],0)], self.stroke, self.border_width)
        self.draw.line([(self.size[0],0), (self.size[0],self.size[1])], self.stroke, self.border_width)
        self.draw.line([(self.size[0],self.size[1]), (0,self.size[1])], self.stroke, self.border_width)
        self.draw.line([(0,self.size[1]), (0,0)], self.stroke, self.border_width)

    
    # Helper functions
    def arm_points(self, angle, length, right):
        r = range(self.size[0]-1)
        for x in reversed(r) if right else r:
            if self.pixels[x, self.arm_yoff] == self.stroke:
                return [(x, self.arm_yoff), self.limb_point((x, self.arm_yoff), angle, length, right)]

    def leg_points(self, angle, length, right):
        x = self.c[0] + (self.leg_xoff if right else -self.leg_xoff)
        for y in reversed(range(self.size[1]-1)):
            if self.pixels[x, y] == self.stroke:
                return [(x, y), self.limb_point((x, y), angle, length, right)]

    def ellipse(self, c, r):
        self.draw.ellipse(self.bound(c, r), (0,0,255), self.stroke, self.width-2)

    def bound(self, c, r):
        return [(c[0] - r, c[1] - r), (c[0] + r, c[1] + r)]

    def polygon(self, points, fill, width):
        self.draw.line([points[0],points[len(points)-1]],fill,width)
        for i in range(len(points)-1):
            self.draw.line([points[i],points[i+1]],fill,width)

    def limb_point(self, p, deg, dis, right):
        x, y = int(dis*cos(radians(deg))), int(dis*sin(radians(deg)))+p[1]
        return (x+p[0] if right else -x+p[0], y)

    def rand_pastel(self):
        return (randint(0,255),80,255)