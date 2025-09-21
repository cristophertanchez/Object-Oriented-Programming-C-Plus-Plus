"""
arm_kinematics.py

What this script does:
1) Forward kinematics (positions of A, B, C) for two angle conventions:
   - ABSOLUTE: θ1, θ2, θ3 are measured from the global x-axis.
   - RELATIVE: θ1 is from x-axis; θ2 from link1; θ3 from link2.
2) Time update: θ(t+Δt) = θ(t) + ω * Δt  (constant angular velocity during Δt).
3) Instantaneous endpoint velocities from ω’s.
4) Demo at the bottom you can edit.

Coordinates:
- x to the right, y up.
- Link lengths: L1, L2, L3 > 0
- Angles are in RADIANS in the math. Use helpers deg()/rad() to convert.

Points:
- A: end of link 1
- B: end of link 2
- C: end of link 3
"""

from __future__ import annotations
import math
from dataclasses import dataclass

# ---------- helpers to make degrees/radians painless ----------
def deg(d: float) -> float:
    "degrees -> radians"
    return math.radians(d)

def rad(r: float) -> float:
    "radians -> radians (identity) – for symmetry/readability"
    return r


@dataclass
class Links:
    L1: float
    L2: float
    L3: float

@dataclass
class Angles:
    θ1: float
    θ2: float
    θ3: float

@dataclass
class Omegas:
    ω1: float
    ω2: float
    ω3: float

@dataclass
class Points:
    A: tuple[float, float]
    B: tuple[float, float]
    C: tuple[float, float]


# ---------- 1) forward kinematics ----------
def fk_absolute(θ: Angles, L: Links) -> Points:
    """
    Angles ABSOLUTE to the global x-axis (each link has its own absolute θ).
    A = (L1 cos θ1,                                L1 sin θ1)
    B = A + (L2 cos θ2,                            L2 sin θ2)
    C = B + (L3 cos θ3,                            L3 sin θ3)
    """
    xA = L.L1 * math.cos(θ.θ1);  yA = L.L1 * math.sin(θ.θ1)
    xB = xA + L.L2 * math.cos(θ.θ2);  yB = yA + L.L2 * math.sin(θ.θ2)
    xC = xB + L.L3 * math.cos(θ.θ3);  yC = yB + L.L3 * math.sin(θ.θ3)
    return Points(A=(xA,yA), B=(xB,yB), C=(xC,yC))

def fk_relative(θ: Angles, L: Links) -> Points:
    """
    Angles RELATIVE (typical robotics, also called "joint angles"):
    Link1 absolute angle:       α1 = θ1
    Link2 absolute orientation: α2 = θ1 + θ2
    Link3 absolute orientation: α3 = θ1 + θ2 + θ3
    """
    α1 = θ.θ1
    α2 = θ.θ1 + θ.θ2
    α3 = θ.θ1 + θ.θ2 + θ.θ3

    xA = L.L1 * math.cos(α1);  yA = L.L1 * math.sin(α1)
    xB = xA + L.L2 * math.cos(α2);  yB = yA + L.L2 * math.sin(α2)
    xC = xB + L.L3 * math.cos(α3);  yC = yB + L.L3 * math.sin(α3)
    return Points(A=(xA,yA), B=(xB,yB), C=(xC,yC))


# ---------- 2) integrate angles over a small Δt ----------
def step_angles(θ: Angles, ω: Omegas, dt: float) -> Angles:
    """
    Simple Euler integration for constant angular velocities over Δt:
    θ_new = θ_old + ω * dt
    """
    return Angles(θ1=θ.θ1 + ω.ω1*dt,
                  θ2=θ.θ2 + ω.ω2*dt,
                  θ3=θ.θ3 + ω.ω3*dt)


# ---------- 3) instantaneous endpoint velocities (optional) ----------
def velocities_absolute(θ: Angles, ω: Omegas, L: Links) -> Points:
    """
    If each link's θ is absolute, each endpoint velocity is sum of each link's contribution.
    For a link with absolute angle α and angular speed ω, the endpoint velocity contribution is
      v = ω * L * (-sin α, cos α)
    A gets term from link1; B gets link1+link2; C gets link1+link2+link3.
    """
    # contributions
    v1 = (ω.ω1 * L.L1 * -math.sin(θ.θ1),  ω.ω1 * L.L1 *  math.cos(θ.θ1))
    v2 = (ω.ω2 * L.L2 * -math.sin(θ.θ2),  ω.ω2 * L.L2 *  math.cos(θ.θ2))
    v3 = (ω.ω3 * L.L3 * -math.sin(θ.θ3),  ω.ω3 * L.L3 *  math.cos(θ.θ3))
    vA = v1
    vB = (v1[0]+v2[0], v1[1]+v2[1])
    vC = (v1[0]+v2[0]+v3[0], v1[1]+v2[1]+v3[1])
    return Points(A=vA, B=vB, C=vC)

def velocities_relative(θ: Angles, ω: Omegas, L: Links) -> Points:
    """
    For RELATIVE (joint) angles, the absolute orientations are α1=θ1, α2=θ1+θ2, α3=θ1+θ2+θ3,
    and each joint's angular velocity adds perpendicular motion to all downstream links.
    Velocity of A:        ω1 x r1 (with α1)
    Velocity of B:        ω1 x r1 + ω2 x r2 (with α2)
    Velocity of C:        ω1 x r1 + ω2 x r2 + ω3 x r3 (with α3)
    Each "ωk x rk" in 2D becomes: ωk * Lk * (-sin αk, cos αk)
    """
    α1 = θ.θ1
    α2 = θ.θ1 + θ.θ2
    α3 = θ.θ1 + θ.θ2 + θ.θ3
    v1 = (ω.ω1 * L.L1 * -math.sin(α1),  ω.ω1 * L.L1 *  math.cos(α1))
    v2 = (ω.ω2 * L.L2 * -math.sin(α2),  ω.ω2 * L.L2 *  math.cos(α2))
    v3 = (ω.ω3 * L.L3 * -math.sin(α3),  ω.ω3 * L.L3 *  math.cos(α3))
    vA = v1
    vB = (v1[0]+v2[0], v1[1]+v2[1])
    vC = (v1[0]+v2[0]+v3[0], v1[1]+v2[1]+v3[1])
    return Points(A=vA, B=vB, C=vC)


# ---------- 4) convenience wrappers ----------
def forward_kinematics(θ: Angles, L: Links, mode: str="ABSOLUTE") -> Points:
    mode = mode.upper()
    if mode == "ABSOLUTE":
        return fk_absolute(θ, L)
    elif mode == "RELATIVE":
        return fk_relative(θ, L)
    else:
        raise ValueError("mode must be 'ABSOLUTE' or 'RELATIVE'")

def endpoint_velocities(θ: Angles, ω: Omegas, L: Links, mode: str="ABSOLUTE") -> Points:
    mode = mode.upper()
    if mode == "ABSOLUTE":
        return velocities_absolute(θ, ω, L)
    elif mode == "RELATIVE":
        return velocities_relative(θ, ω, L)
    else:
        raise ValueError("mode must be 'ABSOLUTE' or 'RELATIVE'")


# ---------- 5) demo you can edit ----------
if __name__ == "__main__":
    # --- choose your inputs ---
    L = Links(L1=2.0, L2=1.5, L3=1.0)         # lengths (units)
    θ = Angles(θ1=deg(30), θ2=deg(20), θ3=deg(-10))  # initial angles
    ω = Omegas(ω1=deg(15), ω2=deg(-20), ω3=deg(10))  # angular velocities (rad/s)
    dt = 0.05                                   # time step (s)

    MODE = "ABSOLUTE"   # "ABSOLUTE" or "RELATIVE" — switch to match needed convention

    # --- current positions ---
    P = forward_kinematics(θ, L, MODE)
    print(f"t:      A{P.A}  B{P.B}  C{P.C}")

    # --- advance angles by Δt, then recompute positions ---
    θ_next = step_angles(θ, ω, dt)
    P_next = forward_kinematics(θ_next, L, MODE)
    print(f"t+dt:   A{P_next.A}  B{P_next.B}  C{P_next.C}")

    # --- instantaneous endpoint velocities at time t ---
    V = endpoint_velocities(θ, ω, L, MODE)
    print(f"vel:    vA{V.A}  vB{V.B}  vC{V.C}   (units/s)")
# --------------------------------------------------------------

# ----- plotting helper: simulate and visualize the arm over time -----
import math
import matplotlib.pyplot as plt

def simulate_and_plot(L, theta0, omega, dt=0.05, steps=200, mode="RELATIVE", trail=True):
    """
    Euler step: theta <- theta + omega*dt
    Then compute A,B,C via forward kinematics and plot the motion.
    L: Links(L1,L2,L3)
    theta0: Angles(θ1,θ2,θ3)
    omega: Omegas(ω1,ω2,ω3)   (radians/sec)
    dt: timestep (sec)
    steps: number of steps to simulate
    mode: "RELATIVE" or "ABSOLUTE"
    trail: if True, leaves a path of C (end-effector)
    """
    # pick FK based on convention
    fk = fk_relative if mode.upper() == "RELATIVE" else fk_absolute

    # sim storage
    As, Bs, Cs = [], [], []
    th = theta0

    # precompute a reasonable axis limit
    Lsum = L.L1 + L.L2 + L.L3
    lim = Lsum * 1.1

    # live plot setup
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"3-Link Arm ({mode}) — Euler dt={dt}")

    # artists
    arm_line, = ax.plot([], [], "-", lw=3)           # O->A->B->C polyline
    tip_trail, = ax.plot([], [], ".", ms=2, alpha=0.6) if trail else (None,)
    origin_dot = ax.plot([0], [0], "ko")[0]

    for n in range(steps):
        # record current positions
        P = fk(th, L)
        A, B, C = P.A, P.B, P.C
        As.append(A); Bs.append(B); Cs.append(C)

        # draw
        arm_line.set_data([0, A[0], B[0], C[0]], [0, A[1], B[1], C[1]])
        if trail:
            tip_trail.set_data([p[0] for p in Cs], [p[1] for p in Cs])
        plt.pause(0.001)

        # Euler step (angles)
        th = step_angles(th, omega, dt)

    plt.ioff()
    plt.show()
# ----------------- end of plotting helper -----------------
if __name__ == "__main__":
    L = Links(L1=2.0, L2=1.5, L3=1.0)
    θ  = Angles(θ1=deg(30), θ2=deg(20), θ3=deg(-10))
    ω  = Omegas(ω1=deg(15), ω2=deg(-20), ω3=deg(10))
    dt = 0.05

    # one-shot prints (what you already had)
    P = forward_kinematics(θ, L, mode="RELATIVE")
    print("A,B,C at t:", P)
    Pn = forward_kinematics(step_angles(θ, ω, dt), L, mode="RELATIVE")
    print("A,B,C at t+dt:", Pn)

    # now visualize a few seconds of motion
    simulate_and_plot(L, θ, ω, dt=dt, steps=200, mode="RELATIVE", trail=True)
