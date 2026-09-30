# come struttura dati ho scelto una lista di liste, del tipo:
# foto = [codice, titolo, autore, mese, anno]
# album = [
#     [2019, [foto_1, foto_2]],
#     [2021, [foto_3]],
#     ...
# ]
import csv


# regole:
# ogni anno deve comparire solo una volta
# il codice è univoco in tutto l album
# il mese deve essere copmpreso tra 1 e 12
# l anno della foto deve coincidere con quello del gruppo

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album = []

    try:
        with open(file_path, "r", encoding="utf-8", newline="") as file:
            lettore = csv.reader(file, skipinitialspace=True)

            #ignoro la riga dell'intestazione, None è il valore che restituisce se il csv è vuoto
            next(lettore, None)

            for riga in lettore:
                codice, titolo, autore, mese, anno = riga

                mese = int(mese)
                anno = int(anno)

                foto = [codice, titolo, autore, mese, anno]

                gruppo_trovato = None

                #cerco se l'anno è già presente
                for gruppo in album:
                    if gruppo[0] == anno:
                        gruppo_trovato = gruppo
                        break

                #se l'anno non esiste creo un nuovo gruppo
                if gruppo_trovato is None:
                    gruppo_trovato = [anno, []]
                    album.append(gruppo_trovato)

                #aggiungo la foto alla lista del suo anno
                gruppo_trovato[1].append(foto)
        return album
    except FileNotFoundError:
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    #controlli di validità dell'input
    if mese < 1 or mese > 12:
        return None
    if cerca_foto(album, codice) is not None:
        return None

    foto = [codice, titolo, autore, mese, anno]

    #aggiungo la nuova foto al csv
    try:
        with open(file_path,"r+", encoding="utf-8", newline="") as file:
            #la devo aggiungere al fondo del file quindi
            file.seek(0, 2)

            scrittore = csv.writer(file)
            scrittore.writerow(foto)

    except FileNotFoundError:
        return None


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for gruppo in album:
        foto_anno = gruppo[1]

        for foto in foto_anno:
            if foto[0] == codice:
                return (
                    f"{foto[0]}, {foto[1]}, {foto[2]}, {foto[3]}, {foto[4]}"
                )


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""



def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
