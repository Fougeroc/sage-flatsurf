r""" 
Construction of Chamanara's surfaces which depend on a parameter alpha less than one.
See the paper "Affine automorphism groups of surfaces of infinite type" in which the surface 
is called $X_\alpha$.

EXAMPLES::

    sage: from flatsurf import translation_surfaces
    sage: s = translation_surfaces.chamanara(1/2)
    sage: s.plot()
    Graphics object consisting of 129 graphics primitives
"""

from flatsurf.geometry.surface import Surface
from flatsurf.geometry.half_dilation_surface import HalfDilationSurface
from sage.rings.integer_ring import ZZ

def ChamanaraPolygon(alpha):
    from sage.categories.fields import Fields
    field=alpha.parent()
    if not field in Fields():
        ValueError("The value of alpha must lie in a field.")
    if alpha<=0 or alpha>=1:
        ValueError("The value of alpha must be between zero and one.")
    # The value of x is $\sum_{n=0}^\infty \alpha^n$.
    x=1/(1-alpha)
    from flatsurf.geometry.polygon import polygons
    return polygons((1,0), (-x,x), (0,-1), (x-1,1-x))
#    pc=PolygonCreator(field=field)
#    pc.add_vertex((0,0))
#    pc.add_vertex((1,0))
#    pc.add_vertex((1-x,x))
#    pc.add_vertex((1-x,x-1))
#    return pc.get_polygon()

class ChamanaraSurface(Surface):
    r"""
    The ChamanaraSurface $X_{\alpha}$.
    
    EXAMPLES::

        sage: from flatsurf.geometry.chamanara import ChamanaraSurface
        sage: ChamanaraSurface(1/2)
        Chamanara surface with parameter 1/2
    """
    def __init__(self, alpha):
        self._p = ChamanaraPolygon(alpha)
        self._field = alpha.parent()
        self.rename('Chamanara surface with parameter {}'.format(alpha))
        Surface.__init__(self)
    
    def base_ring(self):
        return self._field
    
    def polygon_labels(self):
        return ZZ
        
    def polygon(self, lab):
        return self._p
    
    def is_finite(self):
        return False
    
    def opposite_edge(self, p, e):
        if e==0 or e==2:
            return 1-p,e
        elif e==1:
            if p<0:
                return p+1,3
            elif p>1:
                return p-1,3
            else:
                # p==0 or p==1
                return 1-p,1
        else:
            # e==3
            if p<=0:
                return p-1,1
            else:
                # p>=1
                return p+1,1

    def base_label(self):
        return ZZ(0)

def chamanara_half_dilation_surface(alpha, n=8):
    r"""
    Return Chamanara's surface thought of as a Half Dilation surface.
    """
    s=HalfDilationSurface(ChamanaraSurface(alpha))
    adjacencies = [(0,1)]
    for i in range(n):
        adjacencies.append((-i,3))
        adjacencies.append((i+1,3))
    s.graphical_surface(adjacencies=adjacencies)
    return s
    
def chamanara_surface(alpha,n=8):
    r"""
    Return Chamanara's surface thought of as a translation surface.
    """
    s = chamanara_half_dilation_surface(alpha).minimal_translation_cover()
    l = s.base_label()
    adjacencies = [(l,1)]
    for i in range(n):
        adjacencies.append((l,3))
        l = s.opposite_edge(l,3)[0]
    l = s.base_label()
    l = s.opposite_edge(l,1)[0]
    for i in range(n):
        adjacencies.append((l,3))
        l = s.opposite_edge(l,3)[0]
    s.graphical_surface(adjacencies=adjacencies)
    return s

