from math import pi, sin, cos, asin, acos, atan2


def to_radians(angle_in_degrees):
    return angle_in_degrees * pi / 180.0


def to_degrees(angle_in_radians):
    return angle_in_radians * 180.0 / pi


def offset(c1, distance, bearing):
    lat1 = to_radians(c1[1])
    lon1 = to_radians(c1[0])
    dByR = distance / 6378137
    lat = asin(sin(lat1) * cos(dByR) + cos(lat1) * sin(dByR) * cos(bearing))
    lon = lon1 + atan2(sin(bearing) * sin(dByR) * cos(lat1), cos(dByR) - sin(lat1) * sin(lat))
    return [to_degrees(lon), to_degrees(lat)]


def circle_to_polygon(center, radius, num_segments):
    coordinates = []
    for i in range(num_segments):
        coordinates.append(offset(center, radius, 2 * pi * i / num_segments))
    coordinates.append(coordinates[0])
    return coordinates

coord = circle_to_polygon((4.400864, 51.225588), 50, 1000)
print([coord])
