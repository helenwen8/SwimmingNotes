# this is a test file
# of me trying to make terrains
# also we will make items here ol
# lol rip

# so the goal of terrain class is to generate said terrain with given specification
# what is the given specification? idfk... probably a list of x,y points?
# if we can randomize, we just have to write more functions to randomly generate
# but ya fuck this


class Terrain(object):
    # type - sharp edges or smooth arcs
    # pointsList - know where to draw the things
    def __init__(self, pointsList, drawType):
        self.pointsList = pointsList
        self.type = type
        pass

    def drawTerrain(self, yeet):
        pass

# so this is the type of terrain where you can climb wall on
# this is the one that really really really need attention on the hitbox thing

class StickyTerrain(Terrain):
    def __init__(self, pointsList, type):
        pass

# so this is bad terrain
# if you touch this you die lel

class ScaryTerrain(Terrain):
    def __init__(self, pointsList):
        pass

    def drawTerrain(self, uyeet):
        pass

class Collectables(object):
    def __init__(self):
        pass