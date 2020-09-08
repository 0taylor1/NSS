'''
8/2 08:20
get mouse movement data from pygame and save in a .csv file
ex spikes1.py
'''
from pygame import *
import numpy as np
import math
import os

# file paths
data_dir = os.path.split(os.path.abspath(__file__))[0]

# constants
display_width = 600
display_height = 600
display_center = (int(display_width/2), int(display_height/2))
frame_rate = 40 # (frames/second)
font_size = 26
num_text_cols = 5
target_radius = 200
target_size = 10
num_targets = 8
cursor_size = 20

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# global vars
Font = None

header = 'timestamp, speed, angle'
dt = [('timestamp', np.int), ('speed', np.float), ('angle', np.float)]
data_array = np.array([], dtype=dt)

def mouse_speed(mouse_mvmt):
	x = mouse_mvmt[0]
	y = mouse_mvmt[1]
	speed = math.sqrt(x**2 + y**2)
	# print('%.2f'%speed)
	return speed

def mouse_angle(mouse_mvmt):
	x = mouse_mvmt[0]
	y = mouse_mvmt[1]
	angle = math.atan2((-1)*y, x)
	# print('%.2f'%np.degrees(angle))
	return angle

def draw_line(dp, mouse_mvmt):
	end_x = display_center[0] + mouse_mvmt[0]*10
	end_y = display_center[1] + mouse_mvmt[1]*10
	draw.line(dp, RED, display_center, (end_x, end_y), 10)

def draw_targets(dp, num_targets, mouse_pos, overlapping):
	'''
	draw num_targets targets in a circle around the center,
	target turns green when overlapping with cursor
	returns:
		overlapping, array of num_targets bool values
		play_sound, whether or not to play sound
	'''
	# center target
	draw.circle(dp, BLUE, display_center, target_size)
	angles = np.linspace(0, np.pi*2, num_targets, endpoint=False)
	play_sound = False
	for i in range(num_targets):
		x = int(target_radius*np.cos(angles[i])) + display_center[0]
		y = int(target_radius*np.sin(angles[i])) + display_center[1]
		distance = np.hypot(mouse_pos[0]-x, mouse_pos[1]-y)
		overlaps = (distance < (cursor_size + target_size))
		if not overlapping[i] and overlaps:
			play_sound = True
		overlapping[i] = overlaps
		color = GREEN if overlapping[i] else WHITE
		draw.circle(dp, color, (x, y), target_size)
	return overlapping, play_sound

def load_sound(name):
	'''for chime sound when target is reached'''
	class NoneSound:
		def play(self): pass
	if not mixer or not mixer.get_init():
		return NoneSound()
	fullname = os.path.join(data_dir, name)
	try:
		sound = mixer.Sound(fullname)
	except error:
		print('cannot load sound: %s'%fullname)
		raise SystemExit(str(geterror()))
	return sound

def text(dp, text, x, y, color=WHITE):
	'''blits text onto display'''
	dp.blit(Font.render(text, 1, color, BLACK), (x, y))

def display_text(dp, mouse_mvmt):
	x = np.arange(0, display_width, int(display_width/num_text_cols), dtype=int)
	y = np.arange(0, display_height, (font_size*1.2), dtype=int)
	pad = "          "

	# texts to display
	text(dp, "(x, y)", x[1], y[0], GREEN)
	labels = ["pos", "rel", "speed", "angle"]
	values = [	mouse.get_pos(),
				mouse_mvmt,
				'%.2f'%mouse_speed(mouse_mvmt),
				'%.2f'%math.degrees(mouse_angle(mouse_mvmt))
				]

	for i in range(len(labels)):
		text(dp, labels[i], x[0], y[i+1], BLUE)
		text(dp, str(values[i]), x[1], y[i+1])

def get_mouse_data():
	# pygame init
	init()
	game_display = display.set_mode((display_width, display_width))
	# game_display = display.set_mode((0,0), FULLSCREEN)
	display.set_caption("targets")
	clock = time.Clock()
	sound = load_sound('chime.wav')
	global Font
	Font = font.Font(None, font_size)

	mouse_pos = ()
	mouse_mvmt = ()
	overlapping = np.zeros(num_targets)
	done = False
	while not done:
		mouse_mvmt = mouse.get_rel()
		for e in event.get():
			mouse_pos = mouse.get_pos()
			mouse_mvmt = mouse.get_rel()
			if  e.type == KEYDOWN:
				if e.key == K_q:
					print("quitting")
					done = True
			if e.type == QUIT:
				done = True

		game_display.fill(BLACK)
		display_text(game_display, mouse_mvmt)
		overlapping, play_sound = draw_targets(game_display, num_targets, mouse_pos, overlapping)
		if play_sound: sound.play()
		# draw_line(game_display, mouse_mvmt) # velocity vector
		draw.circle(game_display, RED, mouse_pos, cursor_size, 0)

		data_entry = np.array([tuple((time.get_ticks(),
								mouse_speed(mouse_mvmt),
								mouse_angle(mouse_mvmt)))], dtype=dt)
		global data_array
		data_array = np.append(data_array, data_entry)

		display.update()
		clock.tick(frame_rate)

	# save data
	np.savetxt('mouse-data.csv', data_array, delimiter=",", fmt=['%d', '%f', '%f'], header=header)
	print("saved data")
	# quit()

# get_mouse_data()