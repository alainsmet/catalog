#!/usr/bin/env python3

# Proiect catalog - Alain Smet - 22/03/2020

import os
import operator

# Definitia clasei catalog


class catalog:
    lista_obiecte = []  # Lista cu toate produsele adaugate
    __moneda = 'RON'
    __unitate_dist = 'cm'
    __unitate_turatie = 'rpm'
    __unitate_consum = 'W'
    __unitate_volum = 'L'

    def __init__(self, pret=0., consum=0., producator='', cod_produs='',
                 stoc=0):
        self.pret = pret
        self.consum = consum
        self.producator = producator
        self.cod_produs = cod_produs
        self.stoc = stoc
        self.clasa = ''
        self.subclasa = ''

    def creare_produs(self):
        """Metoda care permite introducerea valorilor intr-un mod mai 'sigur'
           cu o verificare de informatii"""
        self.input_valoare('cod_produs', 'Introdu noul cod produs : ', '')
        self.input_valoare('producator', 'Introdu producatorul : ',
                           'nu este un nume valid')
        self.input_valoare('pret',
                           f'Introdu pretul produsului ({self.__moneda}) : ',
                           'nu este un pret valid')
        self.input_valoare('consum',
                           'Introdu consumul produsului '
                           f'({self.__unitate_consum}) : ',
                           'nu este un consum valid')
        self.input_valoare('stoc', 'Introdu stocul disponibil : ',
                           'nu este un numar valid')

    def input_valoare(self, carac, text_input, text_eroare, skip=False):
        """Metoda de baza care cere o valoare de la utilizator. Skip = True
           permite sa nu modifice valoarea in cazul in care primeste un sir
           gol."""
        while True:
            val_brut = input(text_input)
            if carac == 'cod_produs':
                if val_brut == '' and skip is True:
                    break
                elif val_brut == '':
                    print('Codul produs nu poate fi nul')
                elif len(self.cautare_produs('cod_produs', val_brut)) > 0:
                    print(f'Referinta {val_brut} exista deja pentru un alt '
                          'produs. Referinta trebuie sa fie unica.')
                else:
                    setattr(self, carac, val_brut)
                    break
            else:
                if val_brut == '' and skip is True:
                    break
                val = self.verif_valoare(carac, val_brut)
                if val is not None:
                    setattr(self, carac, val)
                    break
                else:
                    print(f'{val_brut} ' + text_eroare)

    def incarcare_valoare(self, carac, valoare):
        """Permite setarea unei variabile doar daca valoarea corespunde cu
           tipul variabilei"""
        if carac == 'cod_produs':
            if valoare == '' or \
               len(self.cautare_produs('cod_produs', valoare)) > 0:
                return False
            else:
                setattr(self, carac, valoare)
                return True
        else:
            val = self.verif_valoare(carac, valoare)
            if val is not None:
                setattr(self, carac, val)
                return True
            else:
                return False

    def num_obiecte(self):
        """Returneaza numarul de produse continute in catalog"""
        return len(catalog.lista_obiecte)

    def cautare_produs(self, carac, sir_cautare, strict=True, lista_cautare=[],
                       op_filtru='='):
        """Returneaza o lista cu toate produsele la care caracteristica <carac>
           corespunde cu valoarea cautata <sir_cautare>"""
        if lista_cautare == []:
            lista_cautare = catalog.lista_obiecte
        lista_rezultate = []
        lista_sir_cautare = str(sir_cautare).split(',')
        for e in lista_cautare:
            if hasattr(e, carac):
                attr_val = getattr(e, carac)
                if strict is True:
                    if str(attr_val) in lista_sir_cautare:
                        lista_rezultate.append(e)
                else:
                    find_count = 0
                    for sir in lista_sir_cautare:
                        if op_filtru == '=':
                            try:
                                if type(attr_val) is int:
                                    if attr_val == int(sir):
                                        find_count += 1
                                elif type(attr_val) is float:
                                    if attr_val == float(sir):
                                        find_count += 1
                                elif str(attr_val).lower() \
                                     .find(sir.lower()) > -1:
                                    find_count += 1
                            except:
                                pass
                        elif op_filtru == '!=':
                            try:
                                if type(attr_val) is int:
                                    if attr_val != int(sir):
                                        find_count += 1
                                elif type(attr_val) is float:
                                    if attr_val != float(sir):
                                        find_count += 1
                                elif str(attr_val).lower() \
                                     .find(sir.lower()) == -1:
                                    find_count += 1
                            except:
                                pass
                        elif op_filtru == '>':
                            try:
                                if type(attr_val) is int:
                                    if attr_val > int(sir):
                                        find_count += 1
                                elif type(attr_val) is float:
                                    if attr_val > float(sir):
                                        find_count += 1
                            except:
                                pass
                        elif op_filtru == '>=':
                            try:
                                if type(attr_val) is int:
                                    if attr_val >= int(sir):
                                        find_count += 1
                                elif type(attr_val) is float:
                                    if attr_val >= float(sir):
                                        find_count += 1
                            except:
                                pass
                        elif op_filtru == '<':
                            try:
                                if type(attr_val) is int:
                                    if attr_val < int(sir):
                                        find_count += 1
                                elif type(attr_val) is float:
                                    if attr_val < float(sir):
                                        find_count += 1
                            except:
                                pass
                        elif op_filtru == '<=':
                            try:
                                if type(attr_val) is int:
                                    if attr_val <= int(sir):
                                        find_count += 1
                                elif type(attr_val) is float:
                                    if attr_val <= float(sir):
                                        find_count += 1
                            except:
                                pass
                    if find_count > 0:
                        lista_rezultate.append(e)
        return lista_rezultate

    def lista_ord(self, carac, lista='', invers=False):
        """Returneaza o lista cu produsele ordonate dupa o caracteristica
           (pret, consum, ...). Daca <invers> == False, ordonate de la cel mai
           mic pana la cel mai mare."""
        lista_rezultate = []
        lista_sort = []
        # Lista care stocheaza tipurile pentru fiecare caracteristica
        lista_format = [str for x in range(len(carac))]
        if lista != '':
            for i, el in enumerate(lista):
                lista_interm = [i]
                for j, c in enumerate(carac):
                    if hasattr(el, c):
                        attr_val = getattr(el, c)
                        tip_val = type(attr_val)
                        lista_interm.append(attr_val)
                        if tip_val is not lista_format[j]:
                            lista_format[j] = tip_val
                            if len(lista_sort) > 1:
                                # Cand gasim prima valoare cu un tip diferit,
                                # incercam sa modificam valorile de inainte, ca
                                # sa nu ciclam din nou pe toata lista.
                                for a in range(i+1):
                                    print(a, len(lista_sort))
                                    if type(lista_sort[a][j+1]) is not tip_val:
                                        if tip_val is float:
                                            lista_sort[a][j+1] = 0.
                                        elif tip_val is int:
                                            lista_sort[a][j+1] = 0
                                        else:
                                            lista_sort[a][j+1] = ''
                    else:
                        if lista_format[j] is float:
                            lista_interm.append(0.)
                        elif lista_format[j] is int:
                            lista_interm.append(0)
                        else:
                            lista_interm.append('')
                lista_sort.append(lista_interm)
            lista_sort = sorted(lista_sort, key=lambda x: x[1:],
                                reverse=invers)
            for el in lista_sort:
                lista_rezultate.append(lista[el[0]])
        return lista_rezultate

    def verif_valoare(self, carac, valoare):
        """Verifica daca valoarea introdusa <valoare> corespunde tipului de
           date pentru caracteristica <carac>"""
        if carac in self.__dict__:
            tip_carac = type(getattr(self, carac))
            if tip_carac is int:
                try:
                    val = int(valoare)
                    if val < 0:
                        return None
                    return val
                except:
                    return None
            elif tip_carac is float:
                try:
                    val = float(valoare)
                    if val < 0:
                        return None
                    return val
                except:
                    return None
            elif tip_carac is str:
                return valoare
            else:
                return None
        else:
            return None

    def print_catalog(self, carac=[], filtru=[], carac_filtru=[],
                      op_filtru=[], sort=[], invers=False):
        """Listeaza catalogul de produse, si permite sa filtreze si sa
           sorteze"""
        lista_rezultate = catalog.lista_obiecte
        sir_e = 'Catalog complet de produse disponibile'
        dict_operator = {'=': 'contine',
                         '>': 'mai mare decat',
                         '>=': 'mai mare sau egal decat',
                         '<': 'mai mic decat',
                         '<=': 'mai mic sau egal decat',
                         '!=': 'nu contine'}
        if carac_filtru != [] and filtru != []:
            sir_e = 'Extras din catalog, unde '
            for n in range(len(filtru)):
                lista_rezultate = self.cautare_produs(carac_filtru[n],
                                                      filtru[n], False,
                                                      lista_rezultate,
                                                      op_filtru[n])
                if n == 0:
                    sir_e += f'{carac_filtru[n]} ' \
                             f'{dict_operator[op_filtru[n]]} ' \
                             f'{filtru[n].replace(",", " sau ")}'
                else:
                    sir_e += f' si {carac_filtru[n]} ' \
                             f'{dict_operator[op_filtru[n]]} ' \
                             f'{filtru[n].replace(",", " sau ")}'
        if sort != []:
            lista_rezultate = self.lista_ord(carac=sort, lista=lista_rezultate,
                                             invers=invers)
            sir_e += ', sortat dupa '
            for n in range(len(sort)):
                if n == 0:
                    sir_e += f'{sort[n]} '
                else:
                    sir_e += f'si {sort[n]} '
            if invers is False:
                sir_e += 'ascendent'
            else:
                sir_e += 'descendent'
        if carac != []:
            offset = 5
            latime_col = [len(carac[x]) for x in range(len(carac))]
            for e in lista_rezultate:
                for c in range(len(carac)):
                    if hasattr(e, carac[c]):
                        if len(str(getattr(e, carac[c]))) > latime_col[c]:
                            latime_col[c] = len(str(getattr(e, carac[c])))
            sep_linie = ''
            for l in latime_col:
                sep_linie += '='*(l + offset + 2) + '+'
            sep_linie = sep_linie[1:-1]

            print(sir_e, '\n')
            print(sep_linie)
            sir_e = ''
            for c in range(len(carac)):
                sir_e += carac[c].replace('_', ' ').capitalize(). \
                         ljust(latime_col[c] + offset) + ' | '
            sir_e = sir_e[:-3]
            print(sir_e)
            print(sep_linie)
            for e in lista_rezultate:
                sir_e = ''
                for c in range(len(carac)):
                    if hasattr(e, carac[c]):
                        sir_e += str(getattr(e, carac[c])). \
                                 ljust(latime_col[c] + offset) + " | "
                    else:
                        sir_e += ''.ljust(latime_col[c] + offset) + " | "
                sir_e = sir_e[:-3]
                print(sir_e)
            print(sep_linie)

            print('\n', f'Total produse : {len(lista_rezultate)} din '
                  f'{len(catalog.lista_obiecte)}', sep='')


class Electrocasnice_mari(catalog):
    def __init__(self, pret=0., consum=0., producator='', cod_produs='',
                 adancime=0., latime=0., inaltime=0., stoc=0):
        catalog.__init__(self, pret, consum, producator, cod_produs, stoc)
        self.clasa = '<<Electrocasnice mari>>'
        self.adancime = adancime
        self.latime = latime
        self.inaltime = inaltime

    def creare_produs(self):
        """Metoda care permite introducerea valorilor intr-un mod mai 'sigur'
           cu o verificare de informatii"""
        catalog.creare_produs(self)
        self.input_valoare('adancime', 'Introdu adancimea '
                           f'({catalog._catalog__unitate_dist}) : ',
                           'nu este o valoare valida')
        self.input_valoare('latime', 'Introdu latimea '
                           f'({catalog._catalog__unitate_dist}) : ',
                           'nu este o valoare valida')
        self.input_valoare('inaltime', 'Introdu inaltimea '
                           f'({catalog._catalog__unitate_dist}) : ',
                           'nu este o valoare valida')


class Electrocasnice_mici(catalog):
    def __init__(self, pret=0., consum=0., producator='', cod_produs='',
                 lungime_cablu=0., baterie='Nu', stoc=0):
        catalog.__init__(self, pret, consum, producator, cod_produs, stoc)
        self.clasa = '<<Electrocasnice mici>>'
        self.lungime_cablu = lungime_cablu
        self.baterie = baterie

    def creare_produs(self):
        """Metoda care permite introducerea valorilor intr-un mod mai 'sigur'
           cu o verificare de informatii"""
        catalog.creare_produs(self)
        self.input_valoare('lungime_cablu', 'Introdu lungimea cablului '
                           f'({catalog._catalog__unitate_dist}) : ',
                           'nu este o valoare valida')
        self.input_valoare('baterie', f'Introdu informatii despre baterie : ',
                           'nu este o valoare valida')


class Frigider(Electrocasnice_mari):
    def __init__(self, pret=0., consum=0., producator='', cod_produs='',
                 adancime=0., latime=0., inaltime=0., capacitate_congelator=0.,
                 capacitate_frigider=0., stoc=0):
        Electrocasnice_mari.__init__(self, pret, consum, producator,
                                     cod_produs, adancime, latime, inaltime,
                                     stoc)
        catalog.lista_obiecte.append(self)
        self.subclasa = '<<Frigider>>'
        self.capacitate_congelator = capacitate_congelator
        self.capacitate_frigider = capacitate_frigider

    def __str__(self):
        ret_string = f'{self.subclasa.strip("<>")} marca : ' \
                     f'{self.producator}, cod produs : {self.cod_produs}' \
                     f'\nPret : {self.pret} {catalog._catalog__moneda}\n' \
                     f'Consum : {self.consum} ' \
                     f'{catalog._catalog__unitate_consum}, Dimensiuni ' \
                     f'(A x L x I) : {self.adancime} x {self.latime} x ' \
                     f'{self.inaltime} ({catalog._catalog__unitate_dist})\n' \
                     f'Capacitate : frigider {self.capacitate_frigider} ' \
                     f'{catalog._catalog__unitate_volum} - congelator ' \
                     f'{self.capacitate_congelator} ' \
                     f'{catalog._catalog__unitate_volum}\n' \
                     f'Stoc : {self.stoc}'
        return ret_string

    def creare_produs(self):
        """Metoda care permite introducerea valorilor intr-un mod mai 'sigur'
           cu o verificare de informatii"""
        Electrocasnice_mari.creare_produs(self)
        self.input_valoare('capacitate_congelator',
                           'Introdu capacitatea congelatorului '
                           f'({catalog._catalog__unitate_volum}) : ',
                           'nu este o valoare valida')
        self.input_valoare('capacitate_frigider',
                           'Introdu capacitatea frigiderului '
                           f'({catalog._catalog__unitate_volum}) : ',
                           'nu este o valoare valida')


class Aragaz(Electrocasnice_mari):
    def __init__(self, pret=0., consum=0., producator='', cod_produs='',
                 adancime=0., latime=0., inaltime=0., nr_arzatoare=0, stoc=0):
        Electrocasnice_mari.__init__(self, pret, consum, producator,
                                     cod_produs, adancime, latime,
                                     inaltime, stoc)
        catalog.lista_obiecte.append(self)
        self.subclasa = '<<Aragaz>>'
        self.nr_arzatoare = nr_arzatoare

    def __str__(self):
        ret_string = f'{self.subclasa.strip("<>")} marca : ' \
                     f'{self.producator}, cod produs : {self.cod_produs}\n' \
                     f'Pret : {self.pret} {catalog._catalog__moneda}\n' \
                     f'Consum : {self.consum} ' \
                     f'{catalog._catalog__unitate_consum}, Dimensiuni ' \
                     f'(A x L x I) : {self.adancime} x {self.latime} x ' \
                     f'{self.inaltime} ({catalog._catalog__unitate_dist})\n' \
                     f'Numar arzatoare : {self.nr_arzatoare}\n' \
                     f'Stoc : {self.stoc}'
        return ret_string

    def creare_produs(self):
        """Metoda care permite introducerea valorilor intr-un mod mai 'sigur'
           cu o verificare de informatii"""
        Electrocasnice_mari.creare_produs(self)
        self.input_valoare('nr_arzatoare', f'Introdu numarul de arzatoare : ',
                           'nu este o valoare valida')


class Mixer(Electrocasnice_mici):
    def __init__(self, pret=0., consum=0., producator='', cod_produs='',
                 lungime_cablu=0., baterie='Nu', rotatii_min=0, stoc=0):
        Electrocasnice_mici.__init__(self, pret, consum, producator,
                                     cod_produs, lungime_cablu, baterie, stoc)
        catalog.lista_obiecte.append(self)
        self.subclasa = '<<Mixer>>'
        self.rotatii_min = rotatii_min

    def __str__(self):
        ret_string = f'{self.subclasa.strip("<>")} marca : {self.producator}' \
                     f', cod produs : {self.cod_produs}\nPret : {self.pret} ' \
                     f'{catalog._catalog__moneda}\nConsum : {self.consum} ' \
                     f'{catalog._catalog__unitate_consum}, Lungime cablu : ' \
                     f'{self.lungime_cablu} ' \
                     f'{catalog._catalog__unitate_dist}\n' \
                     f'Baterie: {self.baterie}, Rotatii pe min : ' \
                     f'{self.rotatii_min} ' \
                     f'{catalog._catalog__unitate_turatie}\nStoc : {self.stoc}'
        return ret_string

    def creare_produs(self):
        """Metoda care permite introducerea valorilor intr-un mod mai 'sigur'
           cu o verificare de informatii"""
        Electrocasnice_mici.creare_produs(self)
        self.input_valoare('rotatii_min', 'Introdu viteza de rotatie '
                           f'({catalog._catalog__unitate_turatie}) : ',
                           'nu este o valoare valida')


class Fier_calcat(Electrocasnice_mici):
    def __init__(self, pret=0., consum=0., producator='', cod_produs='',
                 lungime_cablu=0., baterie='Nu', rezervor=0., stoc=0):
        Electrocasnice_mici.__init__(self, pret, consum, producator,
                                     cod_produs, lungime_cablu, baterie, stoc)
        catalog.lista_obiecte.append(self)
        self.subclasa = '<<Fier calcat>>'
        self.rezervor = rezervor

    def __str__(self):
        ret_string = f'{self.subclasa.strip("<>")} marca : ' \
                     f'{self.producator}, cod produs : {self.cod_produs}\n' \
                     f'Pret : {self.pret} {catalog._catalog__moneda}\n' \
                     f'Consum : {self.consum} ' \
                     f'{catalog._catalog__unitate_consum}, Lungime cablu : ' \
                     f'{self.lungime_cablu} ' \
                     f'{catalog._catalog__unitate_dist}\nBaterie: ' \
                     f'{self.baterie}, Rezervor : {self.rezervor} ' \
                     f'{catalog._catalog__unitate_volum}\nStoc : {self.stoc}'
        return ret_string

    def creare_produs(self):
        """Metoda care permite introducerea valorilor intr-un mod mai 'sigur'
           cu o verificare de informatii"""
        Electrocasnice_mici.creare_produs(self)
        self.input_valoare('rezervor', 'Introdu volumul rezervorului '
                           f'({catalog._catalog__unitate_volum}) : ',
                           'nu este o valoare valida')

if __name__ == '__main__':

    import sys
    import inspect

    def lista_tip_produs():
        """Genereaza o lista cu tipurile de produse disponibile (doar subclase
           cu superclasa catalog fara subclase, de exemplu aragaz,
           frigider, ..."""
        clase_dispo = inspect.getmembers(sys.modules[__name__],
                                         inspect.isclass)
        lista_produse = []
        for c in clase_dispo:
            if issubclass(c[1], catalog):
                num_subclase = 0
                for subclasa in clase_dispo:
                    if issubclass(subclasa[1], c[1]):
                        num_subclase += 1
                if num_subclase == 1:
                    lista_produse.append(c)
        return lista_produse

    def print_ajutor():
        print('Lista de comenzi disponibile :',
              'add : adauga un produs in catalog - add <tip produs>',
              'del : sterge un produs din catalog - del <cod produs>',
              'edit : modifica informatiile despre un produs - edit '
              '<cod produs> <carac de editat>', 'exit : iesire din catalog',
              'help : listeaza comenzile disponibile', 'info : '
              'informatie despre un produs - info <cod produs>',
              'list : listeaza produsele din catalog',
              'load : incarca un alt catalog - load <cale catalog>',
              'options : modifica optiunile din aplicatie',
              'save : salveaza datele intr-un fisier csv - save <cale catalog>'
              ' - save : salveaza in fisier de baza', sep='\n')

    def split_comanda(sir_brut):
        """Returneaza o lista de parametri, asa cum trebuie :)"""
        strip_sir_brut = sir_brut.strip()
        temp_sir = ''
        comentariu_flag = False
        comentariu_chars = ['\"', '\'']
        comanda = []

        for char in strip_sir_brut:
            if char == ' ' and comentariu_flag is False:
                temp_sir = temp_sir.strip('\"')
                temp_sir = temp_sir.strip('\'')
                comanda.append(temp_sir)
                temp_sir = ''
            elif char == ' ' and comentariu_flag is True:
                temp_sir += char
            elif char in comentariu_chars:
                comentariu_flag = not comentariu_flag
                temp_sir += char
            else:
                temp_sir += char

        temp_sir = temp_sir.strip('\"')
        temp_sir = temp_sir.strip('\'')
        comanda.append(temp_sir)
        return comanda

    def incarcare_catalog(cale='catalog.csv'):
        """Incarca datele de un fisier csv existent"""
        try:
            catalog_csv = open(cale, 'r')
        except:
            return False
        catalog.lista_obiecte = []
        global lista_parametri, lista_valori_initiale, lista_coloane
        lista_parametri = []
        lista_valori_initiale = []
        lista_coloane = []
        lista_produse = lista_tip_produs()
        while True:
            linie = catalog_csv.readline().strip()
            lista_linie = linie.split(';')
            if linie != '':
                if lista_linie[0] == '[nume-magazin]':
                    global nume_magazin
                    nume_magazin = lista_linie[1]
                elif lista_linie[0] == '[parametri]':
                    lista_parametri = lista_linie[:]
                elif lista_linie[0] == '[lista-coloane]':
                    for coloana in lista_linie[1:]:
                        if coloana != '':
                            lista_coloane.append(coloana)
                elif lista_linie[0] == '[valori-initiale]':
                    lista_valori_initiale = lista_linie[1:]
                elif lista_linie[0] == '[debut-date]':
                    while True:
                        linie = catalog_csv.readline().strip()
                        lista_linie = linie.split(';')
                        if linie != '' and lista_linie[0] != '[sfarsit-date]':
                            if lista_parametri != []:
                                obiect = None
                                for n in range(len(lista_parametri)):
                                    if n == 0:
                                        if lista_linie[n] \
                                           in (lista_produse[x][0]
                                               for x in range(len(lista_produse))):
                                            for produs in lista_produse:
                                                if lista_linie[n] == produs[0]:
                                                    obiect = produs[1]()
                                    else:
                                        if hasattr(obiect, lista_parametri[n]):
                                            test = obiect.incarcare_valoare(lista_parametri[n],
                                                                            lista_linie[n])
                                            if test is False and \
                                               lista_parametri[n] == cod_produs:
                                                catalog.lista_obiecte.remove(obiect)
                                                break

                        else:
                            break
            else:
                break
        catalog_csv.close()
        return True

    def salvare_catalog(cale='catalog.csv'):
        """Salveaza datele intr-un fisier csv"""
        try:
            catalog_csv = open(cale, 'w')
        except:
            return False
        global lista_coloane, fisier_catalog, nume_magazin
        global lista_parametri, lista_valori_initiale
        catalog_csv.write(f'[nume-magazin];{nume_magazin}\n')
        catalog_csv.write('[lista-coloane]')
        for coloana in lista_coloane:
            catalog_csv.write(f';{coloana}')
        catalog_csv.write('\n[parametri]')
        for param in lista_parametri[1:]:
            catalog_csv.write(f';{param}')
        catalog_csv.write('\n[valori-initiale]')
        for val in lista_valori_initiale:
            catalog_csv.write(f';{val}')
        catalog_csv.write('\n[debut-date]\n')
        for produs in catalog.lista_obiecte:
            catalog_csv.write(f'{produs.__class__.__name__}')
            for param in lista_parametri[1:]:
                if hasattr(produs, param):
                    catalog_csv.write(f';{getattr(produs,param)}')
                else:
                    catalog_csv.write(';')
            catalog_csv.write('\n')
        catalog_csv.write('[sfarsit-date];\n')
        catalog_csv.close()
        return True

    # Pregatirea variabilelor

    global cat, lista_coloane, fisier_catalog, nume_magazin
    global lista_parametri, lista_valori_initiale
    cat = catalog()
    lista_coloane = []
    fisier_catalog = 'catalog.csv'
    nume_magazin = ''
    lista_parametri = []
    lista_valori_initiale = []
    incarcare_catalog(fisier_catalog)
    if nume_magazin == '':
        nume_magazin = input('Intra numele magazinului : ')
    if lista_coloane == []:
        lista_coloane = ['cod_produs', 'subclasa', 'producator', 'pret',
                         'consum', 'stoc']
    if lista_parametri == []:
        lista_parametri = ['cod_produs', 'producator', 'pret', 'consum',
                           'stoc', 'adancime', 'latime', 'inaltime',
                           'lungime_cablu', 'baterie', 'capacitate_congelator',
                           'capacitate_frigider', 'nr_arzatoare',
                           'rotatii_min', 'rezervor', 'clasa', 'subclasa']
    if lista_valori_initiale == []:
        lista_valori_initiale = ['', '', 0., 0., 0, 0., 0., 0., 0., '', 0., 0.,
                                 0, 0., 0., '', '']

    # Program principal

    print(f'Bine ai venit la catalog de produse {nume_magazin}\n')
    print_ajutor()
    print()
    while True:
        sir_brut = input(f'Catalog {nume_magazin} > ')
        comanda = split_comanda(sir_brut)
        if comanda[0] != '':
            cuvant_cheie = comanda[0].lower()
            if cuvant_cheie == 'exit':

                # Permite iesirea din aplicatie. Datele pot fi salvate inainte
                # de a inchide programul.
                # Salveaza datele in fisierul retinut in variabila
                # fisier_catalog

                while True:
                    resp = input('Doresti sa salvezi datele in fisierul '
                                 f'{os.path.basename(fisier_catalog)} inainte '
                                 'de a iesi (Y/N) ? ')
                    if resp.lower() in ['y', 'n']:
                        if resp.lower() == 'y':
                            while True:
                                valid = salvare_catalog(fisier_catalog)
                                if valid is False:
                                    resp = input('A fost o problema cu '
                                                 'scrierea datelor in fisier '
                                                 f'{os.path.basename(fisier_catalog)}. '
                                                 'Doresti sa reincerci '
                                                 '(Y/N) ? ')
                                    if resp.lower() in ['y', 'n']:
                                        if resp.lower() == 'n':
                                            break
                                else:
                                    break
                        break
                break
            elif cuvant_cheie == 'help':
                print_ajutor()
            elif cuvant_cheie == 'add':

                # Adauga un produs in catalog. Sintaxa este : add <tip produs>
                # Un tip de produs corespunde unei clase mostenite din clasa
                # catalog care nu are subclase
                # Aceasta lista este obtinuta prin functia lista_tip_produs()

                lista_produse = lista_tip_produs()
                if len(comanda) > 1:
                    if comanda[1].capitalize() in \
                       (lista_produse[x][0] for x in range(len(lista_produse))):
                        for produs in lista_produse:
                            if comanda[1].capitalize() == produs[0]:
                                nou_produs = produs[1]()
                                nou_produs.creare_produs()
                    else:
                        print(f'{comanda[1].capitalize()} nu este un produs '
                              'valid. Urmatoarele produse sunt disponibile :')
                        for produs in lista_produse:
                            print(produs[0])
                else:
                    print('Trebuie sa introduci un tip de produs. Sintaxa '
                          'este : add <tip produs> . Urmatoarele tipuri de '
                          'produse sunt disponibile :')
                    for produs in lista_produse:
                        print(produs[0])
            elif cuvant_cheie == 'del':

                # Sterge un produs din catalog

                if len(comanda) > 1:
                    if comanda[1] == '*':
                        catalog.lista_obiecte = []
                        print('Toate produsele au fost sterse din catalog.')
                    else:
                        lista_produse = cat.cautare_produs('cod_produs',
                                                           comanda[1])
                        if len(lista_produse) > 0:
                            for produs_gasit in lista_produse:
                                for produs in catalog.lista_obiecte:
                                    if produs_gasit == produs:
                                        catalog.lista_obiecte.remove(produs)
                                        print(f'Produsul {comanda[1]} a fost '
                                              'sters din catalog.')
                        else:
                            print(f'Niciun produs cu codul {comanda[1]} nu a '
                                  'fost gasit in catalog. Introdu list pentru '
                                  'a lista produsele din catalog. Introdu : '
                                  'del * pentru a sterge toate produsele din '
                                  'catalog.')
                else:
                    print('Trebuie sa introduci un cod produs. Sintaxa este : '
                          'del <cod produs>, sau : del * pentru a sterge '
                          'toate produsele din catalog.')
            elif cuvant_cheie == 'list':

                # Listeaza produsele continute in baza de date. Poate accepta :
                #
                # * list : returneaza toate produsele
                # * list <carac><operator><valoare>
                #   returneaza o lista de produse care verifica criteriile.
                #   Operatori acceptati : =, <, >, <=, =>, !=
                #   De exemplu :
                #
                #   list producator=tefal
                #   va afisa toate produsele cu numele producatorului egal cu
                #   sau care contine tefal
                #
                #   list producator=bosch subclasa=mixer
                #   va afisa toate mixerele produse de bosch
                #
                #   list producator!=daewoo
                #   va afisa toate produsele care nu sunt fabricate de daewoo
                #
                #   list pret>500 pret<2000
                #   va afisa toate produsele cu un pret cuprins intre 500 si
                #   2000 RON
                #
                #   list pret>500 adancime>=70
                #   va afisa produsele cu un pret mai mare decat 500 lei si cu
                #   o adancime mai mare sau egala decat 70 cm
                #
                # * list sort=<carac> <desc>
                #   returneaza o lista sortata dupa una sau mai multe
                #   caracteristici
                #
                #   De exemplu :
                #   list sort=pret - va afisa toate produsele sortate dupa pret
                #   crescator
                #
                #   list sort=pret,adancime - va afisa toate produsele
                #   sortate dupa pret, si apoi dupa adancime, in ordinea
                #   crescatoare
                #
                #   list sort=pret desc - va afisa toate produsele sortate
                #   dupa pret descrescator
                #
                # Toate optiunile mentionate mai sus pot fi combinate,
                # de exemplu :
                #
                # list producator=tefal pret>500 pret<=2000 adancime=50
                # sort=pret desc
                #
                # va afisa toate produsele sortate dupa pret descrescator,
                # fabricate de tefal, cu un pret cuprins intre 500 si 2000 RON,
                # cu o adancime egala cu 50 cm

                sort_param = []
                sort_desc = False
                filtru_param = []
                filtru_valoare = []
                filtru_operatori = []
                lista_operatori = ['>=', '<=', '!=', '<', '>', '=']
                if len(comanda) > 1:
                    for el in comanda:
                        if el.startswith('sort='):
                            sort_param = el.split('=')[1].split(',')
                            for e in comanda:
                                if e == 'desc':
                                    sort_desc = True
                        else:
                            for op in lista_operatori:
                                if el.find(op) > -1:
                                    filtru_param.append(el.split(op)[0])
                                    filtru_valoare.append(el.split(op)[1]
                                                          .strip('\'\"'))
                                    filtru_operatori.append(op)
                                    break

                cat.print_catalog(carac=lista_coloane, sort=sort_param,
                                  carac_filtru=filtru_param,
                                  filtru=filtru_valoare,
                                  op_filtru=filtru_operatori, invers=sort_desc)

            elif cuvant_cheie == 'info':

                # Permite afisarea informatiilor despre un produs.
                # Sintaxa este : info <cod produs>, unde <cod produs> poate fi
                # folosit cu sau fara ghilimele
                # Foloseste metoda __str__ pentru fiecare obiect

                if len(comanda) > 1:
                    lista_produse = cat.cautare_produs('cod_produs',
                                                       comanda[1])
                    if len(lista_produse) > 0:
                        for produs in lista_produse:
                            print(produs)
                    else:
                        print(f'Niciun produs cu codul {comanda[1]} '
                              'nu a fost gasit in catalog. Introdu list '
                              'pentru a lista produsele din catalog.')
                else:
                    print('Trebuie sa introduci un cod produs. Sintaxa este : '
                          'info <cod produs>')

            elif cuvant_cheie == 'edit':

                # Permite editarea parametrilor unui produs.
                # Sintaxa este : edit <cod produs>, unde <cod produs> poate
                # fi folosit cu sau fara ghilimele
                # Se poate edita una sau mai multe caracteristici prin sintaxa
                # edit <cod produs> <carac1> <carac2> ...
                # Daca nicio caracteristica nu este trecuta, toate
                # caracteristicile vor fi listate

                if len(comanda) > 1:
                    lista_produse = cat.cautare_produs('cod_produs',
                                                       comanda[1])
                    if len(lista_produse) > 0:
                        produs = lista_produse[0]
                        if len(comanda) > 2:
                            for e in comanda[2:]:
                                if hasattr(produs, e):
                                    produs.input_valoare(e, 'Introdu noua '
                                    f'valoare pentru {e} (valoare veche : '
                                    f'{getattr(produs,e)}) - Apasa <Enter> '
                                    'pentru a anula : ',
                                    'nu este o valoare corecta.', True)
                        else:
                            for e in produs.__dict__:
                                produs.input_valoare(e, 'Introdu noua valoare '
                                                     f'pentru {e} (valoare '
                                                     f'veche : {getattr(produs,e)})'
                                                     ' - Apasa <Enter> pentru a '
                                                     'anula : ',
                                                     'nu este o valoare corecta.',
                                                     True)
                    else:
                        print(f'Niciun produs cu codul {comanda[1]} nu a fost '
                              'gasit in catalog. Introdu list pentru a lista '
                              'produsele din catalog.')
                else:
                    print('Trebuie sa introduci un cod produs pentru a modifica'
                          ' caracteristicile produsului. Introdu : '
                          'edit <cod produs> <carac de editat>')

            elif cuvant_cheie == 'load':

                # Permite deschiderea unui catalog. Sintaxa este :
                # load <cale fisier>
                # Daca un alt catalog era deja deschis, toate informatiile
                # vor fi pierdute.

                if len(comanda) > 1:
                    valid = incarcare_catalog(cale=comanda[1])
                    if valid is True:
                        fisier_catalog = comanda[1]
                        print(f'Catalogul {os.path.basename(comanda[1])} '
                              'a fost incarcat.')
                    else:
                        print('A aparut o problema la incarcarea fisierului '
                              f'{os.path.basename(comanda[1])}.')
                else:
                    print('Trebuie sa introduci calea pentru a incarca un '
                          'catalog. Sintaxa este : load <cale catalog>')

            elif cuvant_cheie == 'save':

                # Permite salvarea datelor intr-un fisier.
                # Sintaxa este : save <cale fisier>
                # Daca calea fisierului nu este trecuta, datele vor fi salvate
                # in fisierul actual retinut in variabila fisier_catalog

                cale_fisier = fisier_catalog
                if len(comanda) > 1:
                    cale_fisier = comanda[1]
                valid = salvare_catalog(cale_fisier)
                if valid is True:
                    print('Catalogul a fost salvat in fisierul '
                          f'{os.path.basename(cale_fisier)}.')
                else:
                    print('A aparut o problema la salvarea datele in fisier'
                          f' {os.path.basename(cale_fisier)}.')

            elif cuvant_cheie == 'options':

                # Autorizeaza modificarea unor parametri din aplicatie.
                # In momentul de fata, doar doua sunt disponibile :
                # 1. Modificarea coloanelor afisate cu functia list
                # 2. Modificarea numelui magazinului

                while True:
                    print('Optiune disponibile :')
                    print('\n1. Schimbarea coloanelor pentru afisajul lista')
                    print('2. Schimbarea numele magazinului\n')
                    resp = input('Options - apasa <enter> pentru a iesi > ')
                    if resp == '':
                        break
                    else:
                        try:
                            num_meniu = int(resp)
                            if num_meniu == 1:
                                print('Afisajul actual contine urmatoarele '
                                      'coloane :')
                                sir = ''
                                for coloana in lista_coloane:
                                    sir += coloana + ', '
                                sir = sir[:-2]
                                print(sir)
                                print('\nParametrii disponibili sunt :')
                                sir = ''
                                for param in sorted(lista_parametri[1:]):
                                    sir += param + ', '
                                sir = sir[:-2]
                                print(sir + '\n')
                                print('Introdu un sir de caractere cu '
                                      'coloanele dorite pentru afisaj, '
                                      'separate cu \',\'')
                                print('De exemplu : cod_produs,producator,'
                                      'pret\n')
                                resp = input('Introdu noile coloane - apasa '
                                             '<enter> pentru a iesi : ')
                                if resp == '':
                                    break
                                else:
                                    lista_coloane_bruta = resp.split(',')
                                    lista_coloane_gasite = []
                                    for coloana in lista_coloane_bruta:
                                        if coloana.strip() in \
                                           lista_parametri[1:]:
                                            lista_coloane_gasite.append(coloana.strip())
                                    if len(lista_coloane_gasite) > 0:
                                        lista_coloane = lista_coloane_gasite
                                        print('Lista coloanelor a fost '
                                              'modificata.\n')
                            if num_meniu == 2:
                                resp = input('Introdu noul nume a magazinului -'
                                             ' apasa <enter> pentru a iesi : ')
                                if resp == '':
                                    break
                                else:
                                    nume_magazin = resp
                                    print('Numele magazinului a fost schimbat')
                        except:
                            print('Numarul sau optiunea introduse nu sunt '
                                  'valide')
            else:
                print(f'{cuvant_cheie} nu este o comanda valida. Intra help '
                      'pentru lista comenzilor.')
            print()
