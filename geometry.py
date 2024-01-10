import math

def isAligned(angle1, angle2) -> bool:
    return abs(angle1 - angle2) < 0.15

def isOpposite(angle1, angle2) -> bool:
        return abs(angle1 - angle2) < math.pi + 0.15 and abs(angle1 - angle2) > math.pi - 0.15

def isPerpendicular(angle1, angle2) -> bool:
    return abs(angle1 - angle2) < 0.5 * math.pi + 0.15 and abs(angle1 - angle2) > 0.5 * math.pi - 0.15
