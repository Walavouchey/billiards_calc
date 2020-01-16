# Calculates which corner a ball lands on when shot at 45 degree angles inside a
# rectangular billiard table, rebounding with elastic collisions and no friction

import math
import sys

def bounce(width, height, x, y, angle, maxIter, debug=0):

    def intersection(x1, y1, x2, y2, x3, y3, x4, y4):
        # Calculates the intersection between two line segments,
        # and returns the position of intersection, if there is one.
        # It's basically black magic derived from matrix determinants.
        # See https://en.wikipedia.org/wiki/Line_line_intersection
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den is 0:
            return None
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        if t <= 0:
            return None
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        if u < -0.0001 or u > 1.0001: # floating point error tolerances
            return None
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return round(x, 3), round(y, 3)

    def moveBall(x, y, angle, top, bot, lft, rgt):
        dirx = x + angle[0]
        diry = y - angle[1]

        # Calculate intersections to each side of the rectangle
        # The y-axis is flipped, btw
        hitTop = intersection(x, y, dirx, diry, lft, top, rgt, top) # top
        hitBot = intersection(x, y, dirx, diry, lft, bot, rgt, bot) # bottom
        hitLft = intersection(x, y, dirx, diry, lft, top, lft, bot) # left
        hitRgt = intersection(x, y, dirx, diry, rgt, top, rgt, bot) # right
        if(debug):
            if hitTop:
                print("Top", hitTop)
            if hitBot:
                print("Bot", hitBot)
            if hitLft:
                print("Lft", hitLft)
            if hitRgt:
                print("Rgt", hitRgt)
        
        # If ball hit a corner, print out which one.
        if hitTop and hitLft:
            return "Top left"
        if hitBot and hitLft:
            return "Bottom left"
        if hitTop and hitRgt:
            return "Top right"
        if hitBot and hitRgt:
            return "Bottom right"
        
        # If not, return the point where the ball collided.
        # Yes, there is a better way to do this.
        if hitTop:
            return hitTop
        if hitBot:
            return hitBot
        if hitLft:
            return hitLft
        if hitRgt:
            return hitRgt
        raise ValueError("Ball went out of bounds!")

    angle = angle * math.pi / 180
    angle = [math.cos(angle), math.sin(angle)]
    iter = 0
    while True:
        try:
            hit = moveBall(x, y, angle, 0, height, 0, width)
        except ValueError as err:
            print(err, iter)
            break

        # If the ball hits a corner, print result and exit
        if type(hit) == str:
            print(hit, "after", iter, "bounces")
            break
        
        # Put ball at new position
        x = hit[0]
        y = hit[1]

        # Reflect ball's "velocity"
        if hit[0] == 0 or hit[0] == width:
            angle[0] *= -1
        if hit[1] == 0 or hit[1] == height:
            angle[1] *= -1

        if iter >= maxIter:
            print("At", hit, "after", iter, "bounces")
            break
        else:
            iter += 1

# Width, height (of the box), x, y (of the ball), angle, maxBounces, printBounces
a = sys.argv[1:]
j = 0
for i in a:
    a[j] = float(i)
    j += 1
bounce(a[0], a[1], a[2], a[3], a[4], a[5], a[6])
