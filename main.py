import pygame
from pymunk.pygame_util import to_pygame
from unicodedata import category

pygame.font.init()
import pymunk as pym
import numpy as n
import pickle
import time as t
import random as r

pygame.init()

# Setup Pymunk Space
space = pym.Space()
space.gravity = (0, 500)
space.iterations = 30
imaginary_space = pym.Space()
imaginary_space.gravity = (0, 0)

ball_collision_type = 1
bounce_collision_type = 2

# Setup Pygame Screen
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 600))
control_panel = pygame.Surface((160, 1000))
pygame.display.set_caption("Machine")

# each block

class module:

    def __init__(self, xsize, ysize, pos, name=None, channels=4):
        self.xsize = xsize*400
        self.ysize = ysize*300
        self.pos = pos

        #Bodies

        self.BodyTop = pym.Body(body_type=pym.Body.STATIC)
        self.BodyTop.position = (pos[0] * 800 - 400, pos[1] * 600 - 598)
        self.BodyBottom = pym.Body(body_type=pym.Body.STATIC)
        self.BodyBottom.position = (pos[0] * 800 - 400, pos[1] * 600-2)
        self.BodyRight = pym.Body(body_type=pym.Body.STATIC)
        self.BodyRight.position = (pos[0] * 800, pos[1] * 600 - 300)
        self.BodyLeft = pym.Body(body_type=pym.Body.STATIC)
        self.BodyLeft.position = (pos[0] * 800 - 797.5, pos[1] * 600 - 300)

        #planks and wheels
        module_data = []
        if name:
            module_data = find_save_file(name)

        try:
            self.planks, self.wheels, self.cushions, self.fans, self.blackholes, self.inputs, self.outputs = module_data
        except TypeError:
            self.planks, self.wheels, self.cushions, self.fans, self.blackholes = [], [], [], [], []
            inputsoutputs = generateInputsOutputs(channels)
            self.inputs = inputsoutputs[0]
            self.outputs = inputsoutputs[1]
        except ValueError:
            self.planks, self.wheels, self.cushions, self.fans, self.blackholes = [], [], [], [], []
            inputsoutputs = generateInputsOutputs(channels)
            self.inputs = inputsoutputs[0]
            self.outputs = inputsoutputs[1]

        for plank in self.planks:
            plank.init()
        for wheel in self.wheels:
            wheel.init()
        for cushion in self.cushions:
            cushion.init()
        for fan in self.fans:
            fan.init()
        for BH in self.blackholes:
            BH.init()

        #holes

        self.inputstop = []
        self.inputsright = []
        self.inputsleft = []
        self.inputsbottom = []

        for input in self.inputs:
            if input[0] == "top":
                self.inputstop.append(input)
            if input[0] == "right":
                self.inputsright.append(input)
            if input[0] == "left":
                self.inputsleft.append(input)
            if input[0] == "bottom":
                self.inputsbottom.append(input)

        self.outputstop = []
        self.outputsright = []
        self.outputsleft = []
        self.outputsbottom = []

        for output in self.outputs:
            if output[0] == "top":
                self.outputstop.append(output)
            if output[0] == "right":
                self.outputsright.append(output)
            if output[0] == "left":
                self.outputsleft.append(output)
            if output[0] == "bottom":
                self.outputsbottom.append(output)

        holesTop = self.outputstop #+ self.inputstop
        holesBottom = self.outputsbottom #+ self.inputsbottom
        holesRight = self.outputsright #+ self.inputsright
        holesLeft = self.outputsleft #+ self.inputsleft

        walltoppoints = [[(-200*xsize, 2.5), (-200*xsize, -2.5)]]
        for i in range(0, len(holesTop)):
            walltoppoints[i].append((holesTop[i][1]-200*xsize, -2.5))
            walltoppoints[i].append((holesTop[i][1]-200*xsize, 2.5))
            walltoppoints.append([(holesTop[i][2]-200*xsize, 2.5), (holesTop[i][2]+(-200*xsize), -2.5)])
        walltoppoints[len(walltoppoints)-1].append((200*xsize, -2.5))
        walltoppoints[len(walltoppoints) - 1].append((200*xsize, 2.5))

        wallbottompoints = [[(-200 * xsize, 2.5), (-200 * xsize, -2.5)]]
        for i in range(0, len(holesBottom)):
            wallbottompoints[i].append((holesBottom[i][1]-(200*xsize), -2.5))
            wallbottompoints[i].append((holesBottom[i][1]-(200*xsize), 2.5))
            wallbottompoints.append([(holesBottom[i][2]-(200*xsize), 2.5), (holesBottom[i][2] + (-200*xsize), -2.5)])
        wallbottompoints[len(wallbottompoints) - 1].append((200 * xsize, -2.5))
        wallbottompoints[len(wallbottompoints) - 1].append((200 * xsize, 2.5))

        wallrightpoints = [[(2.5, -150 * ysize), (-2.5, -150 * ysize)]]
        for i in range(0, len(holesRight)):
            wallrightpoints[i].append((-2.5, holesRight[i][1] - 150 * ysize))
            wallrightpoints[i].append((2.5, holesRight[i][1] - 150 * ysize))
            wallrightpoints.append([(2.5, holesRight[i][2] - 150 * ysize), (-2.5, holesRight[i][2] - 150 * ysize)])
        wallrightpoints[len(wallrightpoints) - 1].append((-2.5, 150 * ysize))
        wallrightpoints[len(wallrightpoints) - 1].append((2.5, 150 * ysize))

        wallleftpoints = [[(2.5, -150 * ysize), (-2.5, -150 * ysize)]]
        for i in range(0, len(holesLeft)):
            wallleftpoints[i].append((-2.5, holesLeft[i][1] - 150 * ysize))
            wallleftpoints[i].append((2.5, holesLeft[i][1] - 150 * ysize))
            wallleftpoints.append([(2.5, holesLeft[i][2] - 150 * ysize), (-2.5, holesLeft[i][2] - 150 * ysize)])
        wallleftpoints[len(wallleftpoints) - 1].append((-2.5, 150 * ysize))
        wallleftpoints[len(wallleftpoints) - 1].append((2.5, 150 * ysize))

        #generating shapes

        self.wallTopPYMpolys = [pym.Poly(self.BodyTop, rect) for rect in walltoppoints]
        self.wallBottomPYMpolys = [pym.Poly(self.BodyBottom, rect) for rect in wallbottompoints]
        self.wallRightPYMpolys = [pym.Poly(self.BodyRight, rect) for rect in wallrightpoints]
        self.wallLeftPYMpolys = [pym.Poly(self.BodyLeft, rect) for rect in wallleftpoints]

        for shape in self.wallTopPYMpolys:
            shape.elasticity = 1
        for shape in self.wallBottomPYMpolys:
            shape.elasticity = 1
        for shape in self.wallRightPYMpolys:
            shape.elasticity = 1
        for shape in self.wallLeftPYMpolys:
            shape.elasticity = 1

        #adding to space

        space.add(self.BodyTop, *self.wallTopPYMpolys)
        space.add(self.BodyBottom, *self.wallBottomPYMpolys)
        space.add(self.BodyRight, *self.wallRightPYMpolys)
        space.add(self.BodyLeft, *self.wallLeftPYMpolys)

        self.PYMpolys = self.wallTopPYMpolys + self.wallBottomPYMpolys + self.wallRightPYMpolys + self.wallLeftPYMpolys
        self.PYMpoints = walltoppoints + wallbottompoints + wallrightpoints + wallleftpoints

        self.generate_checkpoints_and_generators()

    def generate_checkpoints_and_generators(self):
        self.checkpoints = []
        self.generators = []

        for data in self.outputsbottom:
            self.checkpoints.append(BallCheckpoint(data[1], self.BodyBottom.position[1] - 2, 15, 5, data[3]))
        for data in self.outputstop:
            self.checkpoints.append(BallCheckpoint(data[1], self.BodyTop.position[1] - 2, 15, 5, data[3]))
        for data in self.outputsright:
            self.checkpoints.append(BallCheckpoint(self.BodyRight.position[0] - 2, data[1], 5, 15,  data[3]))
        for data in self.outputsleft:
            self.checkpoints.append(BallCheckpoint(self.BodyLeft.position[0] - 2, data[1], 5, 15,  data[3]))

        for data in self.inputsbottom:
            self.generators.append(ballGenerator(data[3], data[1]+7.5, self.BodyBottom.position[1] - 2, 0, -60, 90))
        for data in self.inputstop:
            self.generators.append(ballGenerator(data[3], data[1]+7.5, self.BodyTop.position[1] + 2, 0, 60, 90))
        for data in self.inputsright:
            self.generators.append(ballGenerator(data[3], self.BodyRight.position[0] - 2, data[1]+7.5, -60, 0, 90))
        for data in self.inputsleft:
            self.generators.append(ballGenerator(data[3], self.BodyLeft.position[0] + 2, data[1] + 7.5, 60, 0, 90))

    def draw_and_update(self):
        for blackhole in self.blackholes:
            blackhole.drawField()
        for fan in self.fans:
            fan.draw_field()
        for blackhole in self.blackholes:
            blackhole.draw(screen)
        for fan in self.fans:
            fan.draw()
        for polygon in self.PYMpolys:
            pygame.draw.polygon(screen, (100, 100, 100), [to_pygame(polygon.body.local_to_world(p)) for p in polygon.get_vertices()])
        for check in self.checkpoints:
            check.draw(screen)
        for gen in self.generators:
            gen.makeBall(frame)
        for plank in self.planks:
            plank.draw(screen)
        for wheel in self.wheels:
            wheel.draw(screen)
        for cushion in self.cushions:
            cushion.draw(screen)


class button:
    def __init__(self, rect, text, color, surface_rect, fontSize=24):
        self.rect = rect
        self.text = text
        self.color = color
        self.fontSize = fontSize
        self.surface_rect = surface_rect

    def get_isClicked(self):
        hitbox = pygame.Rect(self.surface_rect.left+self.rect.left,self.surface_rect.top+self.rect.top , self.rect.width, self.rect.height)
        print(self.rect)
        print(self.surface_rect)
        print(hitbox)
        print(hitbox.collidepoint(pygame.mouse.get_pos()))
        return hitbox.collidepoint(pygame.mouse.get_pos())

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text(self.text, surface, self.fontSize, self.rect.center, (200, 200, 200), self.color)

class BallCheckpoint:
    def __init__(self, x, y, l, w, color):
        self.color = color
        self.pos = (x, y)
        if self.color == "green":
            self.RGBcolor = (0, 1, 0)
        if self.color == "red":
            self.RGBcolor = (1, 0, 0)
        if self.color == "blue":
            self.RGBcolor = (0, 0, 1)
        if self.color == "yellow":
            self.RGBcolor = (1, 1, 0)
        self.rect = pygame.Rect(x, y, l, w)
        self.middle = self.rect.center
        self.brightness = 51
        self.powered = False

    def draw(self, surface):
        drawingrect = self.rect.copy()
        drawingrect.center = to_pygame(self.rect.center)
        pygame.draw.rect(surface, [v*self.brightness for v in self.RGBcolor], drawingrect)
        if self.brightness > 50:
            self.brightness -= 0.1
        for num, ball in enumerate(balls):
            if (((ball.ballBody.position[0]-self.middle[0])**2)+((ball.ballBody.position[1]-self.middle[1])**2)) <= 100:
                try:
                    space.remove(balls[num].ballBody, balls[num].ball)
                    balls.pop(num)
                    if ball.color == self.color:
                        if self.brightness < 195:
                            self.brightness += 60
                        else:
                            self.brightness = 255
                    else:
                        if self.brightness > 50:
                            self.brightness -= 20
                        else:
                            self.brightness = 30
                except AssertionError:
                    pass
        if self.brightness >= 150:
            self.powered = True

class Cushion:
    def __init__(self, x, y, angle):
        self.Body = pym.Body(body_type=pym.Body.KINEMATIC)
        self.Body.position = (x, y)
        self.Body.angle = n.radians(angle)
        s = 5
        self.PYMvert = [(-6*s, 0.5*s),(-4.5*s, 1*s),(0*s, 1.5*s),(4.5*s, 1*s),(6*s, 0.5*s),
                        (6*s, -0.5*s),(4.5*s, -1*s),(0*s, -1.5*s),(-4.5*s, -1*s),(-6*s, -0.5*s)]
        self.PYMpoly = pym.Poly(self.Body, self.PYMvert)
        self.PYMpoly.elasticity = 0.2
        space.add(self.Body, self.PYMpoly)
        self.jolt = False

    def init(self):
        try:
            space.add(self.Body, self.PYMpoly)
        except AssertionError:
            pass

    def draw(self, surface):
        if r.randint(0, 10) == 1 and not(self.jolt):
            self.Body.position += (0, 0.1)
            self.jolt = True
        elif self.jolt:
            self.Body.position -= (0, 0.1)
            self.jolt = False
        self.PYGvert = [to_pygame(self.PYMpoly.body.local_to_world(vert)) for vert in self.PYMvert]
        self.PYGpoly = pygame.draw.polygon(screen, (100, 100, 100), self.PYGvert)
        pygame.draw.polygon(screen, (100, 100, 100), self.PYGvert)

    def updatePYM(self, vel, ang):
        if vel is not None:
            self.Body.position = vel
        if ang is not None:
            self.Body.angle = ang

    def delete(self):
        space.remove(self.Body, self.PYMpoly)

class Wheel:
    def __init__(self, x, y):
        self.rotationSpeed = 2
        self.Body = pym.Body(body_type=pym.Body.KINEMATIC)
        self.Body.position = (x,y)
        self.Body.angular_velocity = self.rotationSpeed
         #self.PYMvert = ((1.73, 1),(12, 1),(12, -1),(1.73, -1),(6.86, -9.9),(5.14, -10.9), (0,-2),(-5.14, -10.86),
        #              (-6.86, -9.89),(-1.73, -.99),(-12, -1),(-12, 1), (-1.73, 1),(-6.86, 9.88),(-5.13,10.9),
        #               (0, 2),(5.14, 10.9),(6.86, 9.89))
        s = 4
        self.PYMvert = [[(1.73*s, 1*s),(12*s, 1*s),(12*s, -1*s),(1.73*s, -1*s), (0,0)],
                        [(1.73*s, -1*s),(6.86*s, -9.9*s),(5.14*s, -10.9*s), (0,-2*s), (0,0)],
                        [(0*s,-2*s),(-5.14*s, -10.86*s),(-6.86*s, -9.89*s),(-1.73*s, -.99*s), (0,0)],
                        [(-1.73*s, 1*s),(-6.86*s, 9.88*s),(-5.13*s,10.9*s),(0*s, 2*s), (0,0)],
                        [(0*s, 2*s),(5.14*s, 10.9*s),(6.86*s, 9.89*s),(1.73*s, 1*s), (0,0)],
                        [(-1.73*s, -.99*s),(-12*s, -1*s),(-12*s, 1*s), (-1.73*s, 1*s),(0,0)]]

        self.PYMpolys = [pym.Poly(self.Body, poly, None, 0.5) for poly in self.PYMvert]
        space.add(self.Body, self.PYMpolys[0], self.PYMpolys[1], self.PYMpolys[2], self.PYMpolys[3], self.PYMpolys[4], self.PYMpolys[5])

    def init(self):
        try:
            space.add(self.Body, self.PYMpolys[0], self.PYMpolys[1], self.PYMpolys[2], self.PYMpolys[3], self.PYMpolys[4], self.PYMpolys[5])
        except AssertionError:
            pass

    def draw(self, surface):
        self.PYGvert = []
        for poly in self.PYMpolys:
            verts = []
            for vert in poly.get_vertices():
                verts.append(to_pygame(poly.body.local_to_world(vert)))
            self.PYGvert.append(verts)
        self.PYGpoly = [pygame.draw.polygon(screen, (100, 100, 100), poly) for poly in self.PYGvert]
        # Draw rotated plank
        for poly in self.PYGvert:
            pygame.draw.polygon(surface, (100, 100, 100), poly)

    def updatePYM(self, val, ang):
        if val != None:
            self.Body.position = val

    def delete(self):
        space.remove(self.Body, self.PYMpolys[0], self.PYMpolys[1], self.PYMpolys[2], self.PYMpolys[3], self.PYMpolys[4], self.PYMpolys[5])

class Plank:
    def __init__(self, x, y, angle):
        self.angle = n.radians(angle)
        self.Body = pym.Body(body_type=pym.Body.KINEMATIC)
        self.p = pym.Poly.create_box(self.Body, (100, 10), 0.5)
        self.p.elasticity = 1
        self.Body.position = (x, y)
        self.Body.angle = self.angle
        space.add(self.Body, self.p)
        self.vertices = [to_pygame(self.Body.local_to_world(v)) for v in self.p.get_vertices()]
        self.PYGpoly = pygame.draw.polygon(screen, (100, 100, 100), self.vertices)
        self.jolt = False
        self.p.friction = 0

    def init(self):
        try:
            space.add(self.Body, self.p)
        except AssertionError:
            pass

    def draw(self, surface):
        if r.randint(0, 5) == 1 and not(self.jolt):
            self.Body.position += (0.1, 0)
            self.jolt = True
        elif self.jolt:
            self.Body.position -= (0.1, 0)
            self.jolt = False
        # Draw rotated plank

        self.vertices = [to_pygame(self.Body.local_to_world(v)) for v in self.p.get_vertices()]
        self.PYGpoly = pygame.draw.polygon(surface, (100, 100, 100), self.vertices)

    def updatePYM(self, vel, ang):
        if vel is not None:
            self.Body.position = vel
        if ang is not None:
            self.Body.angle = ang

    def delete(self):
        space.remove(self.Body, self.p)

class Fan:
    def __init__(self, x, y, angle, force, length):
        self.willDrawField = False
        self.force = force
        self.length = length
        self.angle = n.radians(angle)
        self.Body = pym.Body(body_type=pym.Body.KINEMATIC)
        self.PYMvert = [(7.5, -15.0), (7.5, 7.5), (30.0, 7.5), (30.0, 15.0),
                        (-30.0, 15.0), (-30.0, 7.5), (-7.5, 7.5), (-7.5, -15.0)]
        self.PYMpoly = pym.Poly(self.Body, self.PYMvert, None, 0.5)
        self.Body.position = (x, y)
        self.Body.angle = self.angle
        self.imaginary_body = pym.Body(body_type=pym.Body.KINEMATIC)
        self.imaginary_body.position = (x, y)
        self.imaginary_body.angle = self.angle
        self.imaginary_PYMpoly = [(30, 15), (30, 15+length), (-30, 15+length), (-30, 15)]
        self.imaginary_shape = pym.Poly(self.imaginary_body, self.imaginary_PYMpoly,
                                        None, 0.5)
        space.add(self.Body, self.PYMpoly)
        imaginary_space.add(self.imaginary_body, self.imaginary_shape)

        self.FieldPYGvert = [to_pygame(self.PYMpoly.body.local_to_world(vert)) for vert in self.imaginary_PYMpoly]
        print(self.FieldPYGvert)
        self.FieldPYGpoly = pygame.draw.polygon(screen, (100, 100, 100), self.FieldPYGvert)

        self.PYGvert = [to_pygame(vert) for vert in self.PYMvert]
        self.PYGpoly = pygame.draw.polygon(screen, (100, 100, 100), self.PYGvert)

        self.jolt = False

    def init(self):
        try:
            space.add(self.Body, self.PYMpoly)
            imaginary_space.add(self.imaginary_body, self.imaginary_shape)
        except AssertionError:
            pass

    def draw(self):
        if r.randint(0, 10) == 1 and not(self.jolt):
            self.Body.position += (0, 0.1)
            self.jolt = True
        elif self.jolt:
            self.Body.position -= (0, 0.1)
            self.jolt = False
        self.FieldPYGvert = [to_pygame(self.PYMpoly.body.local_to_world(vert)) for vert in self.imaginary_PYMpoly]
        self.FieldPYGpoly = pygame.draw.polygon(screen, (100, 100, 100), self.PYGvert)
        self.PYGvert = [to_pygame(self.PYMpoly.body.local_to_world(vert)) for vert in self.PYMvert]
        self.PYGpoly = pygame.draw.polygon(screen, (100, 100, 100), self.PYGvert)
        for ball_ in balls:
            pos = ball_.ballBody.position
            if self.imaginary_shape.point_query(pos).distance <= 0:
                force = (self.force*n.cos(self.Body.angle+(3.141/2)), self.force*n.sin(self.Body.angle+(3.141/2)))
                ball_.ballBody.apply_force_at_local_point(force)

    def fieldDrawToggle(self):
        if self.willDrawField:
            self.willDrawField = False
        else:
            self.willDrawField = True

    def draw_field(self):
        if self.willDrawField:
            pygame.draw.polygon(screen, (50, 50, 50), self.FieldPYGvert)

    def updatePYM(self, pos, angle):
        if pos:
            self.Body.position = pos
            self.imaginary_body.position = pos
        if angle:
            self.Body.angle = angle - (3.141/2)
            self.imaginary_body.angle = angle - (3.141/2)
        imaginary_space.step(1/60)
        self.FieldPYGvert = [to_pygame(self.PYMpoly.body.local_to_world(vert)) for vert in self.imaginary_PYMpoly]
        self.FieldPYGpoly = pygame.draw.polygon(screen, (100, 100, 100), self.PYGvert)

        self.PYGvert = [to_pygame(self.PYMpoly.body.local_to_world(vert)) for vert in self.PYMvert]
        self.PYGpoly = pygame.draw.polygon(screen, (100, 100, 100), self.PYGvert)

    def delete(self):
        try:
            space.remove(self.Body, self.PYMpoly)
            imaginary_space.remove(self.imaginary_body, self.imaginary_shape)
        except AssertionError:
            pass

class ball:
    def __init__(self, color, xpos, ypos, frame):
        self.startFrame = frame
        self.color = color
        if self.color == "red":
            self.ballBody = pym.Body(5, 5, body_type=pym.Body.DYNAMIC)
            self.ballBody.position = (xpos, ypos)
            self.ball = pym.Circle(self.ballBody, 6)
            self.ball.elasticity = 0.9
            self.maxSpeed = 900
            self.RGB = (255, 0, 0)
        if self.color == "green":
            self.ballBody = pym.Body(15, 15, body_type=pym.Body.DYNAMIC)
            self.ballBody.position = (xpos, ypos)
            self.ball = pym.Circle(self.ballBody, 6)
            self.ball.elasticity = 0.5
            self.maxSpeed = 900
            self.RGB = (0, 255, 0)
        if self.color == "blue":
            self.ballBody = pym.Body(5, 5, body_type=pym.Body.DYNAMIC)
            self.ballBody.position = (xpos, ypos)
            self.ball = pym.Circle(self.ballBody, 6)
            self.ball.elasticity = 0.2
            self.maxSpeed = 900
            self.RGB = (0, 0, 255)
        if self.color == "yellow":
            self.ballBody = pym.Body(1, 1, body_type=pym.Body.DYNAMIC)
            self.ballBody.position = (xpos, ypos)
            self.ball = pym.Circle(self.ballBody, 6)
            self.ball.elasticity = 0.5
            self.maxSpeed = 900
            self.RGB = (255, 255, 0)
        ball_collision_type = 1
        self.ball.collision_type = ball_collision_type
        self.ball.filter = pym.ShapeFilter(categories=0b0001)
        space.add(self.ballBody, self.ball)
        self.previous_position = self.ballBody.position

    def update(self, frame):
        prev_pos = self.previous_position
        current_pos = self.ballBody.position
        object_tunneling_info = space.segment_query(prev_pos,
                              current_pos, 6, pym.ShapeFilter(mask=0b1110))
        intersection_dis_from_body = [(
                ((info.point-current_pos).x**2
                 +(info.point-current_pos).y**2)**0.5) for info in object_tunneling_info]
        contact = False
        hit = False
        for i, dis in enumerate(intersection_dis_from_body):
            if dis > 0:
                contact = True
                if not hit:
                    hit = object_tunneling_info[i]
        if contact and hit:
            contact_normal = hit.normal
            dot_product = self.ballBody.velocity.dot(contact_normal)
            reflected_velocity = self.ballBody.velocity - 2*dot_product*contact_normal
            alpha = hit.alpha
            shape = hit.shape
            self.ballBody.position = prev_pos+((current_pos-prev_pos)*(alpha-0.2))
            #print(hit)
            #print(f"position: {self.ballBody.position}, velocity: {self.ballBody.velocity}, bounce: {self.ball.elasticity * shape.elasticity * reflected_velocity}, change: {self.ball.elasticity * shape.elasticity * reflected_velocity - self.ballBody.velocity}")
            self.ballBody.velocity = self.ball.elasticity*shape.elasticity*reflected_velocity
            self.ballBody.position += self.ballBody.velocity.normalized()


        pygame.draw.circle(screen, self.RGB, to_pygame(self.ball.body.position), 6)
        if self.ballBody.velocity.length > self.maxSpeed:
            self.ballBody.velocity = self.ballBody.velocity.normalized() * self.maxSpeed
        if (frame-self.startFrame) >= (60*45):
            space.remove(balls[0].ballBody, balls[0].ball)
            balls.pop(0)

        self.previous_position = self.ballBody.position


    def delete(self):
        try:
            space.remove(self.ballBody, self.ball)
        except AssertionError:
            pass

class ballGenerator:
    def __init__(self, color, xpos, ypos, xvel, yvel, timer):
        self.color = color
        self.xpos = xpos
        self.ypos = ypos
        self.xvel = xvel
        self.yvel = yvel
        self.timer = timer

    def makeBall(self, frame):
        if frame%self.timer == 0:
            b = ball(self.color, self.xpos, self.ypos, frame)
            b.ballBody.velocity = (self.xvel, self.yvel)
            balls.append(b)

class TriangleBouncer:
    def __init__(self, x, y, angle, bounce):
        self.Body = pym.Body(body_type=pym.Body.KINEMATIC)
        self.Body.position = (x, y)
        self.Body.angle = n.radians(angle)
        s = 50
        self.PYMvert = [(n[0]*s, n[1]*s) for n in [(0, 1.73),(1, 0),(0, 0)]]
        print(self.PYMvert)
        self.PYMpoly = pym.Poly(self.Body, self.PYMvert, None, 0.1)
        self.PYMpoly.elasticity = bounce
        bounce_collision_type = 2
        self.PYMpoly.collision_type = bounce_collision_type
        self.superElastic_collision_handler = space.add_collision_handler(ball_collision_type, self.PYMpoly.collision_type)
        self.superElastic_collision_handler.post_solve = self.post_solve_bounce
        space.add(self.Body, self.PYMpoly)

    def draw(self):
        self.PYGvert = [to_pygame(self.PYMpoly.body.local_to_world(vert)) for vert in self.PYMvert]
        self.PYGpoly = pygame.draw.polygon(screen, (100, 100, 100), self.PYGvert)
        pygame.draw.polygon(screen, (100, 100, 100), self.PYGvert)

    def updatePYM(self, vel, ang):
        if vel is not None:
            self.Body.position = vel
        if ang is not None:
            self.Body.angle = ang

    def post_solve_bounce(self, arbiter, space, data):
        shape_1, shape_2 = arbiter.shapes
        if shape_1.body.body_type == pym.Body.DYNAMIC:
            ballBody = shape_1.body
        elif shape_2.body.body_type == pym.Body.DYNAMIC:
            ballBody = shape_2.body
        else:
            return

        normal = arbiter.contact_point_set.normal
        velocity = ballBody.velocity
        reflected = velocity - 2 * ballBody.velocity.dot(normal) * normal
        ball.velocity = max(shape_1.elasticity, shape_2.elasticity) * reflected

class BlackHole:
    def __init__(self, x, y, attraction, radius, fall_off):
        self.Body = pym.Body(body_type=pym.Body.KINEMATIC)
        self.Body.position = (x, y)
        self.PYMshape = pym.Circle(self.Body, 10)
        self.PYMshape.elasticity = 1
        self.PYMshape.friction = 0
        self.attraction = attraction
        self.radius = radius
        self.fall_off = fall_off
        self.willDrawField = False
        space.add(self.Body, self.PYMshape)

    def draw(self, screen):
        for num, ball in enumerate(balls):
            dis = ((((ball.ballBody.position[0]-self.Body.position[0])**2)+((ball.ballBody.position[1]-self.Body.position[1])**2)))**0.5
            if dis <= self.radius:
                magnitude = -1*self.attraction/((dis*self.fall_off)**2)
                if magnitude < -2/3*self.attraction:
                    magnitude = -2/3*self.attraction
                magnitude *= (ball.ballBody.mass*2)**0.5
                unit_vector = ((ball.ballBody.position[0]-self.Body.position[0])/dis, (ball.ballBody.position[1]-self.Body.position[1])/dis)
                ball.ballBody.apply_impulse_at_local_point((unit_vector[0]*magnitude, unit_vector[1]*magnitude-7))
        self.PYGpoly = pygame.draw.circle(screen, (100, 100, 100), to_pygame(self.Body.position), 10)
        if self.attraction > 0:
            pygame.draw.circle(screen, (0, 0, 0), to_pygame(self.Body.position), 8)

    def fieldDrawToggle(self):
        if self.willDrawField:
            self.willDrawField = False
        else:
            self.willDrawField = True

    def drawField(self):
        if self.willDrawField:
            pygame.draw.circle(screen, (50, 50, 50), to_pygame(self.Body.position), self.radius)

    def updatePYM(self, vel, ang):
        if vel is not None:
            self.Body.position = vel
        if ang is not None:
            self.Body.angle = ang

    def updateRadius(self, radius):
        self.radius = radius

    def delete(self):
        try:
            space.remove(self.Body, self.PYMshape)
        except AssertionError:
            pass

    def init(self):
        try:
            space.add(self.Body, self.PYMshape)
        except AssertionError:
            pass

def text(text, screen, size, position, color, background):
    font = pygame.font.Font('Quinquefive-KVpBp.ttf', size)
    text_surface = font.render(text, True, color, background)
    text_rect = text_surface.get_rect()
    text_rect.center = position
    screen.blit(text_surface, text_rect)

def paragraph(Text, position, size, spacing, color, background, surface):
    texts = []
    index = 0
    for i, char in enumerate(Text):
        if char == "/":
            print(index, i)
            texts.append(Text[index:i])
            index = i+1
    texts.append(Text[index:len(Text)])
    for i, line in enumerate(texts):
        text(line, surface, size, (position[0], position[1]+(i*(size+spacing))), color, background)

def load():
    try:
        try:
            with open('machine.dat', 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return None
    except EOFError:
        return None

def compile(additions=[]):
    with open("machine.dat", 'wb') as file:
        try:
            pickle.dump(saved_data+additions, file)
        except TypeError:
            pickle.dump(additions, file)

def delete_save_file(file):
    saved_data.remove(file)
    compile()

def find_save_file(name):
    saved_data = load()
    for dat in saved_data:
        if dat[0] == name:
            return dat

def to_pygame(pos):
    """ Convert Pymunk physics coordinates to Pygame coordinates. """
    if isinstance(pos, list):
        return [(v.x+camerapos[0], v.y+camerapos[1]) for v in pos]
    if isinstance(pos, tuple):  # Handle tuples
        return int(pos[0]+camerapos[0]), int(pos[1]+camerapos[1])
    return int(pos.x+camerapos[0]), int(pos.y+camerapos[1])  # Handle Pymunk Vec2d objects

def updateBallGen(ballGens, frame):
    for bG in ballGens:
        bG.makeBall(frame)

def drawBalls(balls):
    for ball in balls:
        ball.update(frame)

def makeWall(x, y, width, height):
    """ Create static walls at the correct position. """
    body = pym.Body(body_type=pym.Body.STATIC)
    shape = pym.Poly.create_box(body, (width, height), 0.01)
    body.position = (x, y)
    shape.elasticity = 1
    space.add(body, shape)
    return shape

def addTuple(num1, num2):
    return num1[0]+num2[0], num1[1]+num2[1]

def drawPlankGUI(x, y, screen):
    pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(x, y, 100, 10))

def drawcheckpoint():
    for check in m.checkpoints:
        check.draw(screen)

def drawWheelGUI(x, y, surface):
    verts = [[(0, 0), (6, -4), (48, -4), (48, 4), (6, 4)],
             [(0, -8), (20, -43), (27, -39), (6, -4), (0, 0)],
             [(-27, -39), (-20, -43), (0, -8), (0, 0), (-6, -3)],
             [(-27, 39), (-6, 4), (0, 0), (0, 8), (-20, 43)],
             [(0, 0), (6, 4), (27, 39), (20, 43), (0, 8)],
             [(-48, -4), (-6, -3), (0, 0), (-6, 4), (-48, 4)]]

    Verts = []
    for poly in verts:
        Verts.append([addTuple(v, (x, y)) for v in poly])

    for poly in Verts:
        pygame.draw.polygon(surface, (200, 200, 200), poly)

def drawCushionGUI(x, y, surface):
    s = 5
    verts = [(-6*s, 0.5*s),(-4.5*s, 1*s),(0*s, 1.5*s),(4.5*s, 1*s),(6*s, 0.5*s),
            (6*s, -0.5*s),(4.5*s, -1*s),(0*s, -1.5*s),(-4.5*s, -1*s),(-6*s, -0.5*s)]
    Verts = [addTuple(v, (x, y)) for v in verts]

    pygame.draw.polygon(surface, (200, 200, 200), Verts)

def drawFanGui(x, y, surface):
    verts = [(7.5, 15.0), (7.5, -7.5), (30.0, -7.5), (30.0, -15.0),
            (-30.0, -15.0), (-30.0, -7.5), (-7.5, -7.5), (-7.5, 15.0)]
    pygame.draw.polygon(surface, (200, 200, 200), [addTuple((x, y), v) for v in verts])

def drawBlackholeGUI(x, y, surface):
    pygame.draw.circle(surface, (200, 200, 200) , (x, y), 10)
    pygame.draw.circle(surface, (100, 100, 100), (x, y), 8)

def drawPlanks(planks):
    for plank in planks:
        plank.draw(screen)

def drawWheels(wheels):
    for wheel in wheels:
        wheel.draw(screen)

def drawCushions(cushions):
    for cushion in cushions:
        cushion.draw(screen)

def moveItem(items, active_item, dragType):
    if active_item is not None:
        if dragType == 0:
            items[active_item].updatePYM((pygame.mouse.get_pos()[0]-camerapos[0], pygame.mouse.get_pos()[1]-camerapos[1]), None)
        elif dragType == 1:
            items[active_item].updatePYM(None, n.arctan2(
                (pygame.mouse.get_pos()[1] - items[active_item].Body.position[1]),
                (pygame.mouse.get_pos()[0] - items[active_item].Body.position[0])))

def deleteItem(active_item, items):
    if active_item is not None:
        items[active_item].delete()
        items.pop(active_item)

def isMouseOnItem(active_item, items, pos, has_field=False):
    num = None
    for index, item in enumerate(items):
        if type(item.PYGpoly) == list:
            for poly in item.PYGpoly:
                if poly.collidepoint(pos):
                    if active_item != index:
                        num = index
        else:
            if item.PYGpoly.collidepoint(pos):  # Correct way to detect clicks
                if active_item != index:
                    num = index
    if has_field:
        for index, item in enumerate(items):
            if num == index:
                item.willDrawField = True
            else:
                item.willDrawField = False
    return num

def generateInputsOutputs(channels, constraintsInputs=[], constraintsOutputs=[]):
    Inputs = []
    Outputs = []
    Colors = []
    directions = {1:"left", 2:"top", 3:"right", 4:"bottom"}
    color_pool = []
    for i in range(0, int(channels/4) + 1):
        color_pool.append("red")
        color_pool.append("green")
        color_pool.append("yellow")
        color_pool.append("blue")

    top_places = [R for R in range(20, 366)]
    left_places = [R for R in range(20, 266)]
    places = {"left":left_places[:],
              "right":left_places[:],
              "bottom":top_places[:],
              "top":top_places[:]}

    for const in constraintsInputs:
        color_pool.remove(const[3])
        try:
            deletion_target = places[const[0]].index(const[1])
            for j in range(1, 60):
                places[const[0]].pop(deletion_target-15)
        except ValueError:
            print("ValueError")
        except IndexError:
            print("IndexError")
        Inputs.append(const)

    for const in constraintsOutputs:
        color_pool.remove(const[3])
        try:
            deletion_target = places[const[0]].index(const[1])
            for j in range(1, 60):
                places[const[0]].pop(deletion_target-15)
        except ValueError:
            print("ValueError")
        except IndexError:
            print("IndexError")
        Outputs.append(const)

    for i in range(0, channels-len(Inputs)):
        dir = directions[r.randint(1, 3)]
        place = places[dir][r.randint(0, len(places[dir])-1)]
        color = color_pool[r.randint(1, len(color_pool)-1)]
        color_pool.remove(color)
        Colors.append(color)

        try:
            deletion_target = places[dir].index(place)
            for j in range(1, 60):
                places[dir].pop(deletion_target-15)
        except ValueError:
            print("ValueError")
        except IndexError:
            print("IndexError")

        Inputs.append([dir, place, place+15, color])

    for i in range(0, channels-len(Outputs)):
        dir = directions[r.randint(1, 4)]
        place = places[dir][r.randint(0, len(places[dir])-1)]

        try:
            deletion_target = places[dir].index(place)
            for j in range(1, 60):
                places[dir].pop(deletion_target-15)
        except ValueError:
            print("ValueError")
        except IndexError:
            print("IndexError")

        Outputs.append([dir, place, place + 15, Colors[i]])

    print(places)
    print(Inputs, Outputs)
    return Inputs, Outputs

def clear_space():
    for shape in list(space.shapes):
        space.remove(shape)
    for body in list(space.bodies):
        space.remove(body)

def load_buttons():
    names = []
    saved_machine_buttons = []
    delete_buttons = []
    if saved_data:
        for dat in saved_data:
            names.append(dat[0])
        for i, name in enumerate(names):
            saved_machine_buttons.append(
                button(pygame.Rect(50, 50 * i + 50, 800, 40), name, (50, 50, 50), screen.get_rect(), 18))
            delete_buttons.append(
                button(pygame.Rect(850, 50*i+50, 40, 40), "d", (50, 50, 50), screen.get_rect(), 18)
            )
    return saved_machine_buttons, delete_buttons, names

def active_item_to_list(active_item):
    try:
        item_type = active_item[0]
        if item_type == "plank":
            return m.planks
        if item_type == "wheel":
            return m.wheels
        if item_type == "cushion":
            return m.cushions
        if item_type == "fan":
            return m.fans
        if item_type == "blackhole":
            return m.blackholes
        else:
            raise ValueError(f"{item_type} is not a valid component")
    except NameError:
        raise NameError("'m' has not been declared yet")

# Create Ball and Plank
IO = generateInputsOutputs(4)

saved_data = load()

channels = 4

camerapos = [0, 0]

isNotPaused = True
balls = []
active_item = [None, None]
dragType = 0
control_panel_rect = control_panel.get_rect()
control_panel_rect.topleft = (820, 0)
startButton = button(pygame.Rect(250, 300, 520, 50), "start new machine", (50, 50, 50), screen.get_rect())
loadSaveButton = button(pygame.Rect(235, 400, 550, 50), "load saved machine", (50, 50, 50), screen.get_rect())
homeButton = button(pygame.Rect(0, 590, 160, 50), "home", (50, 50, 50), control_panel_rect, 18)
saveButton = button(pygame.Rect(0, 530, 160, 50), "save", (50, 50, 50), control_panel_rect, 18)
rerollInputsOutputsButton = button(pygame.Rect(0, 470, 160, 50), "reroll", (50, 50, 50), control_panel_rect, 18)
helpButton = button(pygame.Rect(0, 410, 160, 50), "help", (50, 50, 50), control_panel_rect, 18)
helpBackButton = button(pygame.Rect(440, 535, 120, 40), "back", (50, 50, 50), screen.get_rect(), 18)
addChannelsButton = button(pygame.Rect(526, 75, 50, 50), "+", (50, 50, 50), screen.get_rect(), 18)
subtractChannelsButton = button(pygame.Rect(420, 75, 50, 50), "-", (50, 50, 50), screen.get_rect(), 18)
createModuleButton = button(pygame.Rect(420, 530, 160, 40), "create", (50, 50, 50), screen.get_rect(), 18)
saveButton2 = button(pygame.Rect(426, 500, 160, 50), "save", (50, 50, 50), screen.get_rect())
plankButton = button(pygame.Rect(0, 20, 160, 70), "", (100, 100, 100), control_panel_rect)
wheelButton = button(pygame.Rect(0, 100, 160, 120), "", (100, 100, 100), control_panel_rect)
cushionButton = button(pygame.Rect(0, 230, 160, 40), "", (100, 100, 100), control_panel_rect)
fanButton = button(pygame.Rect(0, 280, 160, 60), "", (100, 100, 100), control_panel_rect)
blackholeButton = button(pygame.Rect(0, 350, 160, 40), "", (100, 100, 100), control_panel_rect)

saved_machine_buttons, delete_saved_machine_buttons, names = load_buttons()

save_name = "_"
# Game Loop
frame = 1
running = True
game_started = False
on_save_screen = False
on_saved_games_screen = False
on_help_screen = False
on_create_module_screen = False

while running:
    screen.fill((0, 0, 0))  # Clear screen at start
    s = t.time()

    if game_started:
        #draw module and components
        m.draw_and_update()
        drawBalls(balls)

        #draw buttons on control panel
        saveButton.draw(control_panel)
        plankButton.draw(control_panel)
        wheelButton.draw(control_panel)
        cushionButton.draw(control_panel)
        fanButton.draw(control_panel)
        blackholeButton.draw(control_panel)
        rerollInputsOutputsButton.draw(control_panel)
        helpButton.draw(control_panel)
        homeButton.draw(control_panel)

        #draw images for the buttons
        drawPlankGUI(30, 50, control_panel)
        drawWheelGUI(80, 160, control_panel)
        drawCushionGUI(80, 250, control_panel)
        drawFanGui(80, 310, control_panel)
        drawBlackholeGUI(80, 370, control_panel)

        screen.blit(control_panel, control_panel_rect)


        for ev in pygame.event.get():

            if ev.type == pygame.KEYDOWN:

                if ev.key == pygame.K_r:
                    dragType = 1

                if ev.key == pygame.K_m:
                    dragType = 0

                if ev.key == pygame.K_s:
                    if pygame.key.get_mods()&pygame.KMOD_CTRL:
                        compile()
                    else:
                        active_item = [None, None]
                        for fan in m.fans:
                            fan.willDrawField = False
                        for blackhole in m.blackholes:
                            blackhole.willDrawField = False

                if ev.key == pygame.K_e:
                    for b in balls:
                        b.delete()
                    balls = []

                if ev.key == pygame.K_p:
                    if isNotPaused:
                        isNotPaused = False
                    else:
                        isNotPaused = True

                if ev.key == pygame.K_d:
                    deleteItem(active_item[1], active_item_to_list(active_item))
                    active_item = [None, None]

                if ev.key == pygame.K_LEFT:
                    item_type = active_item[0]
                    if item_type == "wheel":
                        m.wheels[active_item[1]].Body.angular_velocity -= 0.3
                    if item_type == "fan":
                        m.fans[active_item[1]].force -= 250
                    if item_type == "blackhole":
                        m.blackholes[active_item[1]].attraction -= 1

                if ev.key == pygame.K_RIGHT:
                    item_type = active_item[0]
                    if item_type == "wheel":
                        m.wheels[active_item[1]].Body.angular_velocity += 0.3
                    if item_type == "fan":
                        m.fans[active_item[1]].force += 250
                    if item_type == "blackhole":
                        m.blackholes[active_item[1]].attraction += 1

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if isMouseOnItem(active_item[1], m.planks, ev.pos) != None:
                    active_item = ["plank", isMouseOnItem(active_item[1], m.planks, ev.pos)]
                elif isMouseOnItem(active_item[1], m.wheels, ev.pos) != None:
                    active_item = ["wheel", isMouseOnItem(active_item[1], m.wheels, ev.pos)]
                elif isMouseOnItem(active_item[1], m.cushions, ev.pos) != None:
                    active_item = ["cushion", isMouseOnItem(active_item[1], m.cushions, ev.pos)]
                elif isMouseOnItem(active_item[1], m.fans, ev.pos) != None:
                    active_item = ["fan", isMouseOnItem(active_item[1], m.fans, ev.pos, True)]
                elif isMouseOnItem(active_item[1], m.blackholes, ev.pos) != None:
                    active_item = ["blackhole", isMouseOnItem(active_item[1], m.blackholes, ev.pos, True)]
                else:
                    print(f"active_item: {active_item}")
                    active_item = [None, None]
                if active_item[1] == None:
                    active_item = [None, None]

                if plankButton.get_isClicked():
                    m.planks.append(Plank(400, 300, 0))

                if wheelButton.get_isClicked():
                    m.wheels.append(Wheel(400, 300))

                if cushionButton.get_isClicked():
                    m.cushions.append(Cushion(400, 300, 0))

                if fanButton.get_isClicked():
                    m.fans.append(Fan(400, 300, 180, 3000, 250))

                if blackholeButton.get_isClicked():
                    m.blackholes.append(BlackHole(400, 300, 30, 300, 1/100))

                if saveButton.get_isClicked():
                    on_save_screen = True
                    game_started = False

                if rerollInputsOutputsButton.get_isClicked():
                    for b in balls:
                        b.delete()
                    balls = []
                    clear_space()
                    m = module(2, 2, (1, 1), None, channels)

                if helpButton.get_isClicked():
                    on_help_screen = True
                    game_started = False

                if homeButton.get_isClicked():
                    game_started = False

            if ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    break

            if ev.type == pygame.MOUSEWHEEL:
                if control_panel_rect.top + 15*ev.y <= 20:
                    control_panel_rect.top += 15*ev.y
                else:
                    control_panel_rect.top = 20

            if ev.type == pygame.QUIT:
                compile()
                running = False

        held_keys = pygame.key.get_pressed()
        if held_keys[pygame.K_c]:
            mousepos = pygame.mouse.get_pos()
            camerapos[0] -= (mousepos[0]-500)/75
            camerapos[1] -= (mousepos[1]-300)/75


        if active_item[0] != None:
            moveItem(active_item_to_list(active_item), active_item[1], dragType)
        if active_item[0] == "blackhole" and active_item[1] != None and dragType == 1:
            mousepos = pygame.mouse.get_pos()
            BHpos = m.blackholes[active_item[1]].Body.position
            print(((BHpos[0]-mousepos[0])**2+(BHpos[1]-mousepos[1])**2)**0.5)
            m.blackholes[active_item[1]].radius = (((BHpos[0]-mousepos[0])**2+(BHpos[1]-mousepos[1])**2)**0.5)

    elif on_saved_games_screen:
        if len(saved_machine_buttons) == 0:
            text("you do not have any saves", screen, 18, (500, 50), (200, 100, 100), (0, 0, 0))
        for Button in saved_machine_buttons:
            Button.draw(screen)
        for Button in delete_saved_machine_buttons:
            Button.draw(screen)
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for i, Button in enumerate(saved_machine_buttons):
                    if i < len(saved_machine_buttons):
                        if delete_saved_machine_buttons[i].get_isClicked():
                            delete_save_file(find_save_file(names[i]))
                            saved_machine_buttons, delete_saved_machine_buttons, names = load_buttons()
                        elif Button.get_isClicked():
                            m = module(2, 2, (1, 1), names[i])
                            game_started = True
                            on_saved_games_screen = False
            if ev.type == pygame.QUIT:
                running = False
    elif on_save_screen:
        text("what do you want to name your machine?", screen, 18, (500,200), (200, 200, 200), (0, 0, 0))
        text(save_name, screen, 18, (500, 300), (200, 200, 200), (0,0,0))
        saveButton2.draw(screen)
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_BACKSPACE:
                    save_name = save_name[:-1]
                else:
                    if save_name == "_":
                        save_name = ""
                    if len(save_name) <= 40:
                        save_name += ev.unicode
            if ev.type == pygame.MOUSEBUTTONDOWN and can_save:
                if saveButton2.get_isClicked():
                    if save_name in names:
                        delete_save_file(find_save_file(save_name))
                    compile([[save_name, [m.planks, m.wheels, m.cushions, m.fans, m.blackholes, m.inputs, m.outputs]]])
                    saved_data = load()
                    saved_machine_buttons, delete_saved_machine_buttons, names = load_buttons()
                    save_name = "_"
                    game_started = True
                    on_save_screen = False

        if save_name in names:
            text('this name is already taken', screen, 18, (500, 400), (255, 100, 100), (0, 0, 0))
            text('are you sure that you want to overwrite?', screen, 18, (500, 450), (255, 100, 100), (0, 0, 0))
            can_save = True
        else:
            can_save = True
    elif on_help_screen:
        paragraph("goal:/"
                  "use components to route balls/ to their respectively colored holes//"
                  "controls:/"
                  "click the buttons on the side to add a component/"
                  "M:move/R:rotate or change radius/"
                  "S:set/"
                  "ctrl+S:save/"
                  "D:delete/"
                  "P:pause/"
                  "left arrow: decrease strength or slow rotation/"
                  "right arrow: increase strength or quicken rotation/"
                  "E:emergency stop; deletes all balls on screen",
                  (500, 50), 16, 16, (200, 200, 200), (0, 0, 0), screen)
        helpBackButton.draw(screen)
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if helpBackButton.get_isClicked():
                    on_help_screen = False
                    game_started = True
    elif on_create_module_screen:
        text("module settings", screen, 18, (500, 50), (200, 200, 200), (0, 0, 0))
        text(str(channels), screen, 18, (500, 100), (200, 200, 200), (0, 0, 0))
        addChannelsButton.draw(screen)
        subtractChannelsButton.draw(screen)
        createModuleButton.draw(screen)
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if addChannelsButton.get_isClicked():
                    if channels < 8:
                        channels += 1
                if subtractChannelsButton.get_isClicked():
                    if channels > 1:
                        channels -= 1
                if createModuleButton.get_isClicked():
                    game_started = True
                    on_create_module_screen = False
                    m = module(2, 2, (1, 1), None, channels)
    else:
        if frame%64 < 32:
            text("ballcoin", screen, 32, (500, 200), (200, 200, 200), (0, 0, 0))
        else:
            text("ballcoin", screen, 32, (500, 200), (150, 150, 150), (0, 0, 0))
        startButton.draw(screen)
        loadSaveButton.draw(screen)
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if startButton.get_isClicked():
                    on_create_module_screen = True
                if loadSaveButton.get_isClicked():
                    on_saved_games_screen = True
            if ev.type == pygame.QUIT:
                running = False

    pygame.display.flip()
    frame_time = t.time()-s
    #print(f"frametime: 1/{int(1/frame_time)} seconds")
    if frame_time < 1/60:
        t.sleep(1/60-frame_time)
    if isNotPaused:
        frame+=1
        space.step(1/60)  # Pymunk physics step

pygame.quit()