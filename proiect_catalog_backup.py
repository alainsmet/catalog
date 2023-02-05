##class ReferintaException(Exception):
##    def __init__(self, mesaj):
##        Exception.__init__(self,mesaj)
        
class catalog:
    lista_obiecte = []
    __moneda = 'RON'
    __unitate_dist = 'm'
    __unitate_turatie = 'rpm'
    __unitate_consum = 'W'
    __unitate_volum = 'L'
    
    def __init__(self, pret = 0., consum = 0., producator = '', cod_produs = '', stoc = 0):
        self.pret = pret
        self.consum = consum
        self.producator = producator
        self.cod_produs = cod_produs
        self.stoc = stoc
        self.clasa = ''
        self.subclasa = ''

##    def verif_cod_produs(self, cod):
##        if cod == '':
##            raise ReferintaException('Un produs trebuie sa aiba o referinta')
##        elif len(self.cautare_produs('cod_produs',cod)) > 0:
##            raise ReferintaException('Un produs exista deja in catalog cu aceeasi referinta')

    def creare_produs(self):
##        while True:
##            cod_produs_brut = input('Intrati noul cod produs : ')
##            try:
##                self.verif_cod_produs(cod_produs_brut)
##                self.cod_produs = cod_produs_brut
##                break
##            except ReferintaException as e:
##                print(str(e))
        self.input_valoare('cod_produs', 'Intrati noul cod produs : ', '')
        self.input_valoare('producator', 'Intrati producatorul : ', 'nu este un nume valabil')
        self.input_valoare('pret', f'Intrati pretul produsului ({self.__moneda}) : ', 'nu este un pret valabil')
        self.input_valoare('consum', f'Intrati consumul produsului ({self.__unitate_consum}) : ', 'nu este un consum valabil')
        self.input_valoare('stoc', f'Intrati stocul disponibil : ', 'nu este un numar valabil')

    def input_valoare(self, carac, text_input, text_eroare):
        while True:
            val_brut = input(text_input)
            if carac == 'cod_produs':
                if val_brut == '':
                    print('Codul produs nu poate fi nul')
                elif len(self.cautare_produs('cod_produs',val_brut)) > 0:
                    print(f'Referinta {val_brut} exista deja un alt produs. Referinta trebuie sa fie unica.')
                else:
                    setattr(self,carac,val_brut)
                    break
            else:
                val = self.verif_valoare(carac,val_brut)
                if val != None:
                    setattr(self,carac,val)
                    break
                else:
                    print(f'{val_brut} ' + text_eroare)
        
    def num_obiecte(self):
        """Returneaza numarul de produse continute in catalog"""
        return len(catalog.lista_obiecte)

    def cautare_produs(self, carac, sir_cautare):
        """Returneaza o lista cu toate produsele la care caracteristica <carac> corespunde la valoare cautata <sir_cautare>"""
        lista_rezultate = []
        for e in catalog.lista_obiecte:
            if hasattr(e,carac):
                if str(getattr(e,carac)) == str(sir_cautare):
                    lista_rezultate.append(e)
        return lista_rezultate

    def lista_ord(self, carac, lista = '', invers=False):
        """Returneaza o lista cu produsele ordonate dupa o caracteristica (pret, consum, ...). Daca <invers> == False, ordonate de la cel mai mic pana la cel mai mare."""
        lista_rezultate = []
        if lista != '':
            lista_rezultate = sorted(lista,key=lambda x:getattr(x,carac), reverse=invers)
        return lista_rezultate

    def verif_valoare(self, carac, valoare):
        if carac in self.__dict__:
            tip_carac = type(getattr(self,carac))
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

    def print_catalog(self, carac = [], filtru = '', carac_filtru = '', sort = '', invers=False):
        """Listeaza catalogul de produse, si permite sa filtreze si sa sorteze"""
        lista_rezultate = catalog.lista_obiecte
        sir_e = 'Catalog complet de produse disponibile'
        if carac_filtru != '' and filtru != '':
            lista_rezultate = self.cautare_produs(carac_filtru, filtru)
            sir_e = f'Extras din catalog, unde {carac_filtru} = {filtru}'
        if sort != '':
            lista_rezultate = self.lista_ord(carac=sort, lista=lista_rezultate, invers=invers)
            sir_e += f', sortat dupa {sort} '
            if invers == False:
                sir_e += 'ascendent'
            else:
                sir_e += 'descendent'
        if carac != []:
            offset = 5
            latime_col = [len(carac[x]) for x in range(len(carac))]
            for e in lista_rezultate:
                for c in range(len(carac)):
                    if hasattr(e,carac[c]):
                        if len(str(getattr(e,carac[c]))) > latime_col[c]:
                            latime_col[c] = len(str(getattr(e,carac[c])))

            print(sir_e,'\n')
            sir_e = ''
            for c in range(len(carac)):
                sir_e += carac[c].replace('_', ' ').capitalize().ljust(latime_col[c]+offset) + ' | '
            sir_e = sir_e[:-3]
            print(sir_e)
            print('-' * len(sir_e))
            for e in lista_rezultate:
                sir_e = ''
                for c in range(len(carac)):
                    if hasattr(e,carac[c]):
                        sir_e += str(getattr(e,carac[c])).ljust(latime_col[c]+offset) + " | "
                    else:
                        sir_e += ''.ljust(latime_col[c]+offset) + " | "
                sir_e = sir_e[:-3]
                print(sir_e)

            print('\n',f'Total produse : {len(lista_rezultate)} din {len(catalog.lista_obiecte)}',sep='')
        

class Electrocasnice_mari(catalog):
    def __init__(self, pret = 0., consum = 0., producator = '', cod_produs = '', adincime = 0., \
                 latime = 0., inaltime = 0., stoc = 0):
        catalog.__init__(self, pret, consum, producator, cod_produs, stoc)
        self.clasa = '<<Electrocasnice mari>>'
        self.adincime = adincime
        self.latime = latime
        self.inaltime = inaltime

    def creare_produs(self):
        catalog.creare_produs(self)
        self.input_valoare('adincime', f'Intrati adincimea ({catalog._catalog__unitate_dist}) : ', 'nu este o valoare valabila')
        self.input_valoare('latime', f'Intrati latimea ({catalog._catalog__unitate_dist}) : ', 'nu este o valoare valabila')
        self.input_valoare('inaltime', f'Intrati inaltimea ({catalog._catalog__unitate_dist}) : ', 'nu este o valoare valabila')

class Electrocasnice_mici(catalog):
    def __init__(self, pret = 0., consum = 0., producator = '', cod_produs = '', lungime_cablu = 0., baterie = 'Nu', stoc = 0):
        catalog.__init__(self, pret, consum, producator, cod_produs, stoc)
        self.clasa = '<<Electrocasnice mici>>'
        self.lungime_cablu = lungime_cablu
        self.baterie = baterie

    def creare_produs(self):
        catalog.creare_produs(self)
        self.input_valoare('lungime_cablu', f'Intrati lungimea cablului ({catalog._catalog__unitate_dist}) : ', 'nu este o valoare valabila')
        self.input_valoare('baterie', f'Intrati informatii despre bateria : ', 'nu este o valoare valabila')

class Frigider(Electrocasnice_mari):
    def __init__(self, pret = 0., consum = 0., producator = '', cod_produs = '', adincime = 0., \
                 latime = 0., inaltime = 0., capacitate_congelator = 0., capacitate_frigider = 0., stoc = 0):
        Electrocasnice_mari.__init__(self, pret, consum, producator, cod_produs, adincime, latime, inaltime, stoc)
        catalog.lista_obiecte.append(self)
        self.subclasa = '<<Frigider>>'
        self.capacitate_congelator = capacitate_congelator
        self.capacitate_frigider = capacitate_frigider

    def __str__(self):
        ret_string = f'{self.subclasa.strip("<>")} marca : {self.producator}, cod produs : {self.cod_produs}\nPret : {self.pret} {catalog._catalog__moneda}\n'
        ret_string += f'Consum : {self.consum} {catalog._catalog__unitate_consum}, Dimensiuni (A x L x I) : {self.adincime} x {self.latime} x {self.inaltime} ({catalog._catalog__unitate_dist})\n'
        ret_string += f'Capacitate : frigider {self.capacitate_frigider} {catalog._catalog__unitate_volum} - congelator {self.capacitate_congelator} {catalog._catalog__unitate_volum}\n'
        ret_string += f'Stoc : {self.stoc}'
        return ret_string

    def creare_produs(self):
        Electrocasnice_mari.creare_produs(self)
        self.input_valoare('capacitate_congelator', f'Intrati capacitatea congelatorului ({catalog._catalog__unitate_volum}) : ', 'nu este o valoare valabila')
        self.input_valoare('capacitate_frigider', f'Intrati capacitatea frigiderului ({catalog._catalog__unitate_volum}) : ', 'nu este o valoare valabila')

class Aragaz(Electrocasnice_mari):
    def __init__(self, pret = 0., consum = 0., producator = '', cod_produs = '', adincime = 0., \
                 latime = 0., inaltime = 0., nr_arzatoare = 0, stoc = 0):
        Electrocasnice_mari.__init__(self, pret, consum, producator, cod_produs, adincime, latime, \
                                     inaltime, stoc)
        catalog.lista_obiecte.append(self)
        self.subclasa = '<<Aragaz>>'
        self.nr_arzatoare = nr_arzatoare

    def __str__(self):
        ret_string = f'{self.subclasa.strip("<>")} marca : {self.producator}, cod produs : {self.cod_produs}\nPret : {self.pret} {catalog._catalog__moneda}\n'
        ret_string += f'Consum : {self.consum} {catalog._catalog__unitate_consum}, Dimensiuni (A x L x I) : {self.adincime} x {self.latime} x {self.inaltime} ({catalog._catalog__unitate_dist})\n'
        ret_string += f'Numar arzatoare : {self.nr_arzatoare}\n'
        ret_string += f'Stoc : {self.stoc}'
        return ret_string

    def creare_produs(self):
        Electrocasnice_mari.creare_produs(self)
        self.input_valoare('nr_arzatoare', f'Intrati numarul de arzatoare : ', 'nu este o valoare valabila')

class Mixer(Electrocasnice_mici):
    def __init__(self, pret = 0., consum = 0., producator = '', cod_produs = '', lungime_cablu = 0., \
                 baterie = 'Nu', rotatii_min = 0, stoc = 0):
        Electrocasnice_mici.__init__(self, pret, consum, producator, cod_produs, lungime_cablu, \
                                     baterie, stoc)
        catalog.lista_obiecte.append(self)
        self.subclasa = '<<Mixer>>'
        self.rotatii_min = rotatii_min
        
    def __str__(self):
        ret_string = f'{self.subclasa.strip("<>")} marca : {self.producator}, cod produs : {self.cod_produs}\nPret : {self.pret} {catalog._catalog__moneda}\n'
        ret_string += f'Consum : {self.consum} {catalog._catalog__unitate_consum}, Lungime cablu : {self.lungime_cablu} {catalog._catalog__unitate_dist}\n'
        ret_string += f'Baterie: {self.baterie}, Rotatii pe min : {self.rotatii_min} {catalog._catalog__unitate_turatie}\n'
        ret_string += f'Stoc : {self.stoc}'
        return ret_string

    def creare_produs(self):
        Electrocasnice_mici.creare_produs(self)
        self.input_valoare('rotatii_min', f'Intrati viteza de rotatie ({catalog._catalog__unitate_turatie}) : ', 'nu este o valoare valabila')

class Fier_calcat(Electrocasnice_mici):
    def __init__(self, pret = 0., consum = 0., producator = '', cod_produs = '', lungime_cablu = 0., \
                 baterie = 'Nu', rezervor = 0., stoc = 0):
        Electrocasnice_mici.__init__(self, pret, consum, producator, cod_produs, lungime_cablu, \
                                     baterie, stoc)
        catalog.lista_obiecte.append(self)
        self.subclasa = '<<Fier calcat>>'
        self.rezervor = rezervor

    def __str__(self):
        ret_string = f'{self.subclasa.strip("<>")} marca : {self.producator}, cod produs : {self.cod_produs}\nPret : {self.pret} {catalog._catalog__moneda}\n'
        ret_string += f'Consum : {self.consum} {catalog._catalog__unitate_consum}, Lungime cablu : {self.lungime_cablu} {catalog._catalog__unitate_dist}\n'
        ret_string += f'Baterie: {self.baterie}, Rezervor : {self.rezervor} {catalog._catalog__unitate_volum}\n'
        ret_string += f'Stoc : {self.stoc}'
        return ret_string

    def creare_produs(self):
        Electrocasnice_mici.creare_produs(self)
        self.input_valoare('rezervor', f'Intrati volumul rezervorului ({catalog._catalog__unitate_volum}) : ', 'nu este o valoare valabila')

if __name__ == '__main__':

    import sys, inspect

    def lista_tip_produs():
        clase_dispo = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        lista_produse = []
        for c in clase_dispo:
            if issubclass(c[1],catalog):
                num_subclase = 0
                for subclasa in clase_dispo:
                    if issubclass(subclasa[1],c[1]):
                        num_subclase += 1
                if num_subclase == 1:
                    lista_produse.append(c)
        return lista_produse
        
    def print_ajutor():
        print('Lista de comenzi disponibile :','exit : iesire din catalog', 'add : adauga un produs in catalog - add <tip produs>','del : sterge un produs din catalog - del <cod produs>', \
          'info : informatie despre un produs - info <cod produs>', 'list : listeaza produsele din catalog','help : listeaza comenzile disponibile',sep='\n')
        
    def split_comanda(sir_brut):
        """Returneaza o lista de parametri, asa cum trebuie :)"""
        strip_sir_brut = sir_brut.strip()
        temp_sir = ''
        comentariu_flag = False
        comentariu_chars = ['\"','\'']
        comanda = []
        
        for char in strip_sir_brut:
            if char == ' ' and comentariu_flag == False:
                temp_sir = temp_sir.strip('\"')
                temp_sir = temp_sir.strip('\'')
                comanda.append(temp_sir)
                temp_sir = ''
            elif char == ' ' and comentariu_flag == True:
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

    global cat, lista_coloane
    cat = catalog()
    lista_coloane = ['cod_produs','subclasa','producator','pret','consum','stoc']
    print('Bine ai venit la catalog de produse IKEO\n')
    print_ajutor()
    print()
    while True:
        sir_brut = input('Catalog IKEO > ')
        comanda = split_comanda(sir_brut)
        if comanda[0] != '':
            cuvant_cheie = comanda[0].lower()
            if cuvant_cheie == 'exit':
                break
            elif cuvant_cheie == 'help':
                print_ajutor()
            elif cuvant_cheie == 'add':
                lista_produse = lista_tip_produs()
                if len(comanda) > 1:
                    if comanda[1].capitalize() in (lista_produse[x][0] for x in range(len(lista_produse))):
                        #print(lista_produse)
                        for produs in lista_produse:
                            if comanda[1].capitalize() == produs[0]:
                                nou_produs = produs[1]()
                                nou_produs.creare_produs()
                    else:
                        print(f'{comanda[1].capitalize()} nu este un produs valid. Urmatoarele produse sunt disponibile :')
                        for produs in lista_produse:
                            print(produs[0])
                else:
                    print('Trebuie sa intri un produs. Urmatoarele produse sunt disponibile :')
                    for produs in lista_produse:
                        print(produs[0])
            elif cuvant_cheie == 'list':
                cat.print_catalog(carac=lista_coloane)
            elif cuvant_cheie == 'info':
                if len(comanda) > 1:
                    lista_produse = cat.cautare_produs('cod_produs',comanda[1])
                    if len(lista_produse) > 0:
                        for produs in lista_produse:
                            print(produs)
            else:
                print(f'{cuvant_cheie} nu este o comanda valida. Intra help pentru lista comenzilor.')
            print()
