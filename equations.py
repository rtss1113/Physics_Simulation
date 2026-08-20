import math

def initial_velocity_components(initial_velocity, firing_angle):
    firing_angle_rad = math.radians(firing_angle)
    vi_hori = initial_velocity * math.cos(firing_angle_rad)
    vi_vert = initial_velocity * math.sin(firing_angle_rad)
    return vi_hori, vi_vert

def velocity_components(initial_velocity, firing_angle, time, gravity):
    vi_hori, v_vert = initial_velocity_components(initial_velocity, firing_angle)

    vf_hori = vi_hori + (0 * time)
    vf_vert = v_vert + (-gravity * time)

    return vf_hori, vf_vert

def total_velocity(vf_hori, vf_vert):
    return math.sqrt(vf_hori ** 2 + vf_vert ** 2)


def acceleration_components(gravity):
    a_hori = 0.0
    a_vert = -gravity
    return a_hori, a_vert

def total_acceleration(a_hori, a_vert):
    return math.sqrt(a_hori ** 2 + a_vert ** 2)

def ke(mass, v_total):
    return 0.5 * mass * v_total ** 2

def gpe(mass, gravity, height):
    return mass * gravity * height

def position(initial_velocity, firing_angle, time, gravity, cannon_height):
    vi_hori, vi_vert = initial_velocity_components(initial_velocity, firing_angle)
    d_hori = (vi_hori * time) + (0.5 * 0 * time ** 2)
    d_vert = (vi_vert * time) + (0.5 * -gravity * time ** 2)

    hori = d_hori
    vert = d_vert + cannon_height

    return hori, vert