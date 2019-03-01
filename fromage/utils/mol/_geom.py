import numpy as np
import fromage.utils.array_operations as ao

class GeomInfo(object):
    """
    Contains the extended geometrical information for Mol objects

    This object is meant exclusively to store geometrical data. It needs to be
    initialised as empty since calculating some of the properties is time
    intensive. As such, it needs to be assignable which rules out simply using
    a namedtuple.

    Attributes
    ----------
    coord_array : np array of shape Nat X 3
        Atom coordinates
    plane_coeffs : 3 x 1 np array
        Coefficients for the plane which averages coord_array
    prin_ax : 3 x 1 np array
        Vector representing the principal axis of the molecule
    sec_ax : 3 x 1 np array
        Vector representing the secondary axis of the molecule
    perp_ax : 3 x 1 np array
        Vector perpendicular to the other two such that
        perp_ax = prin_ax (cross) sec_ax

    """
    def __init__(self):
        self.coord_array = None
        self.plane_coeffs = None
        self.prin_ax = None
        self.sec_ax = None
        self.perp_ax = None

    def __str__(self):
        out_str = "Coordinate array:\n" + str(self.coord_array) + "\nPlane coefficients:\n" + str(
            self.plane_coeffs) + "\nPrincipal axis:\n" + str(self.prin_ax) + "\nSecondary axis:\n" + str(
            self.sec_ax) + "\nPerpendicular axis:\n" + str(self.perp_ax)
        return out_str

    def __repr__(self):
        return self.__str__()


def coord_array(self):
    """
    Return a numpy array of the coordinates

    Returns
    -------
    coord_arr : Nat x 3 numpy array
        Array of the form [[x1,y1,z1],[x2,y2,z2],...]

    """
    nat = len(self)
    coord_arr = np.zeros((nat,3))
    for i,atom in enumerate(self):
        coord_arr[i][0] = atom.x
        coord_arr[i][1] = atom.y
        coord_arr[i][2] = atom.z
    return coord_arr

def calc_coord_array(self):
    """Set the coordinate array in geom_info"""
    self.geom_info.coord_array = self.coord_array()

def plane_coeffs(self):
    """
    Return numpy array of the plane coefficients which average the coords

    Returns
    -------
    plane_coeffs : length 4 numpy array
        Plane equation coefficients such that a point on the plane is:
        ax + by + cz + d = 0. The array is [a,b,c,d]

    """
    if self.geom_info.coord_array == None:
        self.calc_coord_array()
    plane_coeffs = ao.plane_from_coord(self.geom_info.coord_array)

    return plane_coeffs

def calc_plane_coeffs(self):
    """Set the plane coefficients in geom_info"""
    self.geom_info.plane_coeffs = self.plane_coeffs()

def axes(self):
    """
    Return principal, secondary and perpendicular axes of the Mol

    Returns
    -------
    axes_out : 3 x 3 np array
        Principal, followed by secondary and perpendicular axes of the molecule

    """
    if self.geom_info.plane_coeffs == None:
        self.calc_plane_coeffs()
    # get the quadrangle which best describes the coordinates (possibly a
    # triangle with the far point repeated twice)
    vertices = ao.quadrangle_from_coord(self.geom_info.coord_array)
    # get the embedded quadrangle vertices
    emb_vert = ao.embedded_vert(vertices)
    # get vectors from projected diagonals
    axes_out_raw = ao.project_quad_to_vectors(emb_vert,self.geom_info.plane_coeffs)
    # we want the first raw to be the secondary and vice versa and the principal
    # to be *(-1) in order to maintian a convention
    axes_out = [-axes_out_raw[1], axes_out_raw[0]]
    # get the perpendicular vector
    perp = np.cross(axes_out[0], axes_out[1])
    # ensure normalisation
    perp = perp/np.linalg.norm(perp)

    axes_out.append(perp)
    axes_out = np.array(axes_out)
    return axes_out

def calc_axes(self):
    """Set the principal and secondary axes in geom_info"""
    axes = self.axes()
    self.geom_info.prin_ax = axes[0]
    self.geom_info.sec_ax = axes[1]
    self.geom_info.perp_ax = axes[2]
