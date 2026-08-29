
import math, os
import FreeCAD as App, FreeCADGui as Gui
V, Rot, Pl = App.Vector, App.Rotation, App.Placement
L1, L2 = 250.0, 200.0
CUBES = ["CubeRed","CubeGreen","CubeBlue"]
PICK = [(-60,70), (-45,60), (-30,50)]
PLACE = (50, 60)
T4_PLACE = -110.0

def tip_xy(t1, t2):
    a = math.radians(t1); b = math.radians(t1+t2)
    return V(L1*math.cos(a)+L2*math.cos(b), L1*math.sin(a)+L2*math.sin(b), 0)

def reset_cubes(doc):
    for (t1,t2), n in zip(PICK, CUBES):
        doc.getObject(n).Placement = Pl(tip_xy(t1,t2), Rot(V(0,0,1), t1+t2))

def set_pose(doc, t1, t2, z, t4, grip):
    p1 = Pl(V(0,0,0), Rot(V(0,0,1), t1)); doc.Arm1.Placement = p1
    p2 = p1.multiply(Pl(V(L1,0,0), Rot(V(0,0,1), t2))); doc.Arm2.Placement = p2
    p3 = p2.multiply(Pl(V(L2,0,-z), Rot(V(0,0,1), t4)))
    doc.ZShaft.Placement = p3; doc.GripperPalm.Placement = p3
    gap = 10*grip
    doc.FingerL.Placement = p3.multiply(Pl(V( gap,0,0), Rot()))
    doc.FingerR.Placement = p3.multiply(Pl(V(-gap,0,0), Rot()))
    return p3

# keyframes: (t, t1, t2, z, t4, grip, held)  held = cube index or -1
def build_keys():
    K = []
    t = 0.0
    def add(dt, t1,t2,z,t4,g,h):
        nonlocal t
        t += dt; K.append((t,t1,t2,z,t4,g,h))
    add(0.0, 0,0,0,0,0,-1)
    add(0.5, 0,0,0,0,0,-1)
    for i,(p1,p2) in enumerate(PICK):
        zp = 140 - 40*i
        add(1.2, p1,p2,0,0,0,-1)
        add(0.6, p1,p2,140,0,0,-1)
        add(0.3, p1,p2,140,0,1,i)
        add(0.6, p1,p2,0,0,1,i)
        add(1.5, PLACE[0],PLACE[1],0,T4_PLACE,1,i)
        add(0.6, PLACE[0],PLACE[1],zp,T4_PLACE,1,i)
        add(0.3, PLACE[0],PLACE[1],zp,T4_PLACE,0,-1)
        add(0.6, PLACE[0],PLACE[1],0,T4_PLACE,0,-1)
    add(1.2, 0,0,0,0,0,-1)
    add(0.5, 0,0,0,0,0,-1)
    return K

def smooth(u):
    u = max(0.0, min(1.0, u)); return u*u*(3-2*u)

def pose_at(K, t):
    if t <= K[0][0]: return K[0][1:]
    for a,b in zip(K, K[1:]):
        if t <= b[0]:
            u = smooth((t-a[0])/(b[0]-a[0])) if b[0]>a[0] else 1
            vals = [a[k]+(b[k]-a[k])*u for k in range(1,6)]
            return tuple(vals)+(b[6] if u>=0.5 or a[6]==b[6] else a[6],)
    return K[-1][1:]

def apply(doc, K, t, state):
    t1,t2,z,t4,g,held = pose_at(K,t)
    p3 = set_pose(doc,t1,t2,z,t4,g)
    if held >= 0:
        c = doc.getObject(CUBES[held])
        if state.get("held") != held:
            state["rel"] = p3.inverse().multiply(c.Placement); state["held"] = held
        c.Placement = p3.multiply(state["rel"])
    else:
        state["held"] = -1
    doc.recompute()

def setup_camera(view):
    view.viewIsometric()
    view.fitAll()
    for _ in range(2): view.zoomIn()

def render(doc, outdir, fps=30, w=1280, h=720, f0=0, f1=None, K=None, state=None):
    K = K or build_keys()
    total = int(K[-1][0]*fps)+1
    f1 = total if f1 is None else min(f1,total)
    view = Gui.getDocument(doc.Name).ActiveView
    state = state if state is not None else {}
    # rebuild state deterministically by replaying held transitions up to f0
    reset_cubes(doc)
    for f in range(0, f0):
        apply(doc, K, f/fps, state)
    for f in range(f0, f1):
        apply(doc, K, f/fps, state)
        Gui.updateGui()
        view.saveImage(os.path.join(outdir, "frame_%04d.png" % f), w, h, "Current")
    return total, f1
