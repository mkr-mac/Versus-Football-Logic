import math

class Player:
  
  def __init__(self, home_or_away, stats):
    # Stats
    self.side = home_or_away
    self.name = stats[0]
    self.number = stats[1]
    self.speed = int(stats[2])*10
    self.hit = stats[3]
    self.kicking = stats[4]
    self.disipline = stats[5]
    self.recieving = stats[6]
    self.passing = stats[7]
    self.stats = stats[:-1]

    # Coordinates
    self.x = 0.0
    self.y = 0.0

    # Flags!
    self.down = False
    self.diving = True
    self.collidable = True
    self.can_catch = False

  def move(self, dirc, mod, opposite_team):
    mag = self.speed*mod
    opposite_team_coords = []
    for pl in opposite_team:
      opposite_team_coords.append((pl.x, pl.y))
    if 'N' in dirc:
      co = self.collide((self.x, self.y),opposite_team_coords, (0,mag))
    if 'S' in dirc:
      co = self.collide((self.x, self.y),opposite_team_coords, (0,-1*mag))
    if 'F' in dirc:
      co = self.collide((self.x, self.y),opposite_team_coords, (mag,0))
    if 'B' in dirc:
      co = self.collide((self.x, self.y),opposite_team_coords, (-1*mag,0))

    x, y = co[0]

  def dive(self, dirc):
    if 'N' in dirc:
      self.y += 1.0
    if 'S' in dirc:
      self.y += 1.0
    if 'F' in dirc:
      self.x += 1.0
    if 'B' in dirc:
      self.x -= 1.0

  def set_position(self, pos_data):
    self.collidable = True
    self.can_catch = False

    pos = pos_data[1]
    if len(pos_data) > 3:
      if int(pos_data[3]) > -500:
        pos_data[3] = -500

    if pos == 'C':
      self.x = -500
      self.y = 0.0

    elif pos == 'RG':
      self.x = -500
      self.y = -1000

    elif pos == 'RT':
      self.x = -500
      self.y = -2000

    elif pos == 'LG':
      self.x = -500
      self.y = 1000

    elif pos == 'LT':
      self.x = -500
      self.y = 2000

    elif ((pos == 'R') or (pos == 'D')):
      self.x = int(pos_data[3])
      self.y = int(pos_data[4])

    elif pos == 'QB':
      self.x = int(pos_data[3])
      self.y = 0

  def throw(self, target_x, target_y, lob):
    if not has_ball:
      return
    # TODO: Solve for arc
    self.Ball.setvector(2, 2, 2)

  def get_stat_csv(self):
    csv = ""
    for stat in self.stats:
      csv += str(stat)
      csv += ","

    return csv[:-1]


  def get_stat_with_pos_csv(self):
    csv = ""
    for stat in self.stats:
      csv += str(stat)
      csv += ","

    csv += str(int(self.x)) + ","
    csv += str(int(self.y))

    return csv

  def get_position_csv(self):
    csv = ""
    csv += str(self.stats[0]) + ","
    csv += str(self.stats[1]) + ","
    csv += str(int(self.x)) + ","
    csv += str(int(self.y))

    return csv

  # INPUTS:
  # COORD: center coords of player to move, in milliyards.
  # OTHER_COORDS: coords of other targets that can be collided with
  # DELTA: how far that the player moves.

  # OUTPUTS:
  # if no collide, i send new coords, and a None. [Example [-3444,340509],None]
  # if collide, i send new coords, and an index + degree of impact. [Example [-3444,340509],None]

  # PROBLEMS:
  # Uses a Naive Algorithm. I can make this faster by pruning distant players.
  def collide(coord,other_coords,delta):

    # Helpers
    def sign(x):
      if x == 0:
        return 0
      if x < 0:
        return -1
      if x > 0:
        return 1

    def did_collide(a,b):
      # If the center points are both within 1000 you collided.
      x_collide = abs(a[0] - b[0]) <= 1000
      y_collide = abs(a[1] - b[1]) <= 1000
      return x_collide and y_collide


    # How many steps? Also, how far to go?
    step_delta = [sign(delta[0]),sign(delta[1])]
    steps = max([abs(delta[0]),abs(delta[1])])

    for i in range(steps):
      coord = [coord[0] + step_delta[0],coord[1] + step_delta[1]]
      for idx, other_coord in enumerate(other_coords):
        if did_collide(coord,other_coord):
          # Undo step
          coord = [coord[0] - step_delta[0],coord[1] - step_delta[1]]
          # Calculate collision angle
          angle = math.degrees(math.atan2(other_coord[1] - coord[1], other_coord[0] - coord[0]))
          # return index
          return [coord,[idx,angle]]

    return [coord,None]
