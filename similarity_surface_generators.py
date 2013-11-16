from sage.rings.integer_ring import ZZ
from sage.misc.cachefunc import cached_method

ZZ_1 = ZZ(1)
ZZ_2 = ZZ(2)

from similarity_surface import TranslationSurface_generic

class InfiniteStaircase(TranslationSurface_generic):
    r"""
    The infinite staircase.

     ...
     +--+--+
     |  |  |
     +--+--+--+
        |  |  |
        +--+--+--+
           |  |  |
           +--+--+--+
              |  |  |
              +--+--+
                  ...
    """
    def _repr_(self):
        r"""
        String representation.
        """
        return "The infinite staircase"

    def base_ring(self):
        r"""
        Return the rational field.
        """
        from sage.rings.rational_field import QQ
        return QQ

    def polygon(self, lab):
        r"""
        Return the polygon labeled by ``lab``.
        """
        if lab not in self.polygon_labels():
            raise ValueError("lab (=%s) not a valid label"%lab)
        from polygon import square
        return square()

    def polygon_labels(self):
        r"""
        The set of labels used for the polygons.
        """
        return ZZ

    def opposite_edge(self, p, e):
        r"""
        Return the pair ``(pp,ee)`` to which the edge ``(p,e)`` is glued to.
        """
        if (p+e) % 2:
            return p+1,(e+2)%4
        else:
            return p-1,(e+2)%4

class EInfinity(TranslationSurface_generic):
    r"""
    The surface based on the $E_\infinity$ graph.

     The biparite graph is shown below, with edges numbered:

      0   1   2  -2   3  -3   4  -4 
    *---o---*---o---*---o---*---o---*...
            |
            |-1
            o

    Here, black vertices are colored *, and white o. 
    Black nodes represent vertical cylinders and white nodes
    represent horizontal cylinders.
    """
    def __init__(self,lambda_squared=None, field=None):
        TranslationSurface_generic.__init__(self)
        if lambda_squared==None:
            from sage.rings.number_field.number_field import NumberField
            from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
            R=PolynomialRing(ZZ,'x')
            x = R.gen()
            from sage.rings.qqbar import AA
            self._field=NumberField(x**3-ZZ(5)*x**2+ZZ(4)*x-ZZ(1), 'r', embedding=AA(ZZ(4)))
            self._l=self._field.gen()
        else:
            if field is None:
                self._l=lambda_squared
                self._field=lambda_squared.parent()
            else:
                self._field=field
                self._l=field(lambda_squared)

    def _repr_(self):
        r"""
        String representation.
        """
        return "The E-infinity surface"

    def base_ring(self):
        r"""
        Return the rational field.
        """
        return self._field

    @cached_method
    def get_white(self,n):
        r"""Get the weight of the white endpoint of edge n."""
        l=self._l
        if n==0 or n==1:
            return l
        if n==-1:
            return l-1
        if n==2:
            return 1-3*l+l**2
        if n>2:
            x=self.get_white(n-1)
            y=self.get_black(n)
            return l*y-x
        return self.get_white(-n)

    @cached_method
    def get_black(self,n):
        r"""Get the weight of the black endpoint of edge n."""
        l=self._l
        if n==0:
            return self._field(1)
        if n==1 or n==-1 or n==2:
            return l-1
        if n>2:
            x=self.get_black(n-1)
            y=self.get_white(n-1)
            return y-x
        return self.get_black(1-n)

    def polygon(self, lab):
        r"""
        Return the polygon labeled by ``lab``.
        """
        if lab not in self.polygon_labels():
            raise ValueError("lab (=%s) not a valid label"%lab)
        from polygon import rectangle
        return rectangle(2*self.get_black(lab),self.get_white(lab))

    def polygon_labels(self):
        r"""
        The set of labels used for the polygons.
        """
        return ZZ

    def opposite_edge(self, p, e):
        r"""
        Return the pair ``(pp,ee)`` to which the edge ``(p,e)`` is glued to.
        """
        if p==0:
            if e==0:
                return (0,2)
            if e==1:
                return (1,3)
            if e==2:
                return (0,0)
            if e==3:
                return (1,1)
        if p==1:
            if e==0:
                return (-1,2)
            if e==1:
                return (0,3)
            if e==2:
                return (2,0)
            if e==3:
                return (0,1)
        if p==-1:
            if e==0:
                return (2,2)
            if e==1:
                return (-1,3)
            if e==2:
                return (1,0)
            if e==3:
                return (-1,1)
        if p==2:
            if e==0:
                return (1,2)
            if e==1:
                return (-2,3)
            if e==2:
                return (-1,0)
            if e==3:
                return (-2,1)
        if p>2:
            if e%2:
                return -p,(e+2)%4
            else:
                return 1-p,(e+2)%4
        else:
            if e%2:
                return -p,(e+2)%4
            else:
                return 1-p,(e+2)%4

class TFractal(TranslationSurface_generic):
    r"""
    The TFractal surface.

    The TFractal surface is a translation surface of finite area built from
    infinitely many polygons. The basic building block is the following polygon

     w/r    w     w/r
    +---+------+---+
    | 1 |   2  | 3 | h2
    +---+------+---+
        |   0  | h1
        +------+
            w

    where ``w``, ``h1``, ``h2``, ``r`` are some positive numbers. Default values
    are ``w=h1=h2=1`` and ``r=2``.

    .. TODO::

        In that surface, the linear flow can be computed more efficiently using
        only one affine interval exchange transformation with 5 intervals. But
        the underlying geometric construction is not a covering.
    """
    def __init__(self, w=ZZ_1, r=ZZ_2, h1=ZZ_1, h2=ZZ_1):
        from sage.structure.sequence import Sequence
        from sage.combinat.words.words import Words

        self._field = Sequence([w,r,h1,h2]).universe()
        if not self._field.is_field():
            self._field = self._field.fraction_field()
        self._w = self._field(w)
        self._r = self._field(r)
        self._h1 = self._field(h1)
        self._h2 = self._field(h2)
        self._words = Words('LR')

    def _repr_(self):
        return "The T-fractal surface with parameters w=%s, r=%s, h1=%s, h2=%s"%(
                self._w, self._r, self._h1, self._h2)

    def base_ring(self):
        return self._field

    def polygon_labels(self):
        from sage.combinat.words.words import Words
        from sage.sets.finite_enumerated_set import FiniteEnumeratedSet
        from cartesian_product import CartesianProduct # custom cartesian product

        return CartesianProduct([self._words, FiniteEnumeratedSet([0,1,2,3])])

    def opposite_edge(self, p, e):
        r"""
         w/r         w/r
        +---+------+---+
        | 1 |  2   | 3 |
        |   |      |   |  h2
        +---+------+---+
            |  0   | h1
            +------+
            w
        """
        w,i = p
        if i == 0:
            if e == 0:
                if w.is_empty():   return (w,2),2
                elif w[-1] == 'L': return (w[:-1],1),2
                elif w[-1] == 'R': return (w[:-1],3),2
            if e == 1: return (w,0),3
            if e == 2: return (w,2),0
            if e == 3: return (w,0),1
        if i == 1:
            if e == 0: return (w + self._words('L'), 2), 2
            if e == 1: return (w,2),3
            if e == 2: return (w + self._words('L'), 0), 0
            if e == 3: return (w,3), 1
        if i == 2:
            if e == 0: return (w,0),2
            if e == 1: return (w,3),3
            if e == 2:
                if w.is_empty():   return (w,0),0
                elif w[-1] == 'L': return (w[:-1],1),0
                elif w[-1] == 'R': return (w[:-1],3),0
            if e == 3: return (w,1),1
        if i == 3:
            if e == 0: return (w + self._words('R'), 2), 2
            if e == 1: return (w,1),3
            if e == 2: return (w + self._words('R'), 0), 0
            if e == 3: return (w,2),1


    def polygon(self, lab):
        r"""
        Return the polygon with label ``lab``.
         w/r         w/r
        +---+------+---+
        | 1 |  2   | 3 |
        |   |      |   |  h2
        +---+------+---+
            |  0   | h1
            +------+
            w
        """
        return (1 / self._r ** w.length()) * self._base_polygon(lab[1])

    @cached_method
    def _base_polygon(self, i):
        from polygon import Polygons
        if i == 0:
            w = self._w
            h = self._h1
        if i == 1 or i == 3:
            w = self._w / self._r
            h = self._h2
        if i == 2:
            w = self._w
            h = self._h2
        return Polygons(self.base_ring())([(w,0),(0,h),(-w,0),(0,-h)])

    def base_label(self):
        return (self._words(''), 0)


class SimilaritySurfaceGenerators:
    r"""
    Examples of similarity surfaces.
    """
    @staticmethod
    def example():
        r"""
        Construct a SimilaritySurface from a pair of triangles.
        """
        from similarity_surface import SimilaritySurface_polygons_and_gluings
        from polygon import PolygonCreator
        pc=PolygonCreator()
        pc.add_vertex((0,0))
        pc.add_vertex((2,-2))
        pc.add_vertex((2,0))
        p0=pc.get_polygon()
        pc=PolygonCreator()
        pc.add_vertex((0,0))
        pc.add_vertex((2,0))
        pc.add_vertex((1,3))
        p1=pc.get_polygon()
        ps=(p0,p1)
        glue={ (0,2):(1,0), (0,0):(1,1), (0,1):(1,2), (1,0):(0,2), (1,1):(0,0), (1,2):(0,1) }
        return SimilaritySurface_polygons_and_gluings(ps,glue)


    @staticmethod
    def right_angle_triangle(w,h):
        from sage.structure.sequence import Sequence
        from polygon import Polygons
        from sage.modules.free_module import VectorSpace
        from similarity_surface import SimilaritySurface_polygons_and_gluings

        F = Sequence([w,h]).universe()
        if not F.is_field():
            F = F.fraction_field()
        V = VectorSpace(F,2)
        P1 = Polygons(F)([V((w,0)),V((-w,h)),V((0,-h))])
        P2 = Polygons(F)([V((0,h)),V((-w,-h)),V((w,0))])
        ps = (P1,P2)
        glue = {(0,0):(1,2),(0,1):(1,1),(0,2):(1,0)}
        return SimilaritySurface_polygons_and_gluings(ps,glue)

class TranslationSurfaceGenerators:
    r"""
    Common and less common translation surfaces.
    """
    @staticmethod
    def regular_octagon():
        r"""
        Return the translation surface built from the regular octagon by
        identifying opposite sides.

        EXAMPLES::

            sage: T = translation_surfaces.regular_octagon()
            sage: T
            Translation surface built from the regular octagon
            sage: T.stratum()
            H_2(2)
        """
        from polygon import regular_octagon
        from similarity_surface import TranslationSurface_polygons_and_gluings
        polygons = [regular_octagon()]
        identifications = {}
        identifications.update(dict(((0,i),(0,i+4)) for i in xrange(4)))
        return TranslationSurface_polygons_and_gluings(polygons=polygons, identifications=identifications)

    @staticmethod
    def octagon_and_squares():
        from polygon import square, regular_octagon
        from sage.matrix.matrix_space import MatrixSpace
        from similarity_surface import TranslationSurface_polygons_and_gluings

        o = regular_octagon()
        K = o.parent().field()
        sqrt2 = K.gen()
        rot = MatrixSpace(K,2)([[sqrt2/ZZ_2,-sqrt2/ZZ_2],[sqrt2/ZZ_2,sqrt2/ZZ_2]])
        polygons = [regular_octagon(), ZZ_2*square(K), ZZ_2*rot*square(K)]
        identifications = {
            (0,0): (1,3),
            (0,1): (2,3),
            (0,2): (1,0),
            (0,3): (2,0),
            (0,4): (1,1),
            (0,5): (2,1),
            (0,6): (1,2),
            (0,7): (2,2),
            }
        return TranslationSurface_polygons_and_gluings(polygons=polygons, identifications=identifications)

    @staticmethod
    def origami(r,u,rr=None,uu=None,domain=None):
        r"""
        Return the origami defined by the permutations ``r`` and ``u``.

        EXAMPLES::

            sage: S = SymmetricGroup(3)
            sage: r = S('(1,2)')
            sage: u = S('(1,3)')
            sage: o = translation_surfaces.origami(r,u)
            sage: o
            Origami defined by r=(1,2) and u=(1,3)
            sage: o.stratum()
            H_2(2)
        """
        from similarity_surface import Origami
        return Origami(r,u,rr,uu,domain)


    @staticmethod
    def infinite_staircase1():
        return InfiniteStaircase()

    @staticmethod
    def infinite_staircase2():
        from similarity_surface import Origami
        return Origami(
                lambda x: x+1 if x%2 else x-1,  # r  (edge 1)
                lambda x: x-1 if x%2 else x+1,  # u  (edge 2)
                lambda x: x+1 if x%2 else x-1,  # rr (edge 3)
                lambda x: x-1 if x%2 else x+1,  # uu (edge 0)
                domain = ZZ)

    @staticmethod
    def t_fractal(w=ZZ_1, r=ZZ_2, h1=ZZ_1, h2=ZZ_1):
        return TFractal(w,r,h1,h2)