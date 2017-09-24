from Player import Player
import math, random

class Ball:
  # Position
  x=y=z=0
  # Speed vector
  x_speed=y_speed=z_speed=0
  # A held flag
  held = False
  # Passed
  passed = False
  side = ""

  gravity = 10.72835

  def __init__(self):
    pass


  def set_position(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def setvector(self, x, y, z):
    self.x_speed = x
    self.y_speed = y
    self.z_speed = z

  def throw(self, x, y):
    dist = math.sqrt(math.pow(x-self.x, 2)+math.pow(y-self.y, 2))
    vel = math.sqrt(dist/self.gravity) * self.gravity
    if self.held:
      acc = 50-(int(self.held.passing)/4)
    else:
      acc = 0
    self.z_speed = ((math.sqrt(2)*vel)/2) * (1 + random.randint(-acc, acc)/100)
    self.y_speed = (((math.sqrt(2)*vel)/2) * math.atan(abs(y-self.y)/abs(x-self.x))) * (1 + random.randint(-acc, acc)/100)
    self.x_speed = (self.z_speed-self.y_speed) * (1 + random.randint(-acc, acc)/100)
    self.held = False

  def snap(self, dir):
    self.throw(dir*7000, 0)

  def update(self, o_players, d_players):

    if not self.held:

      for pl in o_players:
        if pl.can_catch:
          if self.check_if_near(pl.x, pl.y):
            self.player_hold(pl, "o")
            break

      if not self.held:
        for pl in d_players:
          if pl.can_catch:
            if self.check_if_near(-1*pl.x, -1*pl.y):
              self.player_hold(pl, "d")
              break

      self.x += self.x_speed
      self.y += self.y_speed
      self.z += self.z_speed
      self.z_speed -= self.gravity
      if self.z <= 0:
        self.setvector(0,0,0)
        self.z = 0



  def check_if_near(self, x, y):    
    x_collide = abs(x - self.x) <= 500
    y_collide = abs(y - self.y) <= 500
    return x_collide and y_collide


  def player_hold(self, player, side):
    self.held = player
    self.side = side
    self.x = player.x
    self.y = player.y
    self.z = 1.5

  def get_status(self):
    if self.held:
      return self.side + "," + str(self.held.number)
    else:
      t_p = str(int(self.x)) + "," + str(int(self.y)) + "," + str(int(self.z))
      t_v = str(int(self.x_speed)) + "," + str(int(self.y_speed)) + "," + str(int(self.z_speed))
      return str(t_p) + "," + str(t_v)