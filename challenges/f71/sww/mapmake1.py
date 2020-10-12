#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Small Wide World
Map maker
by Javantea
April 26, 2007

Description:
An idea to make maps.
1: Place all points at the center.
2: Move each point randomly.
3: Move each point closer to it's connected points.
4: Goto 2
5: Profit!

TODO:
Get the randomization.
Get a data set to draw.
Get the flocking.
#TODO:
Make numpy actually optional for getX0Conns.
"""
from __future__ import print_function
from random import randint, seed, random, SystemRandom, shuffle
from math import sqrt, sin, cos, pi, atan2, ceil
from hashlib import sha256
from collections import defaultdict
import heapq
import time
try:
	import numpy as np
except ImportError:
	#print("No Numpy")
	np = None
#end try
polar1 = None
tau = 2 * pi
SMALL = 1e-16

def printVerbose(*args, **kwargs):
	return

class Map:
	"""
	Base class for all maps (friend, object, route).
	Write the hard math and physics here once and use it by calling once.
	"""
	def __init__(self, points=None, width=640, height=480, line_width=2, line_color = '#8888ff'):
		self.points = points
		# There's a bug in python where if I do points=[] above, it 
		# thinks it's a static when it's really really not.
		if points == None: self.points = []
		self.width  = width
		self.height = height
		self.line_width = line_width
		self.line_color = line_color
		self.selectedPoint = None
		self.title = 'Small Wide World Map'
		self.desc = 'Test of drawing a network map with svg'

	def addPoint(self, point):
		self.points.append(point)

	def addPoints(self, points):
		self.points.extend(points)
	
	def randomize(self, amount = 180):
		for point in self.points:
			point.x += randint(-amount, amount)
			point.y += randint(-amount, amount)
		#next point
	#end def randomize()
	
	def scale(self, scale):
		"""
		Scale every point
		"""
		for point in self.points:
			point.x *= scale
			point.y *= scale
		#next point
	#end def scale(scale)
	
	def drag(self, x, y):
		if self.selectedPoint == None:
			return False
		#end if
		r = Vector2(x, y)
		d_len = (r - self.selectedPoint).lensq()
		if (d_len > 100):
			self.selectedPoint.x = x
			self.selectedPoint.y = y
			return True
		#end if
		return False
	#end def drag(x, y)
	
	def click(self, x, y):
		cp = Vector2(x, y)
		min_dr = -1.0
		min_dr_p = None
		for point in self.points:
			dr = cp - point
			dr_len = dr.lensq()
			if (min_dr < 0) or (dr_len < min_dr):
				min_dr = dr_len
				min_dr_p = point
			#end if
		#next point
		if min_dr_p != None:
			min_dr_p.setColor('#cc6666')
			if self.selectedPoint != None:
				self.selectedPoint.setColor('#6666ff')
			#end if
			self.selectedPoint = min_dr_p
		#end if
	#end def click(x, y)
	
	def sort1(self):
		for point in self.points:
			for conn in point.conns:
				dr = conn - point
				point += dr * 0.4
			#next conn
		#next point
	#end def sort1()
	
	def sort2(self, dist1 = 80, f = 0.5):
		"""
		Use springs to decide the position of each point.
		"""
		for point in self.points:
			for conn in point.conns:
				dr = conn - point
				dr_len = dr.length()
				#print '	dr:', dr
				if dr_len == 0.0:
					point.x += 5.0
					point.y += 5.0
					dr_len = sqrt(5*5 + 5*5)
				#end if
				m = 1
				a_len = (f/m) * (dr_len - dist1)
				dr_hat = dr / dr_len
				a = dr_hat * (a_len / m)
				dt = 0.6
				dp = a * (0.5*dt*dt)
				point.x += dp.x
				point.y += dp.y
			#next conn
		#next point
	#end def sort2()
	
	def sort3(self):
		"""
		Use springs to decide the position of each point.
		"""
		for point in self.points:
			if len(point.conns) <= 1: continue
			#avgx = 0
			#avgy = 0
			avg = Vector2(0, 0)
			for conn in point.conns:
				avg += conn
			#next conn
			p = avg / len(point.conns)
			point.x = p.x
			point.y = p.y
		#next point
	#end def sort3()
	
	def sort4(self):
		"""
		Use a style of reverse attack on non-conns that are close.
		"""
		for point in self.points:
			for nonconn in self.points:
				if nonconn in point.conns:
					continue
				#end if
				dr = point - nonconn
				dr_len = dr.length()
				if dr_len < 50:
					if dr_len == 0:
						dr = Vector2(1, 1)
						dr_len = sqrt(2)
					#end if
					dr *= 4.0 / dr_len
					point.x += dr.x
					point.y += dr.y
				#end if
			#next nonconn
		#next point
	#end def sort4()
	
	def sort5(self):
		"""
		This is obviously the best algorithm ever. Hooray for the power 
		of awesomeness.
		"""
		for point in self.points:
			enemies_pos = Vector2(0, 0)
			enemies_len = 0
			friends_pos = Vector2(0, 0)
			for nonconn in self.points:
				if nonconn in point.conns:
					friends_pos += nonconn
					continue
				#end if
				dr = point - nonconn
				dr_len = dr.lensq()
				if dr_len < 2500:
					enemies_pos += nonconn
					enemies_len += 1
				#end if
			#next nonconn
			enemies_pos /= enemies_len
			friends_pos /= len(point.conns)
			dr = friends_pos * 2 - enemies_pos
			# Our position looks like this: enemies ---- friends ---- me
			point.x = dr.x
			point.y = dr.y
			print(point)
			print('\t' + '(' + str(enemies_len) + ')', enemies_pos)
			print('\t' + '(' + str(len(point.conns)) + ')', friends_pos)
		#next point
	#end def sort5()
	
	def sort6(self):
		"""
		A new algorithm based on sort5 but with added validity information.
		"""
		validity = [False for p in self.points]
		for i, point in enumerate(self.points):
			enemies_pos = Vector2(0, 0)
			enemies_len = 0
			friends_pos = Vector2(0, 0)
			friends_len = 0
			for j, nonconn in enumerate(self.points):
				if not validity[j]:
					continue
				#end if
				if nonconn in point.conns:
					friends_pos += nonconn
					friends_len += 1
					continue
				#end if
				enemies_pos += nonconn
				enemies_len += 1
				#end if
			#next nonconn
			if enemies_len > 1: enemies_pos /= enemies_len
			if friends_len > 1: friends_pos /= friends_len
			if enemies_len > 0 or friends_len > 0:
				dr = friends_pos * 1.7 - enemies_pos
				if enemies_len == 0 or (dr - friends_pos).lensq() < 1 or (dr - enemies_pos).lensq() < 1:
					# Fix anything by using a random angle.
					theta = randint(0, 360) * (pi / 180.0)
					dr = Vector2(dr.x + 30 * cos(theta), dr.y + 30 * sin(theta))
				#end if
			else:
				dr = Vector2(0, 0)
			#end if
			# Our position looks like this: enemies ---- friends ---- me
			point.x = dr.x + (randint(0, 100) / 4.0)
			point.y = dr.y + (randint(0, 100) / 4.0)
			#print point
			#print '\t' + '(' + str(enemies_len) + ')', enemies_pos
			#print '\t' + '(' + str(friends_len) + ')', friends_pos
			validity[i] = True
		#next point
	#end def sort6()
	
	def sortBranch(self, r0=40, knownPos=None):
		"""
		A brilliant sorting method that works well with branches but not loops.
		r0 is the length of the bonds set by the algorithm.
		knownPos is a list of booleans that tells us whether point i is given or should be computed.
		roundTry is required for loops. This can be optimized greatly.
		FIXME: Starfish where node 5 is the central node.
		Fixable by picking knownPos based on number of connections.
		TODO: Find other bugs.
		"""
		checkEverything = True
		nodes = len(self.points)
		if nodes < 1:
			# Congrats, you're guaranteed to be sorted.
			return
		#end if
		# This is our algorithm... Written on the whiteboard last night. Understood many years ago but unable to write the code. Until now!
		if knownPos == None:
			knownPos = [False] * nodes
			knownPos[0] = True
			# We don't need to do expensive checks if we have no knowns. *shrug*
			checkEverything = False
			self.points[0].x = self.width / 2
			self.points[0].y = self.height / 2
		#end if
		# v1 in spherical coordinates.
		#v1 = (r1, theta1) == (r1*cos(theta1), r1*sin(theta1))
		v1 = (r0, 0)
		# -v1 in spherical coordinates
		#neg_v1 = (r0, v1[1] + pi)
		fillReady = False
		mapPointToIndex = self.pointToIndex()
		
		for roundTry in range(nodes):
			#print("fillReady?", fillReady)
			knownDone = True
			for i in range(nodes):
				if (not fillReady) and (not knownPos[i]): continue
				#print(self.points[i].name, [c.name for c in self.points[i].conns])
				givens = []
				unknowns = []
				# Set the position of its connections.
				for conn in self.points[i].conns:
					j = mapPointToIndex[conn]
					if knownPos[j]:
						givens.append(j)
						continue
					#end if
					unknowns.append(j)
				#next conn
				if knownPos[i]:
					# First solve the easy cases, then work your way up.
					if len(unknowns) == 0:
						# Everything is known, we're good.
						#print('Yay', self.points[i].x, self.points[i].y)
						continue
					#end if
					if len(givens) == 0:
						# All unknowns, so use the simplex method.
						n_conns = len(unknowns)
						theta0 = tau / n_conns # tau = 2*pi
						x = 0
						for j in unknowns:
							# Spherical coordinates
							theta_j = v1[1] + (theta0 * (x+1))
							#v_j = (r0, theta_j)
							self.points[j].x, self.points[j].y = (self.points[i].x + (r0*cos(theta_j)), self.points[i].y + (r0*sin(theta_j)))
							knownPos[j] = True
							knownDone = False
							#print('Simple', x, j, self.points[j].x, self.points[j].y, theta_j)
							x += 1
						#next j
						continue
					#end if
					if len(givens) == 1:
						# Very easy, create a v1 and do the same as above
						v1i_cartesian = self.points[i] - self.points[givens[0]]
						v1i_theta = atan2(v1i_cartesian.y, v1i_cartesian.x)
						#v1i_spherical = (v1i_cartesian.length(), v1i_theta)
						#neg_v1i_spherical = (v1i_cartesian.length(), v1i_theta+pi)
						n_conns = len(unknowns) + 1
						theta0 = tau / n_conns # tau = 2*pi
						x = 0
						for j in unknowns:
							# Spherical coordinates
							if n_conns == 2:
								theta_j = v1i_theta
							else:
								theta_j = v1i_theta+pi + (theta0 * (x+1))
							#end if
							#v_j = (r0, theta_j)
							self.points[j].x, self.points[j].y = (self.points[i].x + (r0*cos(theta_j)), self.points[i].y + (r0*sin(theta_j)))
							knownPos[j] = True
							knownDone = False
							#print('Simple1', x, j, self.points[j].x, self.points[j].y, theta_j, 'v1it', v1i_theta)
							x += 1
						#next j
					#end if
					#print("Not sure what to do for: given: %i, unknown: %i" % (len(givens), len(unknowns)))
					# Take the list of givens and create a perfect placement for our node
				else:
					# Don't use v1 until all known nodes are figured out.
					# Fixes sortBranch_fail1.json
					if not fillReady: continue
					#print("Not known pos", i, knownPos[i])
					if len(givens) == 0:
						# We don't know any of our neighbors yet, nope.
						continue
					#end if
					if len(givens) == 1:
						# Use v1 to choose our position
						knownPos[i] = True
						j = givens[0]
						#print(i, 'using v_%i' % j)
						theta_j = v1[1]
						self.points[i].x, self.points[i].y = (self.points[j].x + (r0*cos(theta_j)), self.points[j].y + (r0*sin(theta_j)))
						if checkEverything:
							# Expensive check for overlapping points, stops early when no overlap occurs.
							# Worst case scenario, 3*known points
							for theta_j_new in [v1[1] + pi, v1[1] + (pi*0.5), v1[1] + (pi*1.5)]:
								isOverlapped = False
								for k, p in enumerate(self.points):
									if k == i: continue
									if knownPos[k] == False: continue
									dr = self.points[i] - p
									if dr.lensq() < SMALL:
										#print("Found overlap, it's time to fix.")
										# We're on top of something known, move.
										self.points[i].x, self.points[i].y = (self.points[j].x + (r0*cos(theta_j_new)), self.points[j].y + (r0*sin(theta_j_new)))
										isOverlapped = True
										break
									#end if
								#next k, p
								# No overlap found, this is good enough.
								if not isOverlapped: break
							#next theta_j_new
						#end if
						continue
					#end if
					#print('avg')
					# Average of its peers
					totalPos = [0, 0]
					for j in givens:
						totalPos[0] += self.points[j].x
						totalPos[1] += self.points[j].y
					#next j
					avg = (totalPos[0] / len(givens), totalPos[1] / len(givens))
					self.points[i].x, self.points[i].y = avg
					knownPos[i] = True
				#end if
				if not (False in knownPos): break
			#next i
			if not (False in knownPos):
				break
			#end if
			# If knownDone is still true at this point, we're ready to fill in the rest of the values.
			if knownDone: fillReady = True
		#next roundTry
		#if False in knownPos:
		print("Took %i tries, %i nodes" % (roundTry + 1, len(self.points)))
		#end if
	#end def sortBranch(r0=40, knownPos=None)
	
	def sortLinear(self, b0=40):
		"""
		Draws the "backbone" in a line.
		TODO: Test and Understand everything that you need to understand for backbone.
		FIXED: loopsort1_5.json backbone issue with a trivial graph.
		FIXME: python3 ../loopsort1.py -n 10 -c 2 puts c and d in the same place.
		"""
		# Polar coordinates to the rescue!
		loadPolar()
		v = [(b0, 0) for i in self.points]
		self.setCartesian(v)
	#end def sortLinear(b0=40)
	
	def sortCircle(self, b0=40):
		"""
		Draws the "backbone" in a circle.
		Sort in a weird way. Doesn't work for long (or even reasonably sized) graphs.
		"""
		# Polar coordinates to the rescue!
		loadPolar()
		#theta0 = tau / 12 # 30 degrees
		theta0 = tau / 9 # 40 degrees
		rev, atom_hash = self.getPolarConn()
		#v = [(b0, theta0 * i) for i in range(len(self.points))]
		v = []
		bonds = defaultdict(int)
		for i, i_x in rev:
			#print('{0} -- {1} {2}'.format(self.points[i].name, self.points[i_x].name, (i_x + bonds[i_x])))
			v.append((b0, theta0 * ((-0.004 * i_x * i_x) + i_x + bonds[i_x])))
			# Don't put two nodes in the same place hmmm
			if i != i_x: bonds[i_x] += 1
		#next i
		self.setCartesian(v)
	#end def sortCircle(b0=40)
	
	def sortSpiral(self, b0=40):
		"""
		Draws the "backbone" in a spiral.
		Sort in a novel way. Works for backbone only and loops well, but not branches.
		TODO: Test and Understand everything that you need to understand for backbone.
		"""
		# Use grid because we have the infrastructure.
		rows = cols = len(self.points)
		grid = []
		for i in range(rows):
			grid.append([None] * cols)
		#next i
		pos = (cols // 2, rows // 2)
		#grid[pos[1]][pos[0]] = self.points[0]
		directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
		#dir_names = 'right down left up'.split(' ')
		currDirection = 0
		for p in self.points:
			#print(p.name)
			foundSpot = False
			while not foundSpot:
				if grid[pos[1]][pos[0]] == None:
					grid[pos[1]][pos[0]] = p
					foundSpot = True
					break
				#end if
				# Move in the current direction.
				#print(dir_names[currDirection])
				pos = (pos[0] + directions[currDirection][0], pos[1] + directions[currDirection][1])
			#loop
			# Move in the current direction until we can turn.
			while True:
				pos = (pos[0] + directions[currDirection][0], pos[1] + directions[currDirection][1])
				if grid[pos[1]][pos[0]] == None:
					break
				#end if
				#print(dir_names[currDirection], 'because', grid[pos[1]][pos[0]].name)
			#loop
			# If we can turn, turn.
			nextDirection = (currDirection + 1) % 4
			peekPos = (pos[0] + directions[nextDirection][0], pos[1] + directions[nextDirection][1])
			if grid[peekPos[1]][peekPos[0]] == None:
				currDirection = nextDirection
				#print(dir_names[currDirection], 'turn')
			#end if
		#next i
		# TODO: Shrink the grid if necessary.
		gridToPos(grid, b0)
		self.centerBound()
	#end def sortSpiral(b0=40)
	
	def sortLattice(self, b0=40):
		"""
		Sort almost perfectly for completely unconnected nodes.
		TODO: take connections into account.
		TODO: Make rows and cols variable.
		TODO: Limited sortLattice using knownPos
		"""
		nodes = len(self.points)
		side_len = int(ceil(sqrt(nodes)))
		if side_len < 2:
			# We don't want your tiny 1 node graph at this point.
			return
		#end if
		row_pos = Vector2(0, 0)
		i = 0
		# Reverse direction with each row for better performance.
		# --->
		# <---
		# --->
		mul = -1
		for row in range(side_len):
			q = side_len
			if i + q > nodes: q = nodes - i
			if mul == 1:
				mul = -1
				row_pos.x += (side_len - 1) * b0
			else:
				mul = 1
				row_pos.x -= (side_len - 1) * b0
			#end if
			for col in range(q):
				p = self.points[i]
				p.x = row_pos.x + (mul * col * b0)
				p.y = row_pos.y
				i += 1
			#next col
			row_pos.x += b0 * -0.5
			row_pos.y += b0 * 0.8660254037844386
		#next row
	#end def sortLattice(b0=40)
	
	def sortRandomTheta(self, b0=40):
		"""
		Pick random values for theta.
		"""
		# Polar coordinates to the rescue!
		loadPolar()
		v = [(b0, random() * tau) for i in self.points]
		self.setCartesian(v)
	#end def sortRandomTheta(b0=40)
	
	def sortFix(self, b0=40):
		"""
		Fix the problem with sortLinear above
		../loopsort1.py -n 10 -c 2 puts c and d in the same place.
		This fixes d but not j. An obvious problem is square instead of ngon, 
		but with the ngon it's broken putting it all the way over to the right.
		That's because it's seeing i-j being long and thinking that i is e. 
		This can benefit from grouping, but is it the only solution? Seems legit.
		
		"""
		for p in self.points:
			for q in p.conns:
				drx = abs(p.x - q.x)
				if drx < SMALL:
					# Two connected items are on top of one another, should we fix it?
					#print("Should we fix?", p.name, '--', q.name)
					# Let's move q and everything to the right to the right.
					q.x += b0
					for r in self.points:
						if r.x > p.x:
							#print("moving %s to the right" % r.name)
							r.x += b0
						#end if
					#next r
					# Q got moved twice, so we fix that here. Don't think you can fix this.
					q.x -= b0
				#end if
			#next q
		#next p
	#end def sortFix(b0=40)
	
	def addNodeToGroup(self, p, left, right, groups, currGroup = None):
		"""
		Static utility function, finds the right group and adds to right and left bracket functions.
		You are part of a group if you have two connections to the group.
		This function doesn't cover the case of the left bracket. That's handled in the calling function.
		currGroup is an optional attribute designed to optimize which groups we have to check.
		"""
		# TODO: improve this
		myGroups = set()
		myGroup = None
		if currGroup:
			checkGroups = [currGroup]
		else:
			checkGroups = groups
		#end if
		for q in p.conns:
			for group in checkGroups:
				# Can't add anything to a leaf.
				if group.finished: continue
				if q in group.points:
					# I may belong to this group I suppose...
					if group in myGroups:
						# We found our group.
						myGroup = group
						break
					else:
						myGroups.add(group)
					#end if
				#end if
			#next group
			if myGroup != None: break
		#next q
		if myGroup == None and len(myGroups) != 0:
			# Assume we're in the first group. Not very good idea.
			myGroup = list(myGroups)[0]
		#end if
		if myGroup == None:
			# First member creates the group
			myGroup = MapGroup()
			myGroup.addPoint(p)
			groups.append(myGroup)
			if len(left) == 0:
				# Likely Left bracket
				myGroup.left_bracket = p
			else:
				# Likely Right bracket
				myGroup.right_bracket = p
			#end if
		else:
			# Add to existing group
			myGroup.addPoint(p)
			if len(left) == 0 and myGroup.left_bracket == None:
				# Likely Left bracket
				myGroup.left_bracket = p
			elif len(right) == 0 and myGroup.right_bracket == None:
				# Likely Right bracket
				myGroup.right_bracket = p
			#end if
		#end if
		return myGroup
	#end def addNodeToGroup(p, left, right, groups, currGroup)
	
	def groupNodes(self):
		"""
		Requires sortLinear and sortFix to be called first.
		Returns a list of group objects:
			a list of nodes,
			a left bracket,
			a right bracket,
			a finished boolean
		This allows the organization much easier using a minor modification of sortLoop.
		Look at me algorithming.
		"""
		groups = []
		currGroup = None
		
		for p in self.points:
			left = []
			right = []
			for q in p.conns:
				if q.x < p.x:
					left.append(q)
				else:
					right.append(q)
				#end if
			#next q
			if len(left) == 0 or len(right) == 0:
				if len(left) == 1 or len(right) == 1:
					# This is a leaf
					#print('leaf', p.name)
					leafGroup = MapGroup()
					leafGroup.leaf(p)
					groups.append(leafGroup)
				else:
					# This is a node from a group
					#print('node from a group', p.name)
					currGroup = self.addNodeToGroup(p, left, right, groups, currGroup)
				#end if
			else:
				# left and right have something in them.
				if len(left) == 1 or len(right) == 1:
					# We've got a bracket
					if len(left) == 1:
						# Possible left bracket
						# Check to see if I'm the start of the new group.
						lpoints = []
						rpoints = []
						for q in self.points:
							# Don't count yourself
							if q == p: continue
							if q.x < p.x:
								lpoints.append(q)
							else:
								rpoints.append(q)
							#end if
						#next q
						# Expensive on large maps for for for for.
						newGroup = True
						for q in lpoints:
							for r in q.conns:
								if r in rpoints:
									newGroup = False
									break
								#end if
							#next r
							if newGroup == False: break
						#next q
						if newGroup:
							#print('left bracket', p.name)
							newGroup = MapGroup()
							newGroup.addPoint(p)
							groups.append(newGroup)
							currGroup = newGroup
						else:
							#print('node from group 3', p.name)
							currGroup = self.addNodeToGroup(p, left, right, groups, currGroup)
						#end if
					else:
						# Possible right bracket
						#print('right bracket', p.name)
						currGroup = self.addNodeToGroup(p, left, right, groups, currGroup)
					#end if
				else:
					# It's a group node apparently
					#print('node from group 2', p.name)
					currGroup = self.addNodeToGroup(p, left, right, groups, currGroup)
				#end if
			#end if
		#next p
		
		# Fix the problem with node 0 in one group and the rest in another.
		for group in groups:
			if len(group.points) > 2: continue
			# One or two nodes in a group on their own.
			foundConcat = None
			for j in range(len(groups)):
				if group == groups[j]: continue
				for p in group.points:
					conns_in_G = 0
					for q in p.conns:
						if q in groups[j].points:
							conns_in_G += 1
						#end if
					#next q
					if conns_in_G >= 2:
						foundConcat = j
						break
					#end if
				#next p
				if foundConcat != None: break
			#next j
			if foundConcat != None:
				# Move all group members to the found group.
				groups[foundConcat].points.extend(group.points)
				group.points = []
			#end if
		#next group
		
		# Fix the problem of loop_bug3.json where 0 is conn to 5 6
		# Looking for group A is small and connected to group B and C.
		# Group B is small and connected to C also.
		groupsConns = []
		for i, group in enumerate(groups):
			if len(group.points) > 2:
				# Have to put something here for consistency.
				groupsConns.append([])
				continue
			#end if
			# One or two nodes in a group on their own.
			# TODO: We can skip half of these.
			groupConn = [False for j in range(len(groups))]
			for j in range(len(groups)):
				if i == j: continue
				for k in range(len(group.points)):
					p = group.points[k]
					conns_in_G = 0
					for q in p.conns:
						if q in groups[j].points:
							conns_in_G += 1
							break
						#end if
					#next q
					#debug("conns in G: " + conns_in_G + " " + k);
					if conns_in_G > 0:
						groupConn[j] = True
						break
					#end if
				#next p
			#next j
			foundConcat = None
			foundConcat2 = None
			# look for A in groupsConns.
			for j in range(len(groupsConns)):
				#// We are connected to them.
				if groupConn[j]:
					#// Look for the group we are both connected to.
					for k in range(len(groups)):
						#print(groupConn[k], groupsConns[j])
						if groupConn[k] and len(groupsConns[j]) > k and groupsConns[j][k]:
							#// We have found a loop, add ourselves and them.
							foundConcat = k
							foundConcat2 = j
							break
						#end if
					#next k
				#end if
			#next j
			#debug("Concat 2 " + foundConcat + " " + i);
			if foundConcat != None:
				#// Move all group members to the found group.
				groups[foundConcat].points.extend(group.points)
				group.points = []
				group2 = groups[foundConcat2];
				groups[foundConcat].points.extend(group2.points)
				group2.points = []
				#// Have to put something here for consistency.
				groupsConns.append([])
			else:
				groupsConns.append(groupConn)
			#end if
		#next i, group
		
		# FIXME: when a group consumes a second group, cull doesn't work.
		# python3 ../loopsort1.py -x 26 -n 20 -c 2
		# Fix the bug with groups consuming more nodes than just their group.
		# python3 ../loopsort1.py -x 2 -n 20 -c 1
		newGroups = []
		for group in groups:
			nodesOrphaned = group.cull()
			newGroups.extend(nodesOrphaned)
		#next group
		for p in newGroups:
			stemGroup = MapGroup()
			stemGroup.addPoint(p)
			groups.append(stemGroup)
		#next p
		# Filter any blank groups.
		groups = [g for g in groups if len(g.points) > 0]
		# Sort by minimum x value.
		groups.sort(key=lambda g:g.minX())
		return groups
	#end def groupNodes()
	
	def pointToIndex(self):
		# Reverse point to index.
		mapPointToIndex = {}
		for i, p in enumerate(self.points):
			mapPointToIndex[p] = i
		#next i, p
		return mapPointToIndex
	#end def pointToIndex()
	
	def solveDoubleLoop(self, group, inBetweensSet, ungrouped, knownPos, level=0):
		"""
		Solve double diamond problem and so forth.
		a--b--c--d--e--f--g
		a--d
		d--g
		As you can see, there is just one group in this graph.
		"""
		# If this turns up more groups than the original, this is a cull bug we can fix.
		# This seems strange, but believe me it works in all known problem cases.
		groups = self.groupNodes()
		for group_new in groups:
			print('\t', ', '.join([str(p.name) for p in group_new.points]))
		#next group
		equal_groups = False
		group_picked = None
		first_ungrouped = list(ungrouped)[0]
		for group_new in groups:
			if first_ungrouped in group_new.points:
				# This is our group, so check to see if it is equal to group.
				if len(group_new.points) == len(group.points):
					# Same size, must be same data.
					equal_groups = True
					group_picked = group_new
				else:
					# Different group.
					equal_groups = False
					group_picked = group_new
				#end if
				break
			#end if
		#next group
		mapPointToIndex = self.pointToIndex()
		if equal_groups:
			# double diamond problem
			# given a b c, find d, then sortGroup?
			connectors = set()
			for x in ungrouped:
				for v in inBetweensSet:
					if v in x.conns:
						# this is d.
						connectors.add(v)
					#end if
				#next v
			#next x
			print('Found %i connectors' % len(connectors))
			if len(connectors) <= 2:
				# This almost solves double_diamond.json, but the problem is overlap.
				# This is a singly or doubly connected thing, easy, just sort group.
				unGroupedGroup = MapGroup()
				# Use d as the known, this is bound to cause problems, but...
				# This is a trick to get consistency for python3 ../loopsort1.py -x 31 -n 20 -c 2
				connectors_sorted = list(connectors)
				connectors_sorted.sort(key=lambda x: x.x)
				unGroupedGroup.points = connectors_sorted + list(ungrouped)
				ungrouped_nodes = self.sortGroup(unGroupedGroup, knownPos, mapPointToIndex, 40, level + 1)
			#end if
		else:
			# We lucked out, it's a cull problem
			# This is a very cheap algorithm I assume.
			# python3 ../loopsort1.py -x 42 -n 20 -c 2
			groups_solve = set()
			for x in ungrouped:
				for group_new in groups:
					if x in group_new.points:
						groups_solve.add(group_new)
					#end if
				#next group_new
			#next x
			#print('To solve:')
			ungrouped_nodes = 0
			for group_new in groups_solve:
				#print('\t', ', '.join([str(p.name) for p in group_new.points]))
				if len(group_new.points) == 1:
					continue
				elif len(group_new.points) == 2:
					continue
				#end if
				ungrouped_nodes += self.sortGroup(group_new, knownPos, mapPointToIndex, 40, level + 1)
			#next group_new
		#end if
		
	#end def solveDoubleLoop(group, inBetweensSet, ungrouped, level=0)

	def sortLoop(self, b0=40, level=0):
		"""
		Start small, more and more because it will improve the speed of algorithm and optimize.
		Assumes that sortLinear has already been called.
		Uses sortBranch in combination with sortLoop to fix branches.
		"""
		groups = self.groupNodes()
		for group in groups:
			print('\t', ', '.join([str(p.name) for p in group.points]))
		#next group
		
		knownPos = [False for i in self.points]
		# Reverse point to index dictionary.
		mapPointToIndex = self.pointToIndex()
		#print([x.name for x in self.points[5].conns])
		# TODO: optimize this double loop if it becomes an issue (so far not)
		# FIXME: currX is not threadsafe but who would run two sorts at the same time?
		self.currX = None
		#addX = 0
		ungrouped_nodes = 0
		for group in groups:
			if len(group.points) < 1:
				continue
			elif len(group.points) == 1:
				# Single node groups are leaves or stems. For example: a--b--c--d--e
				p = group.points[0]
				if self.currX == None: self.currX = p.x
				#addX += self.currX - p.x
				#print('addX', p.name, addX)
				p.x = self.currX
				#print('self.currX', p.name, self.currX)
				self.currX += b0
				# TODO: May or may not be necessary for leaves:
				#knownPos[mapPointToIndex[p]] = True
				continue
			elif len(group.points) == 2:
				# A two point group? That's an error.
				print("Warning: Groups of two are pretty rare. One might say they shouldn't exist.")
				p = group.points[0]
				if self.currX == None: self.currX = p.x
				#addX += self.currX - p.x
				p.x = self.currX
				#print('self.currX', p.name, self.currX)
				self.currX += b0
				q = group.points[1]
				#addX += self.currX - q.x
				q.x = self.currX
				self.currX += b0
				# TODO: May or may not be necessary for leaves:
				#knownPos[mapPointToIndex[p]] = True
				#knownPos[mapPointToIndex[q]] = True
				continue
			#end if
			ungrouped_nodes += self.sortGroup(group, knownPos, mapPointToIndex, b0)
		#next group
		# If we know nothing, then just run sortBranch normally.
		if knownPos == [False for i in self.points]:
			knownPos = None
		#end if
		self.sortBranch(b0, knownPos)
		if ungrouped_nodes > 1 and level < 1:
			# One expensive not yet working solution is to repeat sort by loop.
			#self.sortLoop(b0, level+1)
			pass
		#end if
	#end def sortLoop(b0=40, level=0)
	
	def sortGroup(self, group, knownPos, mapPointToIndex, b0=40, level=0):
		"""
		Chooses the position of a group based on shape.
		returns the number of nodes in the group that were not positioned.
		# Pentagon and up
		# Pentagon: python3 loopsort1.py -x 8
		# loopsort1_162.json
		# Hexagon: python3 loopsort1.py -x 9
		# loopsort1_163.json
		# Septagon: python3 loopsort1.py -x 7
		# loopsort1_164.json
		# Octagon: python3 loopsort1.py -x 12
		# loopsort1_167.json
		# Octdecagon: python3 loopsort1.py -x 10
		# loopsort1_165.json
		# The first one goes to 180 - 360/shape. cos((pi-(2*pi/shape))), sin((pi-(2*pi/shape)))

		# 108°
		theta1 = (pi-(2*pi/shape))
		pos1 = (cos(theta1), sin(theta1))
		# 72°
		theta2a = pi - theta1
		# 18°
		theta2b = (pi*0.5) - theta2a
		# 108+18-90 = 36°, we could just remove pi*0.5 from theta2b if we wanted to.
		theta2b = theta2b + theta1 - (pi*0.5)
		pos2a = (cos(theta2b), sin(theta2b))
		pos2 = (pos1[0]+pos2a[0], pos1[0]+pos2a[0])
		"""
		# TODO: Ton of little stuff here..
		p, q = None, None
		if group.left_bracket and group.right_bracket:
			print('lb rb', end=" ")
			p, q = group.left_bracket, group.right_bracket
			if q not in p.conns:
				# Find the correct q in p.conns
				best_q = None
				maxConns = 0
				for q_test in p.conns:
					if q_test.x > p.x and len(q_test.conns) > maxConns:
						maxConns = len(q_test.conns)
						best_q = q_test
					#end if
				#next q_test
				q = best_q
				if q == None:
					print("Error: Unable to find a valid q 1")
					q = group.right_bracket
				#end if
			#end if
			print('p=%s, q=%s' % (p.name, q.name))
		#end if

		# Find p and q amongst the group. Naturally the furthest left.
		if group.left_bracket:
			print('lb', end=" ")
			p = group.left_bracket
		else:
			print('*shrug*', end=" ")
			p = group.points[0]
		#end if
		"""q = group.points[1]
		if p == q:
			q = group.points[0]
			if p == q:
				print("Error: bug in inBetweens code")
			#end if
		#end if"""
		#if q not in p.conns:
		# Find the correct q in p.conns
		best_q = None
		maxConns = 0
		for q_test in p.conns:
			#print(q_test.name, 'has', len(q_test.conns), 'conns')
			# We don't want any other groups in our group.
			if q_test not in group.points: continue
			if len(q_test.conns) > maxConns:
				maxConns = len(q_test.conns)
				best_q = q_test
			#end if
		#next q_test
		q = best_q
		if q == None:
			print("Error: Unable to find a valid q 2", group.right_bracket)
			q = group.right_bracket
			return 0
		#end if
		#end if
		#print('p=%s, q=%s' % (p.name, q.name))

		# Find p, q, and inBetweens correctly!
		inBetweens = self.findRoute(p, q)
		
		if len(inBetweens) > len(group.points):
			# We're using parts of a connected group, verify that we're using 
			# the least possible of it.
			inBetweensSet = set(inBetweens)
			groupSet = set(group.points)
			diff = inBetweensSet.difference(groupSet)
			found_unconn = []
			for v in diff:
				connected = False
				for q in groupSet:
					if q in v.conns:
						connected = True
						break
					#end if
				#next q
				if not connected:
					found_unconn.append(v)
					#break
				#end if
			#next v
			if len(found_unconn) > 0:
				print("Found unconnected nodes:", [v.name for v in found_unconn])
				# Find a route that avoids one of the unconnected.
				inBetweens_test = self.findRoute(p, q, [found_unconn[0]])
				if inBetweens_test != None:
					inBetweens_testSet = set(inBetweens_test)
					diff_test = inBetweens_testSet.difference(groupSet)
					# Choose the shorter of the two:
					if len(diff_test) < len(diff):
						print("Found a shorter route:", [v.name for v in inBetweens], [v.name for v in inBetweens_test])
						inBetweens = inBetweens_test
					#end if
				#end if
			#end if
		#end if
		
		if self.currX == None: self.currX = p.x
		#p.x = self.currX
		#print('self.currX', p.name, self.currX)
		
		#TODO: Fix addX here.
		#addX += self.currX - p.x
		# There's always two nodes inline, the rest are perpendicular.
		self.currX += b0 * 2
		# This can be fixed by setting the shape based on len of inBetweens, I suppose.
		#if len(inBetweens) != (shape):
		#	print("inBetweens are different size.", ', '.join([str(x) for x in inBetweens]))
		#	continue
		#end if
		shape = len(inBetweens)
		# Simple bug to fix.
		if shape == 1:
			print("findRoute bug", [v.name for v in group.points])
			return 0
		#end if
		print("Picked ngon %i %s" % (shape, p.name), [v.name for v in inBetweens], [v.name for v in group.points])
		# Using this method make a loop over shape for each vertex
		prevPos = (p.x, p.y)
		pos = []
		theta_inner = (2*pi/shape)
		for i in range(1, shape):
			theta_i = pi-(theta_inner*i)
			pos_i = (b0*cos(theta_i), b0*sin(theta_i))
			pos.append((pos_i[0] + prevPos[0], pos_i[1] + prevPos[1]))
			prevPos = pos[-1]
		#next i
		# Skip p.
		for i, x in enumerate(inBetweens[1:]):
			x.x = pos[i][0]
			x.y = pos[i][1]
		#next i, x
		# Move all the others left shape - 2.
		"""
		dx = b0 * (shape - 2)
		further = q
		if q.x < p.x: further = p
		for ttr in self.points:
			if ttr in inBetweens: continue
			if ttr.x >= further.x:
				ttr.x -= dx
			#end if
		#next ttr
		"""
		knownPos[mapPointToIndex[p]] = True
		knownPos[mapPointToIndex[q]] = True
		for inBetween in inBetweens:
			knownPos[mapPointToIndex[inBetween]] = True
			# Solve the moving issue.
			#inBetween.x += addX
		#next inBetween
		
		# Detect multiple loops in a single group
		ungrouped_nodes = 0
		# level < 1 needed to avoid infinite recursion
		if len(inBetweens) < len(group.points) and level < 1:
			inBetweensSet = set(inBetweens)
			groupSet = set(group.points)
			ungrouped = groupSet.difference(inBetweensSet)
			print('Ungrouped:', ', '.join([x.name for x in ungrouped]))
			self.solveDoubleLoop(group, inBetweensSet, ungrouped, knownPos, level)
			ungrouped_nodes = len(ungrouped)
		#end if
		return ungrouped_nodes
	#end def sortGroup(group, knownPos, mapPointToIndex, b0=40, level=0)
	
	def toGrid(self, width=40):
		"""
		Unlike sortGrid, toGrid uses input positions to decide which cell to place 
		nodes in. It returns a grid (array of array of points and/or arrays).
		TODO: Improve the quality of position picking.
		"""
		r = self.bounds()
		dx = r[2] - r[0]
		dy = r[3] - r[1]
		cols = ceil(2 * dx / width)
		rows = ceil(2 * dy / width)
		nearby = [[0, 1], [1, 1], [1, 0], [0, -1], [-1, 0], [-1, 1], [-1, -1], [1, -1]]
		grid = []
		for i in range(rows):
			grid.append([None] * cols)
		#next i
		min_x = r[0]
		min_y = r[1]
		for p in self.points:
			row = round((p.y - min_y) / width)
			col = round((p.x - min_x) / width)
			# Check for a nearby empty spot.
			found = False
			for near in nearby:
				if row+near[1] < 0: continue
				if col+near[0] < 0: continue
				if grid[row+near[1]][col+near[0]] == None:
					grid[row+near[1]][col+near[0]] = p
					found = True
					break
				#end if
			#next near
			if not found:
				if grid[row][col]:
					if type(grid[row][col]) == list:
						grid[row][col].append(p)
					else:
						grid[row][col] = [grid[row][col], p]
					#end if
				else:
					grid[row][col] = p
				#end if
			#end if
		#next p
		# Should this be optional? Perhaps.
		gridToPos(grid, width)
		return grid
	#end def toGrid(width=40)

	def density(self, width=40):
		"""
		Based on toGrid, we add up information about where there are nodes.
		Returns a 2d array of integers.
		"""
		r = self.bounds()
		dx = r[2] - r[0]
		dy = r[3] - r[1]
		cols = ceil(dx / width) + 1
		rows = ceil(dy / width) + 1
		#print('rc', rows, cols, 'd', dy, dx)
		grid = []
		for i in range(rows):
			grid.append([0] * cols)
		#next i
		min_x = r[0]
		min_y = r[1]
		for p in self.points:
			row = round((p.y - min_y) / width)
			col = round((p.x - min_x) / width)
			#print(row, col)
			# increment this position
			grid[row][col] += 1
		#next p
		return grid
	#end def density(width=40)

	def sortGridNoRearrange(self, width=40):
		"""
		Equivalent to sortGrid(width, False)
		Faster because it doesn't rearrange Nodes, which is expensive.
		We only need this function so we can do getattr(userdata) in grid1.py
		"""
		return self.sortGrid(width, False)
	#end def sortGridNoRearrange(width)

	def sortGrid(self, width=40, rearrange=True):
		"""
		Create an NxM grid, place one node per cell. This simplifies the branch sort algorithm into a lattice instead of a trigonometry problem.
		"""
		nodes = len(self.points)
		if nodes <= 1:
			# Congratulations, you're guaranteed to be sorted.
			return
		#end if
		# Allocating all at the start will become a mess with large values of num_points, so we make it extensible.
		knownPos = [False] * nodes
		grid_rows = 2
		grid_cols = 2
		grid = []
		for i in range(grid_rows):
			grid.append([None] * grid_cols)
		#next i
		#print(grid)
		grid[0][0] = self.points[0]
		knownPos[0] = True
		# This is bound to change because of extensible. That sucks.
		pointPosMap = {0: [0, 0]}
		# FIXME: Not sure what the right number is, need some cheap boolean detector.
		for roundTry in range(nodes):
			#print("fillReady?", fillReady)
			for i in range(nodes):
				givens = []
				unknowns = []
				# Set the position of its connections.
				for conn in self.points[i].conns:
					j = self.points.index(conn)
					if knownPos[j]:
						givens.append(j)
						continue
					#end if
					unknowns.append(j)
				#next conn
				if knownPos[i]:
					if len(unknowns) == 0:
						# Everything is known, we're good.
						#print('Yay', map1.points[i].x, map1.points[i].y)
						continue
					#end if
					#print('sorting from', map1.points[i].name)
					j = 0
					# Put the unknowns on the grid near the position of the point.
					pos_i = pointPosMap[i]
					#print(pointPosMap, i)
					left = [pos_i[0]-1, pos_i[1]]
					right = [pos_i[0]+1, pos_i[1]]
					up = [pos_i[0], pos_i[1]-1]
					down = [pos_i[0], pos_i[1]+1]
					ul = [pos_i[0]-1, pos_i[1]-1]
					ur = [pos_i[0]+1, pos_i[1]-1]
					dl = [pos_i[0]-1, pos_i[1]+1]
					dr = [pos_i[0]+1, pos_i[1]+1]
					change = [0, 0]
					for p in [left, right, up, down, ul, ur, dl, dr]:
						# Move the p where it should go based on additions.
						p[0] += change[0]
						p[1] += change[1]
						#print('try', p)
						dp = None
						if p[0] + change[0] < 0:
							# available, but we will need to extend left, maybe up or down
							# Extend left
							#print(map1.points[unknowns[j]].name, end=' ')
							#print('extend left', end='')
							for k in range(grid_rows):
								grid[k] = [None] + grid[k]
							#next k
							grid_cols += 1
							dp = [1, 0]
							change[0] += 1
							if p[1] < 0:
								# Extend up
								#print(', extend up', end='')
								grid.insert(0, [None] * grid_cols)
								grid_rows += 1
								dp[1] = 1
								change[1] += 1
							#end if
							if p[1] > grid_rows:
								# Extend down
								#print(', extend down', end='')
								grid.append([None] * grid_cols)
								grid_rows += 1
							#end if
							#print()
							grid[p[1]+dp[1]][p[0]+dp[0]] = self.points[unknowns[j]]
							pointPosMap[unknowns[j]] = [p[0], p[1]]
							knownPos[unknowns[j]] = True
							#print("set %s to %r" % (map1.points[unknowns[j]].name, p))
							j += 1
							if j >= len(unknowns):
								break
							#end if
						elif p[0] >= grid_cols:
							# available, but we will need to extend right
							# Extend right
							#print(map1.points[unknowns[j]].name, end=' ')
							#print('extend right', end='')
							for k in range(grid_rows):
								grid[k] += [None]
							#next k
							grid_cols += 1
							dp = [0, 0]
							if p[1] < 0:
								# Extend up
								#print(', extend up', end='')
								grid.insert(0, [None] * grid_cols)
								grid_rows += 1
								dp[1] = 1
								change[1] += 1
							#end if
							if p[1] > grid_rows:
								# Extend down
								#print(', extend down', end='')
								grid.append([None] * grid_cols)
								grid_rows += 1
							#end if
							#print()
							grid[p[1]+dp[1]][p[0]+dp[0]] = self.points[unknowns[j]]
							pointPosMap[unknowns[j]] = [p[0], p[1]]
							knownPos[unknowns[j]] = True
							#print("set %s to %r" % (map1.points[unknowns[j]].name, p))
							j += 1
							if j >= len(unknowns):
								break
							#end if
						elif p[1] < 0:
							# available, but we will need to extend up
							# Extend up
							#print(map1.points[unknowns[j]].name, end=' ')
							#print('extend up')
							grid.insert(0, [None] * grid_cols)
							grid_rows += 1
							dp = [0, 1]
							change[1] += 1
							grid[p[1]+dp[1]][p[0]+dp[0]] = self.points[unknowns[j]]
							pointPosMap[unknowns[j]] = [p[0], p[1]]
							knownPos[unknowns[j]] = True
							#print("set %s to %r" % (map1.points[unknowns[j]].name, p))
							j += 1
							if j >= len(unknowns):
								break
							#end if
						elif p[1] >= grid_rows:
							# available, but we will need to extend down
							# Extend down
							#print(map1.points[unknowns[j]].name, end=' ')
							#print('extend down')
							grid.append([None] * grid_cols)
							grid_rows += 1
							grid[p[1]][p[0]] = self.points[unknowns[j]]
							pointPosMap[unknowns[j]] = [p[0], p[1]]
							knownPos[unknowns[j]] = True
							#print("set %s to %r" % (map1.points[unknowns[j]].name, p))
							j += 1
							if j >= len(unknowns):
								break
							#end if
						elif grid[p[1]][p[0]] == None:
							#print(map1.points[unknowns[j]].name, end=' ')
							#print('in spot')
							# available, put it there.
							grid[p[1]][p[0]] = self.points[unknowns[j]]
							pointPosMap[unknowns[j]] = [p[0], p[1]]
							knownPos[unknowns[j]] = True
							#print("set %s to %r" % (map1.points[unknowns[j]].name, p))
							j += 1
							if j >= len(unknowns):
								break
							#end if
						#end if
						# Fix the pointPosMap using generated dp. 
						# TODO: do this after the loop for optimization.
						if dp and dp != [0, 0]:
							#print("Fix ppm using", dp)
							for v in pointPosMap:
								pointPosMap[v][0] += dp[0]
								pointPosMap[v][1] += dp[1]
							#next v
							dp = None
						#end if
					#next p
					# Fix the pointPosMap using generated dp. 
					# NOTE: this is a minor hack. See above the same code. This is here because of the breaks.
					if dp and dp != [0, 0]:
						#print("Fix ppm 2 using", dp)
						for v in pointPosMap:
							pointPosMap[v][0] += dp[0]
							pointPosMap[v][1] += dp[1]
						#next v
					#end if
					#print(pointPosMap)
				else:
					# Deal with other things later
					pass
				#end if
			#next i
			if not (False in knownPos):
				break
			#end if
		#next roundTry
		printVerbose("%i rounds" % (roundTry + 1))
		if False in knownPos:
			#print(knownPos)
			#print([self.points[i].name for i in range(len(knownPos)) if not knownPos[i]])
			# TODO: Try to put the unset nodes in slots that are empty near their connections.
			for i in range(len(knownPos)):
				if knownPos[i]: continue
				foundPos = False
				for y in range(len(grid)):
					for x in range(len(grid[0])):
						if grid[y][x] == None:
							grid[y][x] = self.points[i]
							pointPosMap[i] = [x, y]
							#print("set %s to %r" % (map1.points[i].name, (x, y)))
							foundPos = True
							break
						#end if
					#next x
					if foundPos: break
				#next y
				if not foundPos:
					# We need to extend, which is almost never. euler's identity repros this.
					grid.append([None] * grid_cols)
					grid_rows += 1
					grid[-1][0] = self.points[i]
					pointPosMap[i] = [grid_rows - 1, 0]
				#end if
			#next i
		#end if
		
		if rearrange and len(pointPosMap) < len(self.points):
			print("Error: pointPosMap is broken, we can't rearrange.")
			rearrange = False
		#end if
		if rearrange:
			# Improve the potential dramatically at a very high cost.
			#for i in range(10):
			#	if not rearrangeGrid(map1, grid, pointPosMap, 40):
			#		break
			#	#end if
			#next i
			self.rearrangeGrid(grid, pointPosMap, 40)
		#end if
		# Then set the points' positions.
		gridToPos(grid, width)
		return grid
	#end def sortGrid(width=40, rearrange=True)
	
	def rearrangeGrid(self, grid, pointPosMap, width=40, nonConns=None):
		"""
		Reduce potential using algorithm designed last night.
		TODO: auto loop sort of groups on the grid
		Let's solve grid1_128331410_1009.json
		Repro:
		python3 grid1.py -n 16 -c 2 -b 0 -x 3033139000
		Returns True on improvement, False when there is no improvement.
		You do not need to run gridToPos before or after rearrangeGrid, but if you 
		don't and rearrangeGrid returns False, then you will have map1 back as it 
		was, thus the code at the bottom of sortGrid is _correct_ so long as this 
		is true.
		The only bug to be fixed for this graph is adding another row when necessary and putting a node there.
		This algorithm doesn't attempt that.
		FIXME: This is slow even with caching. We must do whatever we can to 
		improve the speed of this as well as deciding not to use it.
		"""
		# TODO: a strange circular dependency, not good, eventually just incorporate.
		global V_Harmonic, V_Harmonic_Angle
		from sww_optimize1 import LJ_Potential, V_SmallWideWorld, V_Harmonic, V_Harmonic_Angle, ConnList
		b0 = 40
		lj_conf = LJ_Potential()
		gridToPos(grid, width)
		x0, conns = self.getX0Conns(True)
		conns_cpp = ConnList(conns)
		if nonConns is None:
			nonConns = getNonConns(conns, True)
		#end if
		nonConns_cpp = ConnList(nonConns)
		V_init = V_SmallWideWorld(x0, conns_cpp, b0, lj_conf, nonConns_cpp)
		#print("V_init:", V_init)
		nodes = len(self.points)
		minV = V_init
		x_out = self.getX0Conns()[0]
		best_x = x_out
		ret = False
		
		for roundTry in range(10):
			madeImprovement = False
			for i in range(nodes):
				# The cache is made up of the potential minus this node's contribution.
				V_cache = PotentialCache(0, i)
				# TODO: C++ version!
				V_node_i = V_SmallWideWorld_Cache(x_out, conns, b0, lj_conf, nonConns, V_cache)
				V_cache.PotentialA = minV - V_node_i
				pos_i = pointPosMap[i]
				for conn in self.points[i].conns:
					j = self.points.index(conn)
					pos_j = pointPosMap[j]
					dx = pos_i[0] - pos_j[0]
					dy = pos_i[1] - pos_j[1]
					dr_sq = (dx * dx) + (dy * dy)
					if dr_sq <= 1:
						# Don't worry about this bond. It's fine.
						continue
					#end if
					# Get a list of positions we can pick for this one...
					possiblePos = getOptionsList(pos_i, pos_j)
					#print(pos_i, pos_j, possiblePos)
					
					best_pos = None
					valid_positions = 0
					for pos in possiblePos:
						if pos[1] >= len(grid) or pos[0] >= len(grid[0]): continue
						if pos[1] < 0 or pos[0] < 0: continue
						# Don't put two in the same place.
						if grid[pos[1]][pos[0]] != None: continue
						valid_positions += 1
						x_out[2 * i] = width * pos[0]
						x_out[2 * i + 1] = width * pos[1]
						#V_i = V_SmallWideWorld(x_out, conns, b0, lj_conf, nonConns)
						V_i = V_SmallWideWorld_Cache(x_out, conns, b0, lj_conf, nonConns, V_cache)
						if V_i < minV:
							#print("Improved V_i: %f when %s moved to %r" % (V_i, map1.points[i].name, pos))
							minV = V_i
							best_x = x_out[:]
							best_pos = pos
						#end if
					#next pos
					dx = abs(pos_i[0] - pos_j[0])
					dy = abs(pos_i[1] - pos_j[1])
					if valid_positions == 0:
						possiblePos = []
						if dx == 0:
							# Try above and below, assuming we can.
							possiblePos = [[pos_j[0] - 1, pos_j[1]], [pos_j[0] + 1, pos_j[1]]]
							if pos_j[0] == 0:
								possiblePos.pop(0)
								#print("Can't go up.")
							elif pos_j[0] >= len(grid):
								possiblePos.pop(1)
								#print("Can't go down.")
							#end if
						#end if
						if dy == 0:
							# Try above and below, assuming we can.
							possiblePos = [[pos_j[0], pos_j[1] - 1], [pos_j[0], pos_j[1] + 1]]
							if pos_j[1] == 0:
								possiblePos.pop(0)
								#print("Can't go up.")
							elif pos_j[1] >= len(grid):
								possiblePos.pop(1)
								#print("Can't go down.")
							#end if
						#end if
						#print('Trying %s with' % self.points[i].name, possiblePos, pos_i, pos_j)
						for pos in possiblePos:
							if len(grid) <= pos[1]: continue
							if len(grid[0]) <= pos[0]: continue
							# Don't put two in the same place.
							if grid[pos[1]][pos[0]] != None: continue
							valid_positions += 1
							x_out[2 * i] = width * pos[0]
							x_out[2 * i + 1] = width * pos[1]
							#V_i = V_SmallWideWorld(x_out, conns, b0, lj_conf, nonConns)
							V_i = V_SmallWideWorld_Cache(x_out, conns, b0, lj_conf, nonConns, V_cache)
							if V_i < minV:
								#print("Improved V_i: %f when %s moved to %r" % (V_i, map1.points[i].name, pos))
								minV = V_i
								best_x = x_out[:]
								best_pos = pos
							#end if
						#next pos
						#print("Got %i valid positions." % valid_positions)
					#end if
					if best_pos is not None:
						# Change the map
						m = np.matrixlib.matrix(best_x)
						m = m.reshape(len(self.points), 2)
						self.setPos([np.array(xa)[0] for xa in m])
						# Change the grid
						#print("name: %s pos %r" % (map1.points[i].name, pointPosMap[i]))
						#print('removing %s from grid pos %r' % (grid[pointPosMap[i][1]][pointPosMap[i][0]].name, pointPosMap[i]))
						grid[pointPosMap[i][1]][pointPosMap[i][0]] = None
						pointPosMap[i] = best_pos
						grid[best_pos[1]][best_pos[0]] = self.points[i]
						#print('added %s from grid pos %r' % (grid[best_pos[1]][best_pos[0]].name, best_pos))
						ret = True
						madeImprovement = True
					else:
						# Reset x_out
						x_out = best_x
					#end if
				#next conn
			#next i
			#print("mi", madeImprovement)
			if madeImprovement == False: break
		#next roundTry
		if ret: printVerbose("Improvement: %3.3f" % (V_init - minV))
		return ret
	#end def rearrangeGrid(grid, pointPosMap, width=40, nonConns=None)

	def sortRightLoop(self, b0=40):
		"""
		A simple algorithm using breadth first.
		"""
		nodes = len(self.points)
		if nodes < 1: return
		self.points[0].setPos(Vector2(0, 0))
		# Guaranteed to be sorted if nodes == 0 or 1.
		if nodes < 2: return
		knowns = set([self.points[0]])
		neighbors = self.points[0].conns
		x = b0
		for roundTry in range(nodes):
			newNeighbors = []
			y = (len(neighbors) - 1)*-b0*0.5
			for point in neighbors:
				# Put point on a line to the right depending on how many neighbors.
				point.x = x
				point.y = y
				y += b0
				newNeighbors.extend(point.conns)
				knowns.add(point)
			#next point
			x += b0
			neighbors = [p for p in newNeighbors if p not in knowns]
			if len(knowns) >= nodes: break
		#next roundTry
	#end def sortRightLoop(b0=40)

	def sortFruchtermanReingold(self, k=24., t=None):
		"""
		Given a position, attempt to improve the position.
		Use strange type of springs to decide the position of each point.
		Fruchterman, T. M. J., & Reingold, E. M. (1991). Graph Drawing by Force-Directed Placement. Software: Practice and Experience, 21(11).
		"""
		# Deal with optional parameters.
		if t == None: t = k * 0.15
		v_disp = []
		# Avoid divide by zero.
		if k < 1e-20: k = 1e-20
		k_sq = k * k
		inv_k = 1 / k
		# Calculate repulsive forces
		for i, point in enumerate(self.points):
			v_disp_i = Vector2(0, 0)
			for j in range(len(self.points)):
				if i == j: continue
				# delta is shorthand for the difference.
				# vector between the positions of the two vertices.
				delta = point - self.points[j]
				# TODO: inverse sqrt.
				delta_len_sq = delta.lensq()
				# If they are too close, limit the force to avoid divide by zero error.
				if delta_len_sq < 1e-20: delta_len_sq = 1e-20
				inv_delta_len_sq = 1. / delta_len_sq
				v_disp_i = v_disp_i + (delta * (+inv_delta_len_sq * +k_sq))
			#next j
			v_disp.append(v_disp_i)
		#next point
		#debug('repulsion: ' + v_disp.map(function(x) { return '(' + x.x + ', ' + x.y + ')'; }).join(', '));
		
		# Calculate attractive forces
		for i, point in enumerate(self.points):
			for conn in point.conns:
				# NOTE: I could use getX0Conns instead if it's faster.
				m = self.points.index(conn)
				# Don't do both directions. Each edge should be counted once.
				if i >= m: continue
				#debug(point.name + " conn " + this.points[m]);
				delta = point - conn
				delta_len = delta.length()
				# (delta / delta_len) * (delta_len * delta_len / k) == delta * delta_len / k
				dr = delta * (delta_len * inv_k)
				v_disp[i] = v_disp[i] - dr
				v_disp[m] = v_disp[m] + dr
			#next conn
		#next i, point
		#debug('after attraction: ' + v_disp.map(function(x) { return '(' + x.x + ', ' + x.y + ')'; }).join(', '));
		
		# Limit the maximum displacement to the temperature t
		# and then prevent from being displaced outside frame.
		for i in range(len(self.points)):
			v_disp_i_len = v_disp[i].length()
			# This is silly but allows t to reduce the maximum displacement over iterations.
			self.points[i].setPos(self.points[i] + (v_disp[i] * min(v_disp_i_len, t) / v_disp_i_len))
		#next i
		
		# Reduce the temperature as the layout approaches a better configuration.
		# When calling sortFruchtermanReingold, reduce the t variable over iterations.

	#end def sortFruchtermanReingold(k=24., t=k*0.15)
	
	def sortFruchtermanReingoldLoop(self, k=24., t=None, iterations=50, dt=0.9):
		"""
		Run sortFruchtermanReingold in a loop
		dt is the factor t is multiplied by each loop
		control t better with higher iterations using larger dt.
		Reasonable value table:
		iterations dt
		50         0.9
		200        0.98
		1000       0.998
		TODO: It should be possible to compute this factor dt.
		"""
		if t == None: t = k * 0.15
		for i in range(iterations):
			self.sortFruchtermanReingold(k, t)
			t = t * dt
			if i & 0xff == 0: print('Iteration:', i)
		#next i
	#end sortFruchtermanReingoldLoop(k=24., t=k*0.15, iterations=50)

	def sortBest(self, width=40, rearrange=True):
		"""
		sortGrid, sortBranch, and sortLoop, pick whichever has lowest potential.
		"""
		from sww_optimize1 import LJ_Potential, V_SmallWideWorld, V_Harmonic, V_Harmonic_Angle, ConnList
		lj_conf = LJ_Potential()
		x0, conns = self.getX0Conns(True)
		conns_cpp = ConnList(conns)
		#print(x0)
		#if verbose:
		#	print("atom conns:", conns)
		#end if
		nonConns = ConnList(getNonConns(conns, True))

		# Not necessary to get spherical coordinates of the original coordinates.
		#output = [spherical2.cartesianToSpherical(v) for v in molecule.x0]
		#print("Spherical coordinates of atoms:")
		#print(output)
		
		# This may be used eventually
		#sphericalCoords, atom_name_hash = molecule.toSpherical(verbose)
		self.sortBranch(width)
		x_out = self.getX0Conns()[0]
		V_branch = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns)

		self.sortLinear(width)
		self.sortLoop(width)
		x_out = self.getX0Conns()[0]
		V_loop = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns)
		
		dV = V_branch - V_loop
		if dV < 0:
			bestSort = 'branch'
			V_best = V_branch
		else:
			bestSort = 'loop'
			V_best = V_loop
		#end if

		self.sortLattice(width)
		x_out = self.getX0Conns()[0]
		V_lattice = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns)
		if V_best > V_lattice:
			bestSort = 'lattice'
			V_best = V_lattice
		#end if
		
		self.sortSpiral(width)
		x_out = self.getX0Conns()[0]
		V_spiral = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns)
		if V_best > V_spiral:
			bestSort = 'spiral'
			V_best = V_spiral
		#end if
		
		self.sortRandomTheta(width)
		x_out = self.getX0Conns()[0]
		V_randTheta = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns)
		if V_best > V_randTheta:
			bestSort = 'randomTheta'
			V_best = V_randTheta
		#end if
		
		self.sortRightLoop(width)
		x_out = self.getX0Conns()[0]
		V_rightLoop = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns)
		#print('V_rL', V_rightLoop)
		if V_best > V_rightLoop:
			bestSort = 'rightLoop'
			V_best = V_rightLoop
		#end if

		self.sortGrid(width, rearrange)
		x_out = self.getX0Conns()[0]
		V_grid = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns)
		#print("Branch Potential:", V_branch)
		#print("Grid dt: %3.3f seconds" % grid_dt)
		#print("Grid Potential:", V_grid)
		dV = (V_best - V_grid)
		#print("%s - Grid: %3.3f" % (bestSort, dV))
		if dV < 0:
			#print("Note: Branch is lower, see %s" % base_filename)
			if bestSort == 'loop':
				self.sortLinear(width)
				self.sortLoop(width)
			elif bestSort == 'lattice':
				self.sortLattice(width)
			elif bestSort == 'spiral':
				self.sortSpiral(width)
			elif bestSort == 'randomTheta':
				self.sortRandomTheta(width)
			elif bestSort == 'rightLoop':
				self.sortRightLoop(width)
			else:
				self.sortBranch(width)
			#end if
		#end if
		self.centerBound()
	#end def sortBest(width=40, rearrange=True)

	def findRoute(self, p, q, avoid=None, level=0):
		"""
		Given two connected Points, find a route not directly connecting the two.
		Returns a list of Points or None in case of failure.
		Dijkstra would rock, but I'm just a hacker, not a computer scientist. j/k
		See Dijkstra below.
		FIXME: This algorithm has a single flaw in 6000 graphs grid1z54/grid1_3486724715_4957lattice.json
		"""
		#return self.dijkstra(p, q, avoid)
		if avoid == None:
			avoid = [p]
		else:
			avoid = [p] + avoid
		#end if
		foundRoute = None
		for conn in p.conns:
			# We don't want to go backwards, infinite recursion.
			if conn in avoid: continue
			if conn != q:
				v = self.findRoute(conn, q, avoid, level + 1)
				if v: 
					#print('found route', ', '.join([str(x) for x in v]))
					foundRoute = [p] + v
					return foundRoute
				#end if
			else:
				# We got a path, but we might not want it.
				# Check if we just started.
				if level > 0:
					return [p, q]
				elif foundRoute == None:
					# TODO: Verify this somehow...
					foundRoute = [q]
				#end if
			#end if
		#next conn
		return foundRoute
	#end def findRoute(p, q, avoid=None)
	
	def dijkstra(self, p, q, avoid=None):
		"""
		Find shortest path. Solves the exponential findRoute problem.
		"""
		dist, rev = self.getDijkstra(p, avoid)
		# Now to find the path from p to q.
		path = [q]
		step = q
		while step != p and step != None:
			path.append(rev[self.points.index(step)])
			step = path[-1]
		#loop
		path.reverse()
		return path
	#end def dijkstra(p, q, avoid=None)
	
	def getDijkstra(self, p, avoid=None):
		"""
		Find shortest path. Solves the exponential findRoute problem.
		TODO: Use avoid list.
		"""
		if avoid == None:
			avoid = []
		#end if
		visited = set()
		dist = [1<<32] * len(self.points)
		rev = [None] * len(self.points)
		#rev[self.points.index(p)] = p
		dist[self.points.index(p)] = 0
		#print(dist)
		H = []
		H = [[dist[i], self.points[i]] for i in range(len(self.points))]
		#print(H)
		heapq.heapify(H)
		#for i in range(len(self.points)):
		#	print((dist[i], self.points[i]))
		#	heapq.heappush(H, (dist[i], self.points[i]))
		#next i
		# This algorithm gives
		while len(H) > 0:
			# Always gives us the lowest, assuming we've heaped properly.
			u = heapq.heappop(H)[1]
			if u in avoid: continue
			u_i = self.points.index(u)
			for v in u.conns:
				if v in avoid: continue
				v_i = self.points.index(v)
				#print('Checking dist for ', str(v), ':', dist[v_i], dist[u_i] + 1)
				if dist[v_i] > dist[u_i] + 1: # l(u, v)
					dist[v_i] = dist[u_i] + 1 #l(u, v)
					rev[v_i] = u
					#print(str(v))
					#decreasekey(H, v)
					# TODO: use some sort of better logic.
					for x in H:
						if x[1] == v:
							x[0] = dist[v_i]
							break
					#next x
					heapq.heapify(H)
				#end if
			#next v
		#loop
		return dist, rev
	#end def getDijkstra(self, p, avoid=None)

	def center(self):
		"""
		Takes the average and puts the center there. This doesn't work with 
		clusters of nodes with nodes far off. This works when you want to bias 
		toward a cluster.
		"""
		if len(self.points) == 0:
			return
		#end if
		mean = Vector2(0,0)
		for point in self.points:
			mean += point
		#next point
		mean /= (1.0 * len(self.points))
		goto = Vector2(self.width/2.0, self.height/2.0)
		diff = goto - mean
		for point in self.points:
			point.x += diff.x
			point.y += diff.y
		#next point
	#end def center()
	
	def centerBound(self):
		"""
		Instead of averaging, this puts the center based on the mean of the 
		bounds. This works with pretty much all graphs.
		"""
		if len(self.points) == 0:
			return
		#end if
		bounds = self.bounds()
		mean = (Vector2(*bounds[:2]) + Vector2(*bounds[2:])) / 2.0
		goto = Vector2(self.width/2.0, self.height/2.0)
		diff = goto - mean
		for point in self.points:
			point.x += diff.x
			point.y += diff.y
		#next point
	#end def centerBound()
	
	def move(self, x, y):
		"""
		Move everything on the map to offset x, y.
		"""
		if len(self.points) == 0:
			return
		#end if
		for point in self.points:
			point.x += x
			point.y += y
		#next point
	#end def move(x, y)

	def bounds(self):
		"""
		Find the maximum extents.
		returns (x_min, y_min, x_max, y_max)
		"""
		if len(self.points) == 0:
			return
		#end if
		# x_min, y_min, x_max, y_max
		minp = self.points[0] + Vector2(0, 0)
		maxp = minp + Vector2(0, 0)
		for point in self.points:
			if point.x < minp.x: minp.x = point.x
			if point.y < minp.y: minp.y = point.y
			if point.x > maxp.x: maxp.x = point.x
			if point.y > maxp.y: maxp.y = point.y
		#next point
		return (minp.x, minp.y, maxp.x, maxp.y)
	#end def bounds()
	
	def squash(self):
		"""
		FIXME: Broken function.
		"""
		mean = Vector2(0,0)
		for point in self.points:
			#mean[0] += point.x
			#mean[1] += point.y
			mean += point
		#next point
		#mean[0] /= (1.0 * len(self.points))
		#mean[1] /= (1.0 * len(self.points))
		mean /= (1.0 * len(self.points))
		#goto = [self.width/2.0, self.height/2.0]
		goto = Vector2(self.width/2.0, self.height/2.0)
		#diff = [goto[0]-mean[0], goto[1]-mean[1]]
		diff = goto - mean
		for point in self.points:
			#point.x += diff[0]
			#point.y += diff[1]
			for conn in point.conns:
				# FIXME: This doesn't make any sense.
				point.x += diff.x
				point.y += diff.y
			#next conn
		#next point
	#end def squash()
	
	def split(self):
		"""
		Return a list of independent graphs.
		"""
		output = [set() for p in self.points]
		where_is_x = list(range(len(self.points)))
		revMap = {}
		for i in range(len(self.points)):
			revMap[self.points[i]] = i
		#next i
		# First step: merge all connections together.
		for i in range(len(self.points)):
			ourSlot = None
			for conn in self.points[i].conns:
				j = revMap[conn]
				if len(output[j]) > 0:
					if ourSlot != None:
						# Incorporate their useless map.
						output[ourSlot].update(output[j])
						for p in output[j]:
							where_is_x[revMap[p]] = ourSlot
						#next p
						output[j] = set()
					else:
						ourSlot = j
					#end if
					#print(self.points[i].name, 'going to', self.points[j].name)
				#end if
			#next conn
			if ourSlot == None:
				x = where_is_x[i]
				output[x].update([self.points[i]] + self.points[i].conns)
				for conn in self.points[i].conns:
					where_is_x[revMap[conn]] = x
				#next conn
				#if i == 328: print("ourSlot is none, so ", where_is_x[i])
			else:
				where_is_x[i] = ourSlot
				output[ourSlot].update([self.points[i]] + self.points[i].conns)
				for conn in self.points[i].conns:
					where_is_x[revMap[conn]] = ourSlot
				#next conn
				#if i == 328: print("ourSlot is %i, so " % ourSlot, where_is_x[i])
			#end if
		#next i
		#print('328len', len(output[328]))
		#print('328map', [revMap[v] for v in output[328]])
		# this leaves us with at most a handful of groups that need to be merged.
		# Look for things to merge.
		merge = True
		while merge:
			#print("step")
			merge = False
			for i in range(len(self.points)):
				# Does no good to merge empties
				if len(output[i]) == 0:
					continue
				#end if
				toMerge = []
				# We are checking if each item connects to another group
				for p in output[i]:
					#j = revMap[p]
					for k in range(len(self.points)):
						# Don't try to merge with yourself.
						if i == k: continue
						if k in toMerge: continue
						if p in output[k]:
							# Incorporate their useless map.
							toMerge.append(k)
						#end if
						x = where_is_x[k]
						if i == x: continue
						if p in output[x]:
							# Incorporate their useless map.
							toMerge.append(k)
						#end if
					#next k
				#next p
				for k in toMerge:
					#print('m %i %i' % (i, k))
					output[i].update(output[k])
					for p in output[k]:
						y = revMap[p]
						#if y == 328 or y == 394:
						#	print("moving %i to %i" % (y, i), [revMap[v] for v in output[k]])
						where_is_x[y] = i
					#next p
					output[k] = set()
					merge = True
				#next k
			#next i
		#loop
		while set() in output:
			output.remove(set())
		#loop
		return output
	#end def split()
	
	def __str__(self):
		return self.drawSvg()
	#def __str__(self):
	
	def drawSvg(self):
		"""
		return a string with an SVG depicting the graph in its current state.
		"""
		# TODO: proper output encoding
		output = """<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">"""
		output += '\n<svg width="{0}" height="{1}" viewBox="0 0 {0} {1}" xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink">\n'.format(self.width, self.height)
		output += '<title>{0}</title>\n'.format(self.title)
		output += '<desc>{0}</desc>\n'.format(self.desc)
		output += '<rect x="1" y="1" width="{0}" height="{1}" fill="none" stroke="blue" />\n'.format(self.width-2, self.height-2)
		
		for i, point in enumerate(self.points):
			#tpos = point + Vector2(8, 8)
			# Draw each point
			#output += "<!--<text x='" + ('%3.3f' % tpos.x) + "' y='" + ('%3.3f' % tpos.y) + "'>" + point.name + "</text>-->\n"
			output += "<circle cx='{0:3.3f}' cy='{1:3.3f}' r='{2:3.1f}' fill='{3}' stroke='grey' stroke-width='1' />\n".format(point.x, point.y, point.size, point.color)
			# Draw each conn
			for conn in point.conns:
				# No need for duplicate paths
				if conn in self.points[:i]: continue
				#output += '<!-- ' + str(point) + ' to ' + str(conn) + '-->\n'
				output += "<path d='M {0:3.3f} {1:3.3f} L {2:3.3f} {3:3.3f}' fill='none' stroke='{4}' stroke-width='{5}' />\n".format(point.x, point.y, conn.x, conn.y, self.line_color, self.line_width)
			#next conn
		#next point
		# A layer of text above the connections.
		output += '<g>'
		for point in self.points:
			tpos = point + Vector2(8, 8)
			if point.url != '':
				output += "<a xlink:href='{0}'>".format(point.url.replace('&', '&amp;'))
			#end if
			output += "<text x='{0:3.3f}' y='{1:3.3f}' font-size='11'>{2}</text>\n".format(tpos.x, tpos.y, point.name.replace('&', '&amp;'))
			if point.url != '':
				output += "</a>\n"
			#end if
		#next point
		output += '</g>'
		output += '</svg>'
		return output
	#end def drawSvg()

	def saveJson(self):
		"""
		save JSON output
		Difficult because of the design, but it works.
		We use float instead of integer representation because the potential 
		energy depends on precise placement. If you want integer, modify this 
		function.
		"""
		# TODO: Decide if this needs to be a wider dependency.
		import json
		desc = ''
		if self.desc:
			desc = '"desc":%s, ' % json.dumps(self.desc)
		#end if
		output = '{%s"nodes":[' % desc
		conns = ''
		alreadyConn = set()
		for point in self.points:
			output += '[%s, %3.2f, %3.2f], ' % (json.dumps(point.name), point.x, point.y)
			for conn in point.conns:
				# Don't add a duplicate connection.
				# NOTE: This assumes dual connection, but that MUST be true.
				# TODO: A better way to do this is i < j
				if conn in alreadyConn: continue
				conns += '[%s, %s], ' % (json.dumps(point.name), json.dumps(conn.name))
			#next conn
			alreadyConn.add(point)
		#next point
		# Strip comma.
		output = output[:-2]
		output += '], "conns":[' + conns[:-2]
		# Add end bracket.
		output += ']}'
		return output
	#end def saveJson(self)

	def loadJson(self, jsonData):
		"""
		load JSON string
		Difficult because of the design, but it works.
		No error handling, this should be silly.
		"""
		# TODO: Decide if this needs to be a wider dependency.
		import json
		try:
			x = json.loads(jsonData)
		except ValueError as ve:
			#print("Error: Invalid JSON", ve)
			raise Exception("Invalid JSON: " + repr(ve))
		#end try
		nameObjMap = {}
		for n in x['nodes']:
			# n is in the format [name, x, y]
			nameObjMap[n[0]] = len(self.points)
			self.points.append(Point(n[0], None, n[1], n[2]))
		#next n
		for c in x['conns']:
			# c in in the format [name, name]
			objIndex1 = nameObjMap[c[0]]
			objIndex2 = nameObjMap[c[1]]
			# Dupes easily.
			if self.points[objIndex2] in self.points[objIndex1].conns: continue
			self.points[objIndex1].addConn(self.points[objIndex2])
		#next c
	#end def loadJson(self, jsonData)

	def toPolar(self, verbose=False):
		"""
		Convert cartesian coordinates to polar dr coordinates. This 
		means that for each atom, we subtract a neighboring atom's 
		position and then convert to polar coordinates. This gives 
		a repeatable method of showing relative angles and bond 
		lengths. To ensure that you have the correct drs in the correct 
		order, ensure that atom_name_hash is the same for the same 
		molecule. If the hash is different, that means you have a 
		different list of polar dr and so they cannot be compared.
		
		Returns:
		[(polar_dr), ...], atom_name_hash
		
		To get the hex digest from atom_name_hash, use atom_name_hash.hexdigest()
		To get the binary digest, use atom_name_hash.digest()
		"""
		dr = [(0, 0)]
		atom_name_hash = sha256()
		atom_name_data = ''
		# We need sorted connections to fix a strange bug related to export/import, so I choose name.
		for p in self.points:
			p.conns.sort(key=lambda x: x.name)
		#next p
		# Make sure they don't use the reverse like N3 -- CT, CT -- N3 because 
		# that produces no useful data.
		reverses = [(0, 0)]
		known = [0]
		unconns = []
		for round_n in range(1000):
			#print('round_n', round_n)
			for i, point in enumerate(self.points):
				if i in known: continue
				# This algorithm requires each molecule to order its atoms in 
				# the same way. We hash the names to ensure that the data is 
				# the same.
				atom_name = point.name
				dr_x = None
				i_x = None
				for x in point.conns:
					i_x_poss = self.points.index(x)
					if i_x_poss not in known: continue
					#print('I think %i is okay' % i_x_poss)
					i_x = i_x_poss
					if len(x.conns) > 1:
						if (i_x, i) not in reverses:
							# We found one I think...
							break
						#end if
					#end if
				#next x
				if len(point.conns) == 0:
					# Unconnected atom
					unconns.append(point)
					continue
				#end if
				if i_x == None: continue
				dr_x = point - self.points[i_x]
				dr.append(dr_x)
				#print('hi2', i)
				atom2_name = self.points[i_x].name
				atom_name_hash.update((atom_name + ('[%i]' % i) + "--" + atom2_name + ('[%i]' % i_x)).encode('utf-8'))
				atom_name_data += (atom_name + "--" + atom2_name) + '\n'
				reverses.append((i, i_x))
				known.append(i)
	        #next i, atom
			# Connect unconnect atoms in a row to the last known.
			if len(unconns) > 0 and len(known) == 0:
				known.append(self.points.index(unconns[0]))
			#end if
			for unc in unconns:
				i = self.points.index(unc)
				i_x = known[-1]
				reverses.append((i, i_x))
				known.append(i)
			#next unc
			
			# We are done when all have connections.
			if len(reverses) >= len(self.points): break
		#next round_n
		if len(dr) != len(self.points):
			print("Error: toPolar failed, expect failure elsewhere.", len(dr), len(self.points))
		#end if
		#print(atom_name_data)
		return [polar1.cartesianToPolar(dv) for dv in dr], atom_name_hash
	#end def toPolar(verbose=False)

	def getPolarConn(self):
		"""
		Same code as toPolar sadly can't fix that.
		returns a list of index pairs [(i, j), ...] and an atom_name_hash object.
		"""
		#dr = []
		atom_name_hash = sha256()
		atom_name_data = ''
		# We need sorted connections to fix a strange bug related to export/import, so I choose name.
		for p in self.points:
			p.conns.sort(key=lambda x: x.name)
		#next p
		# Make sure they don't use the reverse like N3 -- CT, CT -- N3 because 
		# that produces no useful data.
		knownsNotIncremented = 0
		reverses = [(0, 0)]
		known = [0]
		unconns = []
		for round_n in range(len(self.points) * 2):
			knownsIncremented = False
			for i, point in enumerate(self.points):
				if i in known: continue
				# This algorithm requires each molecule to order its atoms in 
				# the same way. We hash the names to ensure that the data is 
				# the same.
				atom_name = point.name
				dr_x = None
				i_x = None
				for x in point.conns:
					# No need for dr_x, just set to true.
					dr_x = True #point - x
					i_x_poss = self.points.index(x)
					if i_x_poss not in known: continue
					i_x = i_x_poss
					if len(x.conns) > 1:
						if (i_x, i) not in reverses:
							# We found one I think...
							break
						#end if
					#end if
				#next x
				if dr_x is None:
					# Unconnected atom
					unconns.append(point)
					continue
				#end if
				if i_x == None: continue
				#dr.append(dr_x)
				atom2_name = self.points[i_x].name
				atom_name_hash.update((atom_name + ('[%i]' % i) + "--" + atom2_name + ('[%i]' % i_x)).encode('utf-8'))
				atom_name_data += (atom_name + "--" + atom2_name) + '\n'
				#reverses.append((point, x))
				reverses.append((i, i_x))
				known.append(i)
				knownsIncremented = True
			#next i, atom
			
			# Connect unconnect atoms in a row to the last known.
			if len(unconns) > 0 and len(known) == 0:
				known.append(self.points.index(unconns[0]))
			#end if
			for unc in unconns:
				i = self.points.index(unc)
				i_x = known[-1]
				reverses.append((i, i_x))
				known.append(i)
			#next unc
			
			# We are done when all have connections.
			if len(reverses) >= len(self.points): break
			
			# We are in trouble if knowns didn't increase. That means two separate structures.
			if not knownsIncremented:
				#print('not knownsIncremented on round', round_n)
				knownsNotIncremented += 1
				if knownsNotIncremented >= 2:
					#print('knownsNotIncremented >= 2 on round', round_n)
					for i in range(len((self.points))):
						if i not in known:
							# Connect it to the last known.
							reverses.append((known[-1], i))
							known.append(i)
							# Reset the counter.
							knownsNotIncremented = 0
							break
						#end if
					#next i
					#break
				#end if
			else:
				knownsNotIncremented = 0
			#end if
		#next round_n
		#print(round_n+1, "rounds to do getPolarConn")
		if len(reverses) != len(self.points):
			print("Error: getPolarConn failed, expect failure elsewhere.")
			print(reverses)
			print(atom_name_data)
		#end if
		#print(atom_name_data)
		return reverses, atom_name_hash
	#end def getPolarConn()
	
	def setCartesian(self, dr):
		"""
		Unlike the name suggests, we are not setting the atom's 
		positions to a list of cartesian coordinates.
		dr is a list of relative polar coordinates.
		"""
		if len(dr) != len(self.points):
			print("Not right number of dr.", len(dr), len(self.points))
			return False
		#end if
		
		# The format of drs is [(atom_0_index, atom_i_index), ...]
		# For example methane is [(0, 1), (1, 0), (2, 0), (3, 0), (4, 0)]
		# That is to say carbon is relative to hydrogen1.
		# hydrogen1 is relative to carbon (circular I know, necessary)
		# hydrogen2 is relative to carbon.
		# ...
		drs, atom_hash = self.getPolarConn()
		#print(atom_hash.hexdigest())
		
		# The first one is always our starting point.
		# We could set it to zero, but let's leave it where it is.
		# We know the position of drs[0][0].
		knowns = [drs[0][0]]
		#print(self.points[drs[0][0]].name, 'assumed')
		#self.atoms[drs[0][0]].pos = self.atoms[drs[0][0]].pos
		j = 0
		while len(knowns) < len(self.points):
			# i starts at 0 and goes to N like it should.
			for i, spc in enumerate(drs):
				if spc[0] in knowns:
					if spc[1] in knowns:
						# We know both, so skip this dr...
						continue
					#end if
					#print(self.points[spc[1]].name, 'relative to', self.points[spc[0]].name, dr[i])
					knowns.append(spc[1])
					self.points[spc[1]].setPos(self.points[spc[0]] + \
						Vector2(*polar1.polarToCartesian(dr[i])))
				elif spc[1] in knowns:
					# spc[0] not in knowns
					#print(self.points[spc[0]].name, 'relative to', self.points[spc[1]].name, dr[i])
					knowns.append(spc[0])
					self.points[spc[0]].setPos(self.points[spc[1]] + \
						Vector2(*polar1.polarToCartesian(dr[i])))
				#end if
			#next i, spc
			j += 1
			if j > 1000:
				# FIXME: when there are disconnected nodes, this should work just like everything else.
				print("rounds has passed 1000, we give up.", len(knowns), len(self.points), knowns)
				print(drs)
				break
			#end if
		#loop
		return True
	#end def setCartesian(dr)
	
	def setPos(self, v):
		"""
		Take an x0 properly reshaped and load into points.
		Example:
		m = np.matrixlib.matrix(x0)
		m = m.reshape(len(x0)//2, 2)
		map1.setPos([np.array(xa)[0] for xa in m])
		"""
		for i, xa in enumerate(v):
			self.points[i].x = xa[0]
			self.points[i].y = xa[1]
		#next i, xa
	#end def setPos(v)
	
	def getX0Conns(self, i_lt_j=False):
		"""
		Returns (X0, conns)
		x0: the 1d array of point [x, y, x, y ...] and the 
		conns: the 2d array of connections [[1], [0, 2], ...]
		x0 is a numpy array, conns is a Python array.
		This is used in sww_optimize1, sortLoop and other things.
		"""
		# TODO: do this without numpy
		if np == None:
			print("Error: numpy is missing when getX0Conns is called.")
			raise Exception("missing library Numpy")
		#end if
		# Get the xy values into a 2D array.
		x0 = np.array([np.array((p.x, p.y)) for p in self.points])
		# Turn it into a 1D array for the optimizer.
		x0 = x0.reshape(1, 2 * len(self.points))[0]
		conns = []
		for i, p in enumerate(self.points):
			pConns = []
			for conn in p.conns:
				pConns.append(self.points.index(conn))
			#next conn
			if i_lt_j: pConns = list(filter(lambda j: i<j, pConns))
			conns.append(pConns)
		#next p
		return x0, conns
	#end def getX0Conns(i_lt_j=False)

	def sortOrder(self, sortFunc = None, n = 100):
		"""
		Also known as experiment 2, also known as pretty, this algorithm attempts a set of random orders, using a sort function it picks the lowest potential. This is slow in Python, but very fast in JavaScript and C++. Thus, it should be ported to C++.
		"""
		if sortFunc == None:
			sortFunc = self.sortGrid
		#end if
		from sww_optimize1 import LJ_Potential, V_SmallWideWorld, V_Harmonic, V_Harmonic_Angle, ConnList
		lj_conf = LJ_Potential()
		b0 = 40
		gtol = 1e-2
		#trueRand = SystemRandom()
		#rn = trueRand.randint(0, 0xffffffff)
		funcName = sortFunc.__name__.replace('sort','')
		
		# Predict potential to stop at.
		A = 1.0
		B = 2.0
		C = 5
		D = 1-C
		E = 0
		nodes = len(self.points)
		num_conns = sum([len(p.conns) for p in self.points])
		#predicted_V = (A*nodes*nodes) + (B*conns*conns) + (C * nodes) + (D * conns) + E
		#predicted_V = 3
		predicted_V = None
		
		start_t = time.time()
		V_all = []
		V_min = 1e36
		x_min = None
		points_min = self.points[:]
		for i in range(n):
			# Use a different seed to get different maps. Deterministic.
			seed = randint(0, 0xffffffff)
			# If we don't do createMap4, the seed will be different, expensive but not as expensive as sorting/optimizing by a long shot.
			# FIXME: rare overwrites
			#base_filename = 'grid1_%i_%i.json' % (rn, i)
			shuffle(self.points)
			# The shuffle will cause these to go bad, so we have to recompute them
			x0, conns = self.getX0Conns(True)
			conns_cpp = ConnList(conns)
			nonConns = ConnList(getNonConns(conns, True))
			#print(x0)
			#if verbose:
			#	print("atom conns:", conns)
			#end if

			# Not necessary to get spherical coordinates of the original coordinates.
			#output = [spherical2.cartesianToSpherical(v) for v in molecule.x0]
			#print("Spherical coordinates of atoms:")
			#print(output)
			
			# This may be used eventually
			#sphericalCoords, atom_name_hash = molecule.toSpherical(verbose)
			sortFunc(b0)
			x_out = self.getX0Conns()[0]
			V_configuration = V_SmallWideWorld(x_out, conns_cpp, b0, lj_conf, nonConns)
			#print(funcName, "Potential:", V_configuration)
			V_all.append(V_configuration)
			if V_configuration < V_min:
				V_min = V_configuration
				x_min = x_out
				points_min = self.points[:]
				if predicted_V == None:
					# TODO: Machine learning.
					#predicted_V = V_min / 100
					a,b,c,d,e,f,g = (-2.17996299e+02,   2.28854783e+02,  -7.53170727e-10, 1.06690869e+04,  -1.32507059e+04,   2.70388458e-02, 6.11521299e+04)
					predicted_V = a*(nodes**2) + b*(num_conns**2) + c*(V_min**2) + d*nodes + e*num_conns + f*V_min + g
				#end if
				if V_min < predicted_V: break
			#end if
		#next i
		sort_dt = (time.time() - start_t)
		results = ("%s dt: %3.3f seconds, %i iterations, predicted V: %3.3f\n" % (funcName, sort_dt, i, predicted_V))
		results += ("%s Potential: first: %3.3f min: %3.3f avg: %3.3f max: %3.3f" % (funcName, V_all[0], V_min, sum(V_all)/len(V_all), max(V_all)))
		self.desc = self.desc.replace('[results]', 'sortOrder [' + results + ']')
		if x_min is not None:
			m = np.matrixlib.matrix(x_min)
			m = m.reshape(len(self.points), 2)
			# FIXME: This makes my head spin, it can't actually work.
			self.points = points_min
			self.setPos([np.array(xa)[0] for xa in m])
			self.centerBound()
		#end if
		return V_all
	#end def sortOrder(sortFunc = None, n = 100)
	
	def sortConstraint(self, b0=40):
		"""
		Constraint solver for SWW
		Designed against hexmulti1.json [2, 2, 3, 3, 3, 3, 4]
		{"nodes":[["g",359.83,300.59], ["e",380.3,335.03], ["b",379.56,265.77], ["a",440.17,299.46], ["f",420.32,334.32], ["c",419.67,264.97], ["d",400.29,299.83]], "conns":[["g","b"], ["g","e"], ["e","f"], ["b","c"], ["b","d"], ["a","c"], ["a","d"], ["a","f"], ["f","d"], ["c","d"]], "showText":true}
		See constraint_graph2.txt
		Unfinished, but it does have a pretty cool method of validating the correctness of split()
		from mapmake1 import Map
		map1 = Map()
		map1.loadJson(open('media_ownership12.json','r').read())
		map1.sortConstraint()
		indep = map1.split()
		maps = []
		for ps in indep:
			map2 = Map()
			map2.addPoints(ps)      
			map2.sortConstraint()
			maps.append(map2)
		#next ps
		Success!
		NOTE: This algorithm is no longer a constraint solver.
		"""
		nodes = len(self.points)
		if nodes < 2:
			# Guaranteed to be sorted.
			return
		#end if
		# First two are gimmes
		first = self.points[0]
		first.x = 0
		first.y = 0
		first_i = 0
		if len(first.conns) == 0:
			for p in self.points:
				if len(p.conns) > 0:
					first = p
					first_i = self.points.index(p)
					break
				#end if
			#next p
			if len(first.conns) == 0:
				# Unconnected graph, there's a good enough solution using sortLattice.
				return self.sortLattice(b0)
			#end if
		#end if
		second = first.conns[0]
		second.x = b0
		second.y = 0
		if nodes < 3:
			# Guaranteed to be sorted.
			return
		#end if
		from sww_optimize1 import LJ_Potential, V_SmallWideWorld, ConnList
		lj_conf = LJ_Potential()
		x0, conns = self.getX0Conns(True)
		conns_cpp = ConnList(conns)
		nonConnsList = getNonConns(conns, True)
		nonConns = ConnList(nonConnsList)
		print(first.name, second.name)
		Maybe = 2
		mapPointToIndex = self.pointToIndex()
		second_i = mapPointToIndex[first.conns[0]]
		nullVector = Vector2()
		options = [None for i in range(nodes)]
		options[first_i] = ConstraintDomain(first_i, [nullVector + first], 1) # Easier to add than convert.
		options[second_i] = ConstraintDomain(second_i, [nullVector + second], 1)
		twoCandidates = [Vector2(b0*0.5, -b0*35.641/40), Vector2(b0*0.5, b0*35.641/40)] # Above or below two nodes
		# Generated by a 8-star graph and subtraction.
		sevenCandidates = [Vector2(b0*0.7071, b0*0.7071), Vector2(0, b0), Vector2(-b0*0.7071, b0*0.7071), Vector2(-b0, 0), Vector2(-b0*0.7071, -b0*0.7071), Vector2(0, -b0), Vector2(b0*0.7071, -b0*0.7071)]
		# The same but reversed, rule out overlapping first
		sevenCandidates2 = [Vector2(b0*0.7071, b0*0.7071), Vector2(0, b0), Vector2(-b0*0.7071, b0*0.7071), Vector2(b0, 0), Vector2(-b0*0.7071, -b0*0.7071), Vector2(0, -b0), Vector2(b0*0.7071, -b0*0.7071)]
		eightCandidates = [Vector2(b0, 0), Vector2(b0*0.7071, b0*0.7071), Vector2(0, b0), Vector2(-b0*0.7071, b0*0.7071), Vector2(-b0, 0), Vector2(-b0*0.7071, -b0*0.7071), Vector2(0, -b0), Vector2(b0*0.7071, -b0*0.7071)]
		# Anyone connect to first or second can be given their options.
		for conn in first.conns:
			if conn == second: continue
			# If it's also connected to the second one, bad luck only two options.
			if second in conn.conns:
				candidates = twoCandidates
			else:
				candidates = sevenCandidates
			#end if
			options[mapPointToIndex[conn]] = ConstraintDomain(first_i, candidates, len(candidates))
		#next conn
		for conn in second.conns:
			i = mapPointToIndex[conn]
			if options[i] != None: continue
			# If it's also connected to the first one, we already dealt with it.
			candidates = sevenCandidates2
			options[mapPointToIndex[conn]] = ConstraintDomain(second_i, candidates, len(candidates))
		#next conn
		
		# Give each node a set of options.
		for roundTry in range(nodes):
			updating = False
			for i, p in enumerate(self.points):
				#dist, rev = self.getDijkstra(p, avoid)
				# Reducing their options might be worthwhile now, but hold on.
				# We definitely need the very least options
				if options[i]: continue
				least_options = None
				least_j = None
				for conn in p.conns:
					j = mapPointToIndex[conn]
					if options[j] != None:
						options_j_len = options[j].length
						#if options_j_len > 3584:
						#	print("No can do, too large")
						#	continue
						#end if
						if least_options == None or options_j_len < least_options:
							least_options = options_j_len
							least_j = j
						#end if
					#end if
				#next conn
				if least_options != None:
					# We can pick around any of their options
					options[i] = ConstraintDomain(least_j, eightCandidates, 8) # least_options * 8
					updating = True
				#end if
			#next i, p
			if not updating: break
		#next roundTry
		if None in options:
			print("One or more options was not set, that means something went wrong.", options) #[len(opt) for opt in options])
			return False
		#end if
		# TODO: The ones with the fewest options should go first, then the rest.
		knowns = [i for i, opt in enumerate(options) if opt.length == 1]
		# Much faster than sqrt in length
		b0_sq = b0 * b0
		b0_sq_margin = b0_sq * 0.1
		#print("Starting off with {0} knowns".format([self.points[x].name for x in knowns]))
		#print("Options:", [[str(x) for x in opt] for opt in options])
		#print([opt.length for opt in options])
		setOrder = knowns[:]
		# FIXME: Don't let this while loop go forever. Should be okay with above, unless you change it.
		k = 0
		while len(setOrder) < len(options):
			for i, opt in enumerate(options):
				if i in setOrder: continue
				if opt.i == i: continue
				if opt.i in setOrder:
					# We can do this because we know what it depends on.
					setOrder.append(i)
				#end if
			#next opt
			k += 1
		#loop
		print("Took {0} loops".format(k))
		#print(setOrder)
		# Don't need to set knowns.
		setOrder = setOrder[len(knowns):]
		min_V = V_SmallWideWorld(x0, conns_cpp, b0, lj_conf, nonConns)
		print("init_V:", min_V)
		min_test = None
		start_t = time.time()
		skip = 0
		base = 0
		first_non_conn = 1
		while len(nonConnsList[base]) == 0 and base < len(self.points):
			base += 1
		#loop
		if base >= len(self.points):
			print("Fully connected, solvable with fully connected algorithm, not this one")
			return
		#end if
		# Temporary
		#simpleOptimization = False
		simpleOptimization = True
		if base == (len(self.points) - 1):
			simpleOptimization = False
		else:
			first_non_conn = nonConnsList[base][0]
			skipAmount = 1
			# TODO: Find the right skip amount and make it happen!
			for opt in (options[::-1][:-first_non_conn]):
				skipAmount *= opt.length
			#next opt
			print('skipAmount', skipAmount, first_non_conn, [opt.length for opt in options])
		#end if
		#print('fu', [len(list(opt.getList(options))) for opt in options], len(list(getConst([list(opt.getList(options)) for opt in options]))))
		for test in getConst([list(opt.getList(options)) for opt in options]):
			if skip > 0:
				skip -= 1
				continue
			#end if
			#print([str(x) for x in test])
			for x in setOrder:
				if options[x].i == x:
					self.points[x].setPos(test[x])
				else:
					self.points[x].setPos(self.points[options[x].i] + test[x])
				#end if
			#next x
			if simpleOptimization:
				lensq_test = (self.points[base] - self.points[first_non_conn]).lensq()
				if lensq_test < b0_sq_margin:
					skip = skipAmount
					print("skipping from {0}".format([str(x) for x in test]))
				#end if
			#end if
			#self.setPos([(v.x, v.y) for v in test])
			x_out = self.getX0Conns()[0]
			V_test = V_SmallWideWorld(x_out, conns_cpp, b0, lj_conf, nonConns)
			if V_test < min_V:
				min_V = V_test
				min_test = test
			#end if
			#if V_test < 0:
			#	print("Found negative potential", V_test)
			#	break
			#end if
			if time.time() - start_t > 10:
				break
			#end if
		#next test
		if min_test:
			for x in setOrder:
				if options[x].i == x:
					self.points[x].setPos(test[x])
				else:
					self.points[x].setPos(self.points[options[x].i] + test[x])
				#end if
			#next x
		#end if
		print("min_V:", min_V)
		return True
	#end def sortConstraint(b0=40)
	
	def sortNearVirtual(self, width=40, useCache=False, randomNeighbors=False, verbose=False):
		"""
		Incredible new algorithm works well with L-BFGS-B because they complement each other.
		Dec 5, 2016
		12:36 < Javantea> For each node in the graph:
		12:36 < Javantea>     Find 2 random or non-random neighbors.
		12:38 < Javantea>     If the node has only 1 or 0 neighbors, make a virtual position based on the unit vector between them and their neighbor multiplied by 40
		12:40 < Javantea>    Otherwise, decide based on the current position and distance of the two neighbors whether there are 1, 2, or 8 valid positions for the node
		12:40 < Javantea>     Find the lowest potential among those positions and place the node there.
		12:41 < Javantea> At the end of the algorithm all virtual positions should be computed based on the current position of the position the virtual position is based on
		"""
		from sww_optimize1 import LJ_Potential, V_SmallWideWorld, V_Harmonic, V_Harmonic_Angle, ConnList
		SMALL_SQ = SMALL * SMALL
		lj_conf = LJ_Potential()
		x0, conns = self.getX0Conns(True)
		conns_cpp = ConnList(conns)
		nonConns = getNonConns(conns, True)
		nonConns_cpp = ConnList(nonConns)
		if useCache:
			# FIXME: i_lt_j probably makes this not work.
			all_conns = conns #self.getX0Conns(False)[1]
			all_nonConns = nonConns #getNonConns(conns, False)
		#end if
		V_init = V_SmallWideWorld(x0, conns_cpp, width, lj_conf, nonConns_cpp)
		if V_init > 1e40:
			print("Initial potential too high, sorting with lattice first. V =", V_init)
			self.sortLattice()
			x0 = self.getX0Conns()[0]
			V_init = V_SmallWideWorld(x0, conns_cpp, width, lj_conf, nonConns_cpp)
			print("V =", V_init)
			if V_init > 1e40:
				print("This graph probably won't work, but let's find out anyway.")
			#end if
		#end if
		minV = V_init
		x_out = x0[:]
		widthsq = width * width
		virtuals = []
		knowns = set([self.points[0]])
		for roundTry in range(len(self.points)):
			for i, node in enumerate(self.points):
				if node in knowns: continue
				# node.x == x_out[2*i], node.y == x_out[2*i+1]
				#print(node.x, x_out[2*i], node.y, x_out[2*i+1])
				if useCache:
					V_cache = PotentialCache(0, i)
					# TODO: C++ version!
					V_variant = V_SmallWideWorld_Cache(x_out, all_conns, width, lj_conf, all_nonConns, V_cache)
					V_cache.PotentialA = minV - V_variant
					#V_test = V_SmallWideWorld_Cache(x_out, all_conns, width, lj_conf, nonConns, V_cache)
					#V_test2 = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns_cpp)
					#print('test', V_test, minV, V_test2)
				#end if
				backup = node + Vector2()
				if len(node.conns) < 2:
					# Leafs get virtual positions based on their neighbors
					if len(node.conns) == 1:
						dr = (node.conns[0] - node)
						# TODO: Deal with small dr better
						if dr.lensq() > SMALL_SQ:
							dr *= width / dr.length()
						#end if
						virtuals.append((node, node.conns[0], dr))
					else:
						# TODO: Place the loner somewhere 40 pixels from any other node.
						pass
					#end if
					continue
				#end if
				if randomNeighbors:
					na = randint(0, len(node.conns)-1)
					nb = randint(0, len(node.conns)-2)
					if nb >= na: nb += 1
					neighbors = [node.conns[na], node.conns[nb]]
				else:
					neighbors = node.conns[:2]
				#end if
				# len(neighbors) == 2, so we can assume
				neighbor_a, neighbor_b = neighbors
				dr = neighbor_a - neighbor_b
				dr_lensq = dr.lensq()
				if dr_lensq >= (widthsq * 4):
					# There's only one place for node, yay. Directly in between.
					node_pos = (neighbor_a + neighbor_b) * 0.5
					node.setPos(node_pos)
					x_out[2 * i] = node.x
					x_out[2 * i + 1] = node.y
					if useCache:
						V_node_i = V_SmallWideWorld_Cache(x_out, all_conns, width, lj_conf, all_nonConns, V_cache)
						#print(V_node_i, '=', V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns_cpp))
					else:
						V_node_i = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns_cpp)
					#end if
					if V_node_i < minV:
						minV = V_node_i
						if verbose: print("New min", minV)
					else:
						#print("Worse", V_node_i)
						node.setPos(backup)
						x_out[2 * i] = node.x
						x_out[2 * i + 1] = node.y
					#end if
					knowns.add(node)
				elif dr_lensq < (widthsq * 0.25):
					# TODO: They are too close together, which is bad. Try 8 positions around them.
					# This is done in constraint.
					#middle = neighbor_b + (dr * 0.5)
					middle = (neighbor_a + neighbor_b) * 0.5
					if dr.x*dr.x > SMALL_SQ: #assume perp.y = dr.y.
						#dr.x*perp.x + dr.y*perp.y = 0
						#dr.x*perp.x + dr.y*dr.y = 0
						perp = Vector2(-dr.y**2/dr.x, dr.y)
					else:
						#dr.x = 0
						perp = Vector2(dr.y, 0)
					#end if
					# TODO: Deal with small perp better
					if perp.lensq() > SMALL_SQ:
						perp *= width / perp.length()
					else:
						# This is not a solution, it's a workaround
						perp = Vector2(width, 0)
					#end if
					#print(neighbor_a, '', neighbor_b, ' dr', dr, ' middle', middle, ' perp', perp)
					node.setPos(middle + perp)
					x_out[2 * i] = node.x
					x_out[2 * i + 1] = node.y
					if useCache:
						V_node_i = V_SmallWideWorld_Cache(x_out, all_conns, width, lj_conf, all_nonConns, V_cache)
						#print(V_node_i, '=', V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns_cpp))
					else:
						V_node_i = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns_cpp)
					#end if
					#print(minV - V_node_i)
					node.setPos(middle - perp)
					x_out[2 * i] = node.x
					x_out[2 * i + 1] = node.y
					if useCache:
						V_node_j = V_SmallWideWorld_Cache(x_out, all_conns, width, lj_conf, all_nonConns, V_cache)
						#print(V_node_j, '=', V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns_cpp))
					else:
						V_node_j = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns_cpp)
					#end if
					#print(minV - V_node_j)
					if V_node_i < V_node_j:
						node.setPos(middle + perp)
						x_out[2 * i] = node.x
						x_out[2 * i + 1] = node.y
						if V_node_i < minV:
							minV = V_node_i
							if verbose: print("New min", minV)
						else:
							#print("Worse", V_node_i)
							node.setPos(backup)
							x_out[2 * i] = node.x
							x_out[2 * i + 1] = node.y
						#end if
					else:
						if V_node_j < minV:
							minV = V_node_j
							if verbose: print("New min", minV)
						else:
							#print("Worse", V_node_j)
							node.setPos(backup)
							x_out[2 * i] = node.x
							x_out[2 * i + 1] = node.y
						#end if
					#end if
					knowns.add(node)
				else:
					# TODO: They are between 0.5*w and 2*w, which means there are 2 good positions.
					# This is done in constraint.
					# h^2 = x^2 + y^2
					# widthsq = middle.x-...
					#middle = neighbor_b + (dr * 0.5)
					middle = (neighbor_a + neighbor_b) * 0.5
					if dr.x*dr.x > SMALL*SMALL: #assume perp.y = dr.y.
						#dr.x*perp.x + dr.y*perp.y = 0
						#dr.x*perp.x + dr.y*dr.y = 0
						perp = Vector2(-dr.y*dr.y/dr.x, dr.y)
					else:
						#dr.x = 0
						perp = Vector2(dr.y, 0)
					#end if
					# TODO: Deal with small perp better
					if perp.lensq() > SMALL_SQ:
						perp *= width / perp.length()
					else:
						# This is not a solution, it's a workaround
						perp = Vector2(width, 0)
					#end if
					#print(neighbor_a, '', neighbor_b, ' dr', dr, ' middle', middle, ' perp', perp)
					node.setPos(middle + perp)
					x_out[2 * i] = node.x
					x_out[2 * i + 1] = node.y
					if useCache:
						V_node_i = V_SmallWideWorld_Cache(x_out, all_conns, width, lj_conf, all_nonConns, V_cache)
						#print(V_node_i, '=', V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns_cpp))
					else:
						V_node_i = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns_cpp)
					#end if
					#print(minV - V_node_i)
					node.setPos(middle - perp)
					x_out[2 * i] = node.x
					x_out[2 * i + 1] = node.y
					if useCache:
						V_node_j = V_SmallWideWorld_Cache(x_out, all_conns, width, lj_conf, all_nonConns, V_cache)
						#print(V_node_j, '=', V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns_cpp))
					else:
						V_node_j = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns_cpp)
					#end if
					#print(minV - V_node_j)
					if V_node_i < V_node_j:
						node.setPos(middle + perp)
						x_out[2 * i] = node.x
						x_out[2 * i + 1] = node.y
						if V_node_i < minV:
							minV = V_node_i
							if verbose: print("New min", minV)
						else:
							#print("Worse", V_node_i)
							node.setPos(backup)
							x_out[2 * i] = node.x
							x_out[2 * i + 1] = node.y
						#end if
					else:
						if V_node_j < minV:
							minV = V_node_j
							if verbose: print("New min", minV)
						else:
							#print("Worse", V_node_j)
							node.setPos(backup)
							x_out[2 * i] = node.x
							x_out[2 * i + 1] = node.y
						#end if
					#end if
					knowns.add(node)
				#end if
			#next node
			if len(knowns) + len(virtuals) == len(self.points): break
		#next roundTry
		if verbose: print(roundTry + 1, "rounds")
		if verbose: print("Virtuals:", [v[0].name for v in virtuals])
		# Resolve all virtual positions.
		for virtual, neighbor, pos in virtuals:
			# TODO: We could try 8 positions or the whole circle around the neighbor.
			backup = virtual + Vector2()
			virtual.setPos(neighbor + pos)
			i = self.points.index(virtual)
			if useCache:
				V_cache = PotentialCache(0, i)
				V_node_i = V_SmallWideWorld_Cache(x_out, all_conns, width, lj_conf, all_nonConns, V_cache)
				V_cache.PotentialA = minV - V_node_i
			#end if
			x_out[2 * i] = virtual.x
			x_out[2 * i + 1] = virtual.y
			if useCache:
				V_node_j = V_SmallWideWorld_Cache(x_out, all_conns, width, lj_conf, all_nonConns, V_cache)
			else:
				V_node_j = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns_cpp)
			#end if
			if V_node_j < minV:
				minV = V_node_j
				if verbose: print("New min", minV)
			else:
				virtual.setPos(backup)
				x_out[2 * i] = virtual.x
				x_out[2 * i + 1] = virtual.y
			#end if
		#next virtual
		#for i, node in enumerate(self.points):
		#	print(node.x, x_out[2*i], node.y, x_out[2*i+1])
		#end if
		V_out = V_SmallWideWorld(x_out, conns_cpp, width, lj_conf, nonConns_cpp)
		if verbose: print("Potential:", minV, V_out)
		return V_out
	#end def sortNearVirtual(self, width=40)

	def sortBranchMod(self, r0=40, knownPos=None, useCache=False, verbose=False):
		"""
		A brilliant sorting method that works well with branches but not loops.
		r0 is the length of the bonds set by the algorithm.
		knownPos is a list of booleans that tells us whether point i is given or should be computed.
		roundTry is required for loops. This can be optimized greatly.
		FIXME: Starfish where node 5 is the central node.
		Fixable by picking knownPos based on number of connections.
		TODO: Find other bugs.
		"""
		nodes = len(self.points)
		if nodes < 1:
			# Congrats, you're guaranteed to be sorted.
			return
		#end if
		from sww_optimize1 import LJ_Potential, V_SmallWideWorld, V_Harmonic, V_Harmonic_Angle, ConnList
		SMALL_SQ = SMALL * SMALL
		lj_conf = LJ_Potential()
		x0, conns = self.getX0Conns(True)
		conns_cpp = ConnList(conns)
		nonConns = getNonConns(conns, True)
		nonConns_cpp = ConnList(nonConns)
		if useCache:
			# FIXME: i_lt_j probably makes this not work.
			all_conns = conns #self.getX0Conns(False)[1]
			all_nonConns = nonConns #getNonConns(conns, False)
		#end if
		V_init = V_SmallWideWorld(x0, conns_cpp, r0, lj_conf, nonConns_cpp)
		if V_init > 1e40:
			print("Initial potential too high, sorting with lattice first. V =", V_init)
			self.sortLattice()
			x0 = self.getX0Conns()[0]
			V_init = V_SmallWideWorld(x0, conns_cpp, r0, lj_conf, nonConns_cpp)
			print("V =", V_init)
			if V_init > 1e40:
				print("This graph probably won't work, but let's find out anyway.")
			#end if
		#end if
		minV = V_init
		x_out = x0[:]
		widthsq = r0 * r0
		virtuals = []
		knowns = set([self.points[0]])

		# This is our algorithm... Written on the whiteboard last night. Understood many years ago but unable to write the code. Until now!
		if knownPos == None:
			knownPos = [False] * nodes
			knownPos[0] = True
			# We don't need to do expensive checks if we have no knowns. *shrug*
			checkEverything = False
			# Translate everything the same amount.
			dr = Vector2(self.width / 2, self.height / 2) - self.points[0]
			for p in self.points:
				p += dr
			#next p
		#end if
		# v1 in spherical coordinates.
		#v1 = (r1, theta1) == (r1*cos(theta1), r1*sin(theta1))
		v1 = (r0, 0)
		# -v1 in spherical coordinates
		#neg_v1 = (r0, v1[1] + pi)
		fillReady = False
		mapPointToIndex = self.pointToIndex()
		
		for roundTry in range(nodes):
			#print("fillReady?", fillReady)
			knownDone = True
			for i in range(nodes):
				if (not fillReady) and (not knownPos[i]): continue
				#print(self.points[i].name, [c.name for c in self.points[i].conns])
				givens = []
				unknowns = []
				# Set the position of its connections.
				for conn in self.points[i].conns:
					j = mapPointToIndex[conn]
					if knownPos[j]:
						givens.append(j)
						continue
					#end if
					unknowns.append(j)
				#next conn
				if knownPos[i]:
					# First solve the easy cases, then work your way up.
					if len(unknowns) == 0:
						# Everything is known, we're good.
						#print('Yay', self.points[i].x, self.points[i].y)
						continue
					#end if
					if len(givens) == 0:
						# All unknowns, so use the simplex method.
						n_conns = len(unknowns)
						theta0 = tau / n_conns # tau = 2*pi
						x = 0
						dr = self.points[unknowns[0]] - self.points[i]
						theta_init = atan2(dr.y, dr.x)
						#print('dr', dr, 'theta_init', theta_init)
						backups = [Vector2(self.points[v].x, self.points[v].y) for v in unknowns]
						for j in unknowns:
							# Spherical coordinates
							theta_j = theta_init + (theta0 * (x+1))
							#v_j = (r0, theta_j)
							self.points[j].x, self.points[j].y = (self.points[i].x + (r0*cos(theta_j)), self.points[i].y + (r0*sin(theta_j)))
							x_out[2*j] = self.points[j].x
							x_out[2*j+1] = self.points[j].y
							knownPos[j] = True
							knownDone = False
							print(self.points[j].name, 'added to', self.points[i].name)
							#print('Simple', x, j, self.points[j].x, self.points[j].y, theta_j)
							x += 1
						#next j
						# only set the values if we improve V
						if useCache:
							V_node_i = V_SmallWideWorld_Cache(x_out, all_conns, r0, lj_conf, all_nonConns, V_cache)
							#print(V_node_i, '=', V_SmallWideWorld(x_out, conns_cpp, r0, lj_conf, nonConns_cpp))
						else:
							V_node_i = V_SmallWideWorld(x_out, conns_cpp, r0, lj_conf, nonConns_cpp)
						#end if
						if V_node_i <= (minV + 4):
							minV = V_node_i
							if verbose: print("New min", minV)
						else:
							print("Worse", V_node_i)
							for bui, j in enumerate(unknowns):
								self.points[j].setPos(backups[bui])
								x_out[2 * i] = backups[bui].x
								x_out[2 * i + 1] = backups[bui].y
							#next j
							minV = V_node_i
						#end if
						continue
					#end if
					if len(givens) == 1:
						# Very easy, create a v1 and do the same as above
						v1i_cartesian = self.points[i] - self.points[givens[0]]
						v1i_theta = atan2(v1i_cartesian.y, v1i_cartesian.x)
						#v1i_spherical = (v1i_cartesian.length(), v1i_theta)
						#neg_v1i_spherical = (v1i_cartesian.length(), v1i_theta+pi)
						n_conns = len(unknowns) + 1
						theta0 = tau / n_conns # tau = 2*pi
						backups = [Vector2(self.points[v].x, self.points[v].y) for v in unknowns]
						x = 0
						for j in unknowns:
							# Spherical coordinates
							if n_conns == 2:
								theta_j = v1i_theta
							else:
								theta_j = v1i_theta+pi + (theta0 * (x+1))
							#end if
							#v_j = (r0, theta_j)
							self.points[j].x, self.points[j].y = (self.points[i].x + (r0*cos(theta_j)), self.points[i].y + (r0*sin(theta_j)))
							x_out[2*j] = self.points[j].x
							x_out[2*j+1] = self.points[j].y
							knownPos[j] = True
							knownDone = False
							print(self.points[j].name, 'added to', self.points[i].name, 'based on', self.points[givens[0]].name)
							#print('Simple1', x, j, self.points[j].x, self.points[j].y, theta_j, 'v1it', v1i_theta)
							x += 1
						#next j
						# only set the values if we improve V
						mapCurr = Map()
						mapCurr.addPoints([self.points[k] for k in range(len(knownPos)) if knownPos[k]])
						#print(mapCurr.saveJson())
						if useCache:
							V_node_i = V_SmallWideWorld_Cache(x_out, all_conns, r0, lj_conf, all_nonConns, V_cache)
							#print(V_node_i, '=', V_SmallWideWorld(x_out, conns_cpp, r0, lj_conf, nonConns_cpp))
						else:
							knownsI = [k for k in range(len(knownPos)) if knownPos[k]]
							conns_mod = []
							for k in range(len(conns)):
								if knownPos[k] == False:
									conns_mod.append([])
									continue
								#end if
								conns_mod.append([m for m in conns[k] if m in knownsI])
							#next k
							#print('cm', conns_mod)
							conns_cpp_mod = ConnList(conns_mod)
							nonConns_mod = []
							for k in range(len(nonConns)):
								if knownPos[k] == False:
									nonConns_mod.append([])
									continue
								#end if
								nonConns_mod.append([m for m in nonConns[k] if m in knownsI])
							#next k
							#print('ncm', nonConns_mod)
							nonConns_cpp_mod = ConnList(nonConns_mod)
							V_node_i = V_SmallWideWorld(x_out, conns_cpp_mod, r0, lj_conf, nonConns_cpp_mod)
						#end if
						if V_node_i <= (minV + 4):
							minV = V_node_i
							if verbose: print("New min", minV)
						else:
							print("Worse", V_node_i)
							for bui, j in enumerate(unknowns):
								self.points[j].setPos(backups[bui])
								x_out[2 * i] = backups[bui].x
								x_out[2 * i + 1] = backups[bui].y
							#next j
							minV = V_node_i
						#end if
					#end if
					#print("Not sure what to do for: given: %i, unknown: %i" % (len(givens), len(unknowns)))
					# Take the list of givens and create a perfect placement for our node
				else:
					# Don't use v1 until all known nodes are figured out.
					# Fixes sortBranch_fail1.json
					if not fillReady: continue
					#print("Not known pos", i, knownPos[i])
					if len(givens) == 0:
						# We don't know any of our neighbors yet, nope.
						continue
					#end if
					if len(givens) == 1:
						# Use v1 to choose our position
						knownPos[i] = True
						j = givens[0]
						#print(i, 'using v_%i' % j)
						theta_j = v1[1]
						self.points[i].x, self.points[i].y = (self.points[j].x + (r0*cos(theta_j)), self.points[j].y + (r0*sin(theta_j)))
						if checkEverything:
							# Expensive check for overlapping points, stops early when no overlap occurs.
							# Worst case scenario, 3*known points
							for theta_j_new in [v1[1] + pi, v1[1] + (pi*0.5), v1[1] + (pi*1.5)]:
								isOverlapped = False
								for k, p in enumerate(self.points):
									if k == i: continue
									if knownPos[k] == False: continue
									dr = self.points[i] - p
									if dr.lensq() < SMALL:
										#print("Found overlap, it's time to fix.")
										# We're on top of something known, move.
										self.points[i].x, self.points[i].y = (self.points[j].x + (r0*cos(theta_j_new)), self.points[j].y + (r0*sin(theta_j_new)))
										isOverlapped = True
										break
									#end if
								#next k, p
								# No overlap found, this is good enough.
								if not isOverlapped: break
							#next theta_j_new
						#end if
						# TODO: only set the values if we improve V
						continue
					#end if
					#print('avg')
					# Average of its peers
					totalPos = [0, 0]
					for j in givens:
						totalPos[0] += self.points[j].x
						totalPos[1] += self.points[j].y
					#next j
					avg = (totalPos[0] / len(givens), totalPos[1] / len(givens))
					self.points[i].x, self.points[i].y = avg
					print(self.points[i].name, 'added to avg of', [self.points[r].name for r in givens])
					knownPos[i] = True
				#end if
				if not (False in knownPos): break
			#next i
			if not (False in knownPos):
				break
			#end if
			# If knownDone is still true at this point, we're ready to fill in the rest of the values.
			if knownDone: fillReady = True
		#next roundTry
		#if False in knownPos:
		print("Took %i tries, %i nodes" % (roundTry + 1, len(self.points)))
		#end if
	#end def sortBranchMod(r0=40, knownPos=None)
#end class Map

class ConstraintDomain:
	def __init__(self, i, constraints, length):
		self.i = i
		self.constraints = constraints[:]
		self.length = length
	#end def ConstraintDomain(i, constraints)
	
	def getList(self, options):
		"""
		Generator over length
		"""
		for i in range(self.length):
			yield self.getOption(i, options)
		#next i
	#end def getList(options)
	
	def getOption(self, j, options):
		# This could be done better, but it works.
		# The way we get options[known] = [pos]
		if options[self.i] == self:
			#assert j == 0
			return self.constraints[0]
		#end if
		#opt = options[self.i].getOption(j // len(self.constraints), options)
		#return opt + self.constraints[j % len(self.constraints)]
		return self.constraints[j]
	#end def getOption(j, options)
	
	def pop(self, j):
		if len(self.constraints) == self.length:
			ret = self.constraints.pop(j)
			self.length -= 1
			return ret
		#end if
		# TODO!
		#print("pop {0} {1} {2} {3}".format(j, self.i, self.length, len(self.constraints)))
		return None
	#end def pop(j)
#end class ConstraintDomain

def getConst(x):
	"""
	get a list of combinations from a list of Constraints.
	getConst takes an array of arrays and tries every combination, the first element coming from the first array, the second from the second array and so on.
	Example:
	list(getConst([[1,2,3], ['a','b','c']]))
	[[1, 'a'], [1, 'b'], [1, 'c'], [2, 'a'], [2, 'b'], [2, 'c'], [3, 'a'], [3, 'b'], [3, 'c']]
	You don't have to worry about too large combinations because it is a well-written and tested generator.
	"""
	if len(x) == 1:
		for y in x[0]:
			yield [y]
		return
	#end if
	for y in x[0]:
		for i in getConst(x[1:]):
			yield [y] + i
	#next i
	return
#end def getConst(x)

class MapGroup:
	def __init__(self):
		self.points = []
		self.left_bracket = None
		self.right_bracket = None
		self.finished = False
	#end def MapGroup()
	
	def leaf(self, p):
		"""
		Make this group a single node leaf.
		"""
		self.finished = True
		self.points = [p]
		self.left_bracket = None
		self.right_bracket = None
	#end def leaf(p)
	
	def addPoint(self, p):
		"""
		Append a point to points.
		"""
		self.points.append(p)
	#end def addPoint(p)
	
	def cull(self):
		"""
		Remove any nodes that aren't part of a loop.
		For example: a-b-c-d-e-f-g, d-a. Remove e, f, and g.
		Return culled nodes. Remove nodes from self.points.
		FIXME: It doesn't work when a whole group is consumed by another group.
		"""
		# Obviously unnecessary to cull groups of 0, 1, or 2.
		if len(self.points) < 3: return []
		# TODO: Build a cache so that we can use it to be quicker.
		cache = []
		to_cull = []
		foundCull = True
		while foundCull:
			foundCull = False
			for p in self.points:
				conns_in_G = 0
				for q in p.conns:
					if q in self.points:
						conns_in_G += 1
					#end if
				#next q
				if conns_in_G < 2:
					to_cull.append(p)
					foundCull = True
					break
				#end if
			#next p
			if foundCull:
				self.points.remove(to_cull[-1])
			#end if
		#loop
		return to_cull
	#end def cull()
	
	def minX(self):
		"""
		A simple method to find the x value of the minimum x value among points.
		This allows necessary sorting.
		Example:
		groups.sort(key=lambda g:g.minX())
		"""
		return min([p.x for p in self.points])
	#end def minX()
	
	def __repr__(self):
		"""
		"""
		return '<MapGroup %r>' % ([p.name for p in self.points])
	#end def __repr__()
	
#end class MapGroup

class JsonMap(Map):
	"""
	A simple object to wrap Map and load JSON file on init.
	Useful for rsvg_map2.
	"""
	def __init__(self, filename='filename.json', seed_id = 234, level=0):
		seed(seed_id)
		Map.__init__(self)
		self.loadJson(open(filename, 'r').read())
	#end def __init__(filename='filename.json', seed_id = 234, level=0)
#end class JsonMap(Map)

class Vector2(object):
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	#end def __init__(x=0, y=0)
	
	def __str__(self):
		return ('%3.3f' % self.x) + ', ' + ('%3.3f' % self.y)
	#end def __str__()
	
	def __add__(self, vec):
		return Vector2(self.x + vec.x, self.y + vec.y)
	
	def __sub__(self, vec):
		return Vector2(self.x - vec.x, self.y - vec.y)
	
	def __mul__(self, other):
		return Vector2(self.x * other, self.y * other)
	
	def __truediv__(self, other):
		#if flt == 0:
		#	return Vector2(0, 0)
		#end if
		return Vector2(self.x / other, self.y / other)
	
	__div__ = __truediv__
	#def __iadd__(self, vec):
	#	v = Vector2(self.x + vec.x, self.y + vec.y)
	#	return v
	
	#def __idiv__(self, flt):
	#	v = Vector2(self.x / flt, self.y / flt)
	#	return v
	
	def setPos(self, v):
		self.x = v.x
		self.y = v.y
	#end def setPos(v)
	
	def length(self):
		return sqrt((self.x * self.x) + (self.y * self.y))
	#end def length()
	
	def lensq(self):
		return (self.x * self.x) + (self.y * self.y)
	#end def lensq()
	
	def dot(self, other):
		return (self.x * other.x) + (self.y * other.y)
	#end def dot(other)
	
#end class Vector2

class Point(Vector2):
	def __init__(self, name, conns=None, x=380, y=180, color='#6666ff', url='', size=4):
		Vector2.__init__(self, x, y)
		self.name = name
		self.url = url
		self.conns = conns
		self.color = color
		self.size = size
		if conns == None: self.conns = []
	#end def Point(name, conns=None, x=380, y=180, color='#6666ff', url='', size=4)
	
	def __str__(self):
		return str(self.name) + ' ' + Vector2.__str__(self)
	#end def __str__()
	
	def addConn(self, conn, reConn=True):
		#print 'adding conn?', self.name, conn
		self.conns.append(conn)
		if(reConn): conn.addConn(self, False)
	#end def addConn(conn, reConn=True)
	
	def setColor(self, value):
		""" Set color to a hex value like #ff0000 """
		self.color = value
	#end def setColor(value)
	
	def __lt__(self, other):
		"""
		For dijkstra, heapq.
		"""
		return False
	#end def __lt__(other)
#end class Point(Vector2)

def loadPolar():
	"""
	Optional cheap polar coordinates module.
	"""
	global polar1
	import polar1
#end def loadPolar()

def gridToPos(grid, width=40):
	"""
	Simple function does the positioning of nodes in grid.
	Assumes a proper grid of points.
	TODO: When multiple nodes are in one cell, they should be spread out as 
	much as possible.
	"""
	for y in range(len(grid)):
		for x in range(len(grid[0])):
			if grid[y][x]:
				if type(grid[y][x]) == list:
					for p in grid[y][x]:
						p.setPos(Vector2(x * width, y * width))
					#end if
				else:
					#print(x, y, grid[y][x].name)
					grid[y][x].setPos(Vector2(x * width, y * width))
				#end if
			#end if
		#next x
	#next y
#end def gridToPos(grid)

class PotentialCache:
	def __init__(self, PotentialA, variant):
		self.PotentialA = PotentialA
		self.variant = variant
	#end def PotentialCache(PotentialA, variant)
#end class PotentialCache

def V_SmallWideWorld_Cache(x, conns, b0, lj_conf, nonConns, cache):
	"""
	A speed up of sww_optimize1.V_SmallWideWorld (hopefully).
	FIXME: Cache produces incorrect results for some reason.
	TODO: speed test.
	"""
	Potential = cache.PotentialA
	dps_all = []
	for i in range(len(conns)):
		dps_all.append([])
	#next i
	# Generate conns list for each node
	for i in [cache.variant]:
		pt_i = Vector2(*x[2*i:2*i+2])
		for j in conns[i]:
			pt_j = Vector2(*x[2*j:2*j+2])
			dp = pt_i - pt_j
			dps_all[i].append(dp)
			dps_all[j].append(dp * -1.)
		#next j
	#next i
	# Harmonic potential with length b0.
	for i in [cache.variant]:
		pt_i = Vector2(*x[2*i:2*i+2])
		dps = dps_all[i]
		for j in conns[i]:
			pt_j = Vector2(*x[2*j:2*j+2])
			dp = pt_i - pt_j
			dp_len = dp.length()
			Potential += V_Harmonic(dp_len, b0)
		#next j
		if len(dps) >= 2:
			# Angular Harmonic calculation
			theta0 = 2 * pi / len(dps)
			# theta is computed for axb, bxc, cxa
			thetas = []
			for k in range(len(dps)):
				ax = dps[k]
				thetas.append(atan2(ax.y, ax.x) % (2*pi))
			#next k
			thetas.sort()
			for k in range(len(thetas)):
				b = (k + 1) % len(thetas)
				theta = (thetas[b] - thetas[k]) % (2*pi)
				Potential += V_Harmonic_Angle(theta, theta0)
			#next k
		#end if
	#next i
	# Lennard-Jones for non-connected nodes.
	for i in [cache.variant]:
		pt_i = Vector2(*x[2*i:2*i+2])
		for j in nonConns[i]:
			pt_j = Vector2(*x[2*j:2*j+2])
			dp = pt_i - pt_j
			dp_len = dp.length()
			Potential += lj_conf.V_LJ(dp_len)
		#next j
	#next i
	return Potential
#end def V_SmallWideWorld_Cache(x, conns, b0, lj_conf, nonConns, cache)

def getOptionsList(pos_i, pos_j, brute=False):
	"""
	Pick spots to move i based on position of i and j.
	"""
	ret = []
	# TODO: Deal with i and j being in all possible configurations dx pos, neg, dy pos, neg.
	dx = pos_j[0] - pos_i[0]
	dy = pos_j[1] - pos_i[1]
	stepk = 1
	stepm = 1
	startk = 0
	startm = 0
	if dx < 0:
		stepk = -1
	#end if
	if dy < 0:
		stepm = -1
		dy -= 1
	else:
		dy += 1
	#end if
	#print('km', startk, dx, stepk, startm, dy, stepm)
	if brute or abs(dx*dy) <= 6:
		for k in range(startk, dx, stepk):
			for m in range(startm, dy, stepm):
				ret.append([pos_i[0] + k, pos_i[1] + m])
			#next m
		#next k
		# Reject the first one which is pos_i
		return ret[1:]
	#end if
	if dx != 0:
		ret.append([pos_i[0] + stepk, pos_i[1]])
		ret.append([pos_j[0] - stepk, pos_j[1]])
	#end if
	if dy > 1 or dy < -1:
		ret.append([pos_i[0], pos_i[1] + stepm])
		ret.append([pos_j[0], pos_j[1] - stepm])
	#end if
	return ret
#end def getOptionsList(pos_i, pos_j, brute=False)

def getNonConns(conns, i_lt_j=False):
	"""
	Inverse of conns. If a is not connected to b, b should be in conns[a].
	If you set i_lt_j == True, it will filter where i >= j.
	Example:
	conns = [[1], [0, 2], [1, 3, 4], [2], [2]]
	i_lt_j = false
	nonConns = [[2, 3, 4], [3, 4], [0], [0, 1, 4], [0, 1, 3]]
	i_lt_j = true
	nonConns = [[2, 3, 4], [3, 4], [], [4], []]
	TODO: Serious unit test.
	"""
	nonConns = []
	for i in range(len(conns)):
		nc = []
		for j in range(len(conns)):
			# Don't check against ourself.
			if i == j: continue
			# If we are connected, not not connected
			if j in conns[i] or i in conns[j]: continue
			nc.append(j)
		#next j
		if i_lt_j: nc = list(filter(lambda j: i<j, nc))
		nonConns.append(nc)
	#next i
	return nonConns
#end def getNonConns(conns, i_lt_j=False)
	
def createMap(seed_id=3243):
	seed(seed_id)
	a = Map()
	b = []
	for i in range(8):
		b.append(Point(chr(ord('b')+i)))
	#next i
	for i in range(7):
		b[i].addConn(b[i+1])
	#next i
	addConn1 = randint(0,len(b)-1)
	addConn2 = (addConn1 + randint(0,len(b))) % len(b)
	if addConn1 == addConn2:
		# Possible
		addConn2 = (addConn1 ^ 7) % len(b)
	if addConn1 == addConn2:
		# Unlikely
		addConn1 = 0
	if addConn1 == addConn2:
		# Impossible
		addConn2 = 1
	#print b, addConn1, addConn2
	b[addConn1].addConn(b[addConn2])
	a.addPoints(b)
	for i in range(4):
		a.randomize()
		a.sort1()
		#a.sort1()
		#a.sort1()
		#a.sort1()
		#a.sort1()
	#next i
	return a
#end def createMap([seed_id])

def main():
	print(createMap())
#end def main()

if __name__ == '__main__':
	main()
#end if
