import sys
from PIL import Image
color, suns, bulbs, to_render = [1,1,1], [], [], []
eye, forward, right, up, s = [0,0,0], [0,0,-1], [1,0,0], [0,1,0], [0]
fisheye = False
w, h = 0, 0

def clamp(num):
	return max(0, min(float(num), 1))

def round(num):
	return int(num + 0.5)

def normalize(vec):
	mag = 0
	for i in vec:
		mag += i**2
	mag = mag**.5
	for i in range(len(vec)):
		vec[i] /= mag

def cross(a, b):
	return [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]

def norm(vec):
	temp = [i**2  for i in vec]
	return sum(temp) ** .5

def dot(vec1, vec2):
	return sum([vec1[i]*vec2[i] for i in range(len(vec1))])

def ray(x,y):
	sx = (2*x -w)/max(w,h)
	sy = (h-2*y)/max(w,h)
	if fisheye:
		mag_forward = sum([forward[i]**2 for i in range(3)])**.5
		sx /= mag_forward
		sy /= mag_forward
		r_2 = sx**2 + sy**2
		if r_2**.5 > 1:
			return None
		else:
			k = (1-r_2)**.5
			return [k*forward[i] + sx*right[i] + sy*up[i] for i in range(3)]
	direction =  [forward[i] + sx*right[i] + sy*up[i] for i in range(3)]
	return direction

def raytrace(direction,eye_0):
	closest = float('inf')
	test = False
	col = [0,0,0]
	illu = [0,0,0]
	t = 0
	closest_obj = None
	normalize(direction)
	for i in to_render:
		
		if i[0] == 's':
			# check if ray originates inside sphere
			cr = [i[j+1] - eye_0[j] for j in range(3)]
			r_2 = i[4] ** 2
			inside = norm(cr) ** 2 < r_2
			tc = dot(cr,direction)/norm(direction)
			if not inside and tc < 0:
				continue
			d_2 = norm([eye_0[j] + tc * direction[j] - i[j+1] for j in range(3)]) ** 2
			if not inside and d_2 > r_2:
				continue
			t_offset = ((r_2 - d_2) ** .5)/norm(direction)
			if inside:
				t = tc + t_offset
			else:
				t = tc - t_offset
		elif i[0] == "p":
			if i[1] != 0:
				temp = [-i[4]/i[1],0,0]
			elif i[2] != 0:
				temp = [0,-i[4]/i[2],0]
			elif i[3] != 0:
				temp = [0,0,-i[4]/i[3]]
			n = [i[j] for j in range(1,4)]
			if(dot(direction,n) == 0):
				continue
			pr = [temp[j] - eye_0[j]   for j in range(3)]
			t = dot(pr,n)/dot(direction,n)
			
			if t <= 0:
				continue
			#print(t)
		if  0 < t < closest:
			col = [i[j] for j in range(5,8)]
			closest = t
			closest_obj = i
	if closest_obj is not None and (len(suns) != 0 or len(bulbs) != 0) :
		point_of_inters = [eye_0[i] + (closest-.000001)*direction[i] for i in range(3)]
		surface_normal = ([point_of_inters[i] - closest_obj[i+1] for i in range(3)]) if closest_obj[0] == 's' else [closest_obj[j] for j in range(1,4)] 
		away_vector = [point_of_inters[i] - eye_0[i] for i in range(3)]
		#print (dot(surface_normal, away_vector))
		if dot(surface_normal, away_vector) > 0:
			surface_normal = [-surface_normal[i] for i in range(3)]
			#print('flip')
		normalize(surface_normal)
		for i in suns:
			light_dir = [i[k] for k in range(3)]
			light_color = [i[k] for k in range(3,6)]
			if eye_0 == eye:	
				g, f = raytrace(light_dir,point_of_inters)
				#print(g)
				if g != float('inf') and g > .01:
					 light_color = [0,0,0]	 
			normal_dot_light = sum([surface_normal[k]*i[k] for k in range(3)])
			if normal_dot_light < 0:
				continue
			for j in range(3):
				illu[j] += col[j] * light_color[j] * normal_dot_light

		for i in bulbs:
			light_dir = [i[k] - point_of_inters[k] for k in range(3)]
			intensity = 1/sum([light_dir[k]**2 for k in range(3)])
			light_color = [i[k] for k in range(3,6)]
			normalize(light_dir)
			normal_dot_light = sum([surface_normal[k]*light_dir[k] for k in range(3)])
			if normal_dot_light < 0:
				continue
			if eye_0 == eye:	
				g, f = raytrace(light_dir,point_of_inters)
				if g != float('inf') and g > .1:
					'''new_point_of_inters = [point_of_inters[k] + (closest-.000001)*light_dir[k] for k in range(3)]
					interesect = True
					for k in range(3):
						interesect = new_point_of_inters[k] == i[k]
					if not interesect:'''
					#light_color = [0,0,0]
					pass
			
			for j in range(3):
				illu[j] += col[j] * light_color[j] * normal_dot_light * intensity
	return closest,illu

def draw():
	for i in range(w):
		for j in range(h):
			direction = ray(i,j)
			if direction == None:
				continue
			t,col = raytrace(direction,eye)
			#print("Coord:",i,j)
			if t != float('inf'):
				#print(t)
				col = [int(clamp(col[i])* 255) for i in range(3)]
				#print(col)
				img[i,j] = (col[0], col[1], col[2],255)
						

if len(sys.argv) == 1:
	print("Must provide at least 1 argument")
	sys.exit()

for i in range (1, len(sys.argv)):
	filereader = open(sys.argv[i],"r")
	
	for line in filereader.readlines():
		if len(line.strip()) != 0:
			words = line.strip().split()
			keyword = words[0]
		else:
			keyword = ""	
		if keyword == "png":
			width, height = int(words[1]), int(words[2])
			image = Image.new("RGBA", (width,height), (0,0,0,0))
			img = image.load()
			w, h = width, height
			color, suns, bulbs, to_render = [1,1,1], [], [], []
			eye, forward, right, up = [0,0,0], [0,0,-1], [1,0,0], [0,1,0]
			fisheye = False
			filename = words[3]
		elif keyword == "color":
			color = [float(words[i]) for i in range(1,4)]
		elif keyword == "sphere":
			temp = ["s"]
			temp.extend([float(words[i]) for i in range(1,5)])
			temp.extend(color)
			temp.extend(s)
			to_render.extend([temp])
		elif keyword == "sun":
			temp = [float(words[i]) for i in range(1,4)]
			normalize(temp)
			temp.extend(color)
			temp.extend(s)
			suns.extend([temp])
		elif keyword == "plane":
			temp = ["p"]
			temp.extend([float(words[i]) for i in range(1,5)])
			temp.extend(color)
			to_render.extend([temp])
		elif keyword == "eye":
			eye = [float(words[i]) for i in range(1,4)]
		elif keyword == "forward":
			forward = [float(words[i]) for i in range(1,4)]
			temp = cross(forward,up)
			right = list(temp)
			temp = cross(right,forward)
			up = list(temp)
			normalize(up)
			normalize(right)
		elif keyword == "up":
			temp = cross(forward,cross([float(words[i]) for i in range(1,4)], forward))
			up = list(temp)
			right = cross(forward,up)
			normalize(up)
			normalize(right)
		elif keyword == "bulb":
			temp = [float(words[i]) for i in range(1,4)]
			temp.extend(color)
			bulbs.extend([temp])
		elif keyword == "fisheye":
			fisheye = True
		elif keyword == "s":
			s = [float(words[1])]
		elif keyword == "":
			pass		
	draw()
	print(filename, "is done!")
	image.save(filename)	
