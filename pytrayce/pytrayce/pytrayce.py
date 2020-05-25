import sys
import numpy as np
import math
import time

def unitVec(vec):
	return vec / np.linalg.norm(vec)

def unitVecFromAngles(inclination, azimuth):
	# Returns unitized vector in NumPy array
	# Angles provided in radians
	# Inclination 0 at zenith (vertical up / +z)
	# Azimuth 0 at +x
	
	x = np.sin(inclination) * np.cos(azimuth)
	y = np.sin(inclination) * np.sin(azimuth)
	z = np.cos(inclination)
	
	u = np.array([x, y, z])
	u = unitVec(u)

	return u

def unitVecFromFocus(source, focus):
	u = focus - source
	u = unitVec(u)

	return u

class SceneObject:
	pass

class Sphere(SceneObject):
	def __init__(self, center, radius):
		self.center = center
		self.radius = radius

	def rayIntersect(self, source, rayDir):
		s = self.center - source
		ls = np.linalg.norm(s)

		sdotd = np.dot(s, unitVec(rayDir))

		a = math.sqrt(ls ** 2 - sdotd ** 2)

		if a > self.radius:
			return None

		b = math.sqrt(self.radius ** 2 - a ** 2)

		d = sdotd - b

		x = rayDir * d + source

		return x
		
t0 = time.time()

(viewWidth, viewHeight) = (640, 480)
viewRatio = float(viewWidth) / float(viewHeight)

S = (-1., 1. / viewRatio + .25, 1., -1. / viewRatio + .25)

x = np.tile(np.linspace(S[0], S[2], viewWidth), viewHeight)
y = np.repeat(np.linspace(S[1], S[3], viewHeight), viewWidth)

print((viewWidth, viewHeight))
print(viewRatio)
print(S)

fov = 90.

posCam = np.array([5., 3., 0.])
sphere1 = Sphere(np.array([9., 12., 0.]), 2.)

#posCam = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
#posCam = np.array([[11, 12, 13],
#				   [21, 22, 23],
#				   [31, 32, 33]])

#print(posCam[0, :])
#print(posCam[:, 1])

rayDir = unitVec(np.array([4., 8., 0.]))

rayInt = sphere1.rayIntersect(posCam, rayDir)

print(posCam)
print(sphere1.center)
print(np.array([9., 10., 0.]))
print(rayDir)
print(rayInt)

print("FART")
a = np.array([1, 2, 3])
print(a)
print(np.linalg.norm(a))
print(a / np.linalg.norm(a))

print(x.size)
print(y.size)

print("Took %.3f seconds" % (time.time() - t0))

#sys.exit()

#########################################################################

#import sdl2
#import sdl2.ext

#sdl2.ext.init()

#window = sdl2.ext.Window("~fart~", size=(viewWidth, viewHeight))
#window.show()

#factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
#sprite = factory.from_image(r"C:\Users\Sterculius\Downloads\Img2.bmp")

#spriterenderer = factory.create_sprite_render_system(window)
#spriterenderer.render(sprite)

#ticks = 0

#event = sdl2.SDL_Event()

##while 1:
#lastTicks = ticks
#ticks = sdl2.timer.SDL_GetPerformanceCounter()
#tickDelta = ticks - lastTicks
#timePassed = tickDelta / sdl2.timer.SDL_GetPerformanceFrequency()

#while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
#	pass

#sdl2.ext.quit()

#sys.exit()

#########################################################################

import pygame

pygame.init()

screen = pygame.display.set_mode([viewWidth, viewHeight], 0)

pxsurf = pygame.Surface([viewWidth, viewHeight], 0)

blitObj = pygame.image.load(r"C:\Users\Sterculius\Downloads\Img.bmp")
blitObjRect = blitObj.get_rect()
speed = [2, 2]

ticks = 0

while 1:
	lastTicks = ticks
	ticks = pygame.time.get_ticks()
	ticksDelta = (ticks - lastTicks)

	if ticksDelta < 1000. / 60.:
		pygame.time.wait(int(1000. / 60.) - ticksDelta)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit(0)

	blitObjRect = blitObjRect.move(speed)
	
	if blitObjRect.left < 0 or blitObjRect.right > viewWidth:
		speed[0] = -speed[0]

	if blitObjRect.top < 0 or blitObjRect.bottom > viewHeight:
		speed[1] = -speed[1]
		
	screen.fill((0, 0, 0))

	pxarray = pygame.PixelArray(pxsurf)
	
	for j in range(viewHeight):
		for i in range(viewWidth):
			pxarray[i][j] = (i / viewWidth * 255, 0, j / viewHeight * 255)

	del pxarray

	screen.blit(pxsurf, (0, 0))

	screen.blit(blitObj, blitObjRect)

	pygame.display.flip()