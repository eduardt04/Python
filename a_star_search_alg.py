from _operator import attrgetter


class Nod:
    def __init__(self, info, h):
        self.info = info
        self.h = h

    def __str__(self):
        return "({}, h={})".format(self.info, self.h)

    def __repr__(self):
        return f"({self.info}, h={self.h})"


class Arc:
    def __init__(self, capat, varf, cost):
        self.capat = capat
        self.varf = varf
        self.cost = cost


class Problema:
    def __init__(self):
        self.noduri = [
            Nod('a', float('inf')), Nod('b', 10),
            Nod('c', 3), Nod('d', 7), Nod('e', 8), Nod('f', 0), Nod('g', 14), Nod('i', 3), Nod('j', 1), Nod('k', 2)
        ]
        self.arce = [
            Arc('a', 'b', 3), Arc('a', 'c', 9), Arc('a', 'd', 7), Arc('b', 'f', 100), Arc('b', 'e', 4),
            Arc('c', 'e', 10), Arc('c', 'g', 6), Arc('d', 'i', 4), Arc('e', 'f', 8), Arc('e', 'c', 1),
            Arc('g', 'e', 7), Arc('i', 'k', 1), Arc('i', 'j', 2)
        ]
        self.nod_start = self.noduri[0]  # de tip Nod
        self.nod_scop = 'f'  # doar info (fara h)

    def cauta_nod_nume(self, info):
        for nod in self.noduri:
            if nod.info == info:
                return nod
        return None


class NodParcurgere:
    problema = None

    def __init__(self, nod_graf, parinte=None, g=0, f=None):
        self.nod_graf = nod_graf  # obiect de tip Nod
        self.parinte = parinte  # obiect de tip Nod
        self.g = g  # costul drumului de la radacina pana la nodul curent
        if f is None:
            self.f = self.g + self.nod_graf.h
        else:
            self.f = f

    def drum_arbore(self):
        nod_c = self
        drum = [nod_c]
        while nod_c.parinte is not None:
            drum = [nod_c.parinte] + drum
            nod_c = nod_c.parinte
        return drum

    def contine_in_drum(self, nod):
        return nod.nod_graf.info in [nod_p.nod_graf.info for nod_p in self.drum_arbore()]

    # se modifica in functie de problema
    def expandeaza(self):
        return list(set([(problema.cauta_nod_nume(arc.varf), arc.cost) for arc in problema.arce
                         if arc.capat == self.nod_graf.info]))

    # se modifica in functie de problema
    def test_scop(self):
        return self.nod_graf.info == self.problema.nod_scop

    def __str__(self):
        parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"


def str_info_noduri(l):
    sir = "["
    for x in l:
        sir += str(x) + "  "
    sir += "]"
    return sir


def afis_succesori_cost(l):
    sir = ""
    for (x, cost) in l:
        sir += "\nnod: " + str(x) + ", cost arc:" + str(cost)
    return sir


def in_lista(l, nod):
    for i in range(len(l)):
        if l[i].nod_graf.info == nod.nod_graf.info:
            return l[i]
    return None


def a_star():
    rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
    open = [rad_arbore]  # open va contine elemente de tip NodParcurgere
    closed = []  # closed va contine elemente de tip NodParcurgere

    while len(open) > 0:
        print(str_info_noduri(open))  # afisam lista open
        nod_curent = open.pop(0)
        closed.append(nod_curent)

        if nod_curent.test_scop():
            break

        expandare = [NodParcurgere(nod_graf=nod, parinte=nod_curent, g=nod_curent.g + cost) for (nod, cost) in
                     nod_curent.expandeaza()]

        for s in expandare:
            if not nod_curent.contine_in_drum(s):
                node_open = in_lista(open, s)
                if node_open is not None and node_open.f > s.f:
                    open.remove(node_open)
                open.append(s)
                open = sorted(sorted(open, key=attrgetter('g'), reverse=True), key=attrgetter('f'))

    print("\n------------------ Concluzie -----------------------")
    if len(open) == 0:
        print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
    else:
        print("Drum de cost minim: " + str_info_noduri(nod_curent.drum_arbore()))


if __name__ == "__main__":
    problema = Problema()
    NodParcurgere.problema = problema
    a_star()
