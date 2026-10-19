import csv
from operator import attrgetter

class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        # TODO
        self.__nome = nome
        self.lista_esp = []
        self.lista_stand = []
        self.new_esp = None
        self.new_stand = None

    def __str__(self):
        return f"{self.__nome}"

    """Aggiungere setter e getter se necessari"""
    # TODO
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, new_nome):
        if any(carat.isdigit() for carat in new_nome):
            raise ValueError("Il nome non può contenere valori numerici")

        self.__nome = new_nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        # TODO
        n_temp = LingottoFiere(self.nome)
        self.lista_esp = []
        self.lista_stand = []
        file = open(file_path, "r")
        lettore = csv.reader(file)
        for riga in lettore:
            if riga[0].startswith("E"):
                self.new_esp = Espositore(
                    nome = n_temp.nome,
                    codice_esp = riga[0],
                    rappr_azienda= riga[1]+' '+riga[2]
                )
                self.lista_esp.append(self.new_esp)
            if riga[0].startswith("S"):
                if len(riga)==4:
                    self.new_stand = StandStandard(
                        nome = n_temp.nome,
                        codice_st = riga[0],
                        metri_sup = riga[1],
                        padiglione = riga[2],
                        prezzo = int(riga[3]),
                    )
                    self.lista_stand.append(self.new_stand)
                else:
                    if riga[4].isdigit():
                        self.new_stand = StandPiuPrese(
                            nome = n_temp.nome,
                            codice_st = riga[0],
                            metri_sup = riga[1],
                            padiglione = riga[2],
                            prezzo = round(int(riga[3])*(1+(0.07*int(riga[4]))), 2),
                            num_prese = riga[4]
                        )
                        self.lista_stand.append(self.new_stand)
                    else:
                        self.new_stand = StandPremium(
                            nome = n_temp.nome,
                            codice_st = riga[0],
                            metri_sup = riga[1],
                            padiglione = riga[2],
                            prezzo = round(int(riga[3]) * 1.30, 2),
                            posizione = riga[4]
                        )
                        self.lista_stand.append(self.new_stand)

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        # TODO
        espositore_trovato = None
        stand_trovato = None
        for espositore in self.lista_esp:
            if espositore.codice_esp == codice_espositore:
                espositore_trovato = espositore
                break

        for stand in self.lista_stand:
            if stand.codice_st == codice_stand:
                stand_trovato = stand.codice_st
                break

        if espositore_trovato and stand_trovato:
            espositore_trovato.stand_assegnato = stand_trovato

        else:
            raise Exception(f"Impossibile assegnare l'espositore {codice_espositore} allo stand {codice_stand}")


    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        # TODO
        for e in self.lista_esp:
            if e.stand_assegnato is None:
                print(f"L'espositore {e.rappr_azienda}, {e.codice_esp}, non ha uno stand assegnato")
            if e.stand_assegnato is not None:
                print(f"All'espositore {e.rappr_azienda}, {e.codice_esp}, è stato assegnato lo stand {e.stand_assegnato}")

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        # TODO
        lista_ordinata = self.lista_stand
        lista_ordinata.sort(key=attrgetter('prezzo'))
        return lista_ordinata


class Espositore(LingottoFiere):
    def __init__(self, nome, codice_esp, rappr_azienda):
        super().__init__(nome)
        self.codice_esp = codice_esp
        self.rappr_azienda = rappr_azienda
        self.stand_assegnato = None
    def __str__(self):
        return f"{self.codice_esp}: {self.rappr_azienda}"

class StandStandard(LingottoFiere):
    def __init__(self, nome, codice_st, metri_sup, padiglione, prezzo):
        super().__init__(nome)
        self.codice_st = codice_st
        self.metri_sup = metri_sup
        self.padiglione = padiglione
        self.prezzo = prezzo
        self.assegnazione = "Disponibile"

    def __str__(self):
        return (f" {self.codice_st}: {self.metri_sup}mq - Padiglione {self.padiglione} - "
                f"Prezzo {self.prezzo}€ ")

    def __lt__(self, other):
        return int(self.prezzo) < int(other.prezzo)

class StandPiuPrese(StandStandard):
    def __init__(self, nome, codice_st, metri_sup, padiglione, prezzo, num_prese):
        super().__init__(nome, codice_st, metri_sup, padiglione, prezzo)
        self.num_prese = num_prese

    def __str__(self):
        return f"{super().__str__()} - Prese aggiuntive: {self.num_prese}"

    def __lt__(self, other):
        return super().__lt__(other)

class StandPremium(StandStandard):
    def __init__(self, nome, codice_st, metri_sup, padiglione, prezzo, posizione):
        super().__init__(nome, codice_st, metri_sup, padiglione, prezzo)
        self.posizione = posizione

    def __str__(self):
        return f"{super().__str__()} - Posizione: {self.posizione}"

    def __lt__(self, other):
        return super().__lt__(other)