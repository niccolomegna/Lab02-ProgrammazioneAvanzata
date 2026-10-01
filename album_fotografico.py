# regole:
# ogni anno deve comparire solo una volta
# il codice è univoco in tutto l album
# il mese deve essere copmpreso tra 1 e 12
# l anno della foto deve coincidere con quello del gruppo

# ho scelto di realizzare la seguente struttura dati:
# foto = [codice, titolo, autore, mese, anno]
# gruppo = [anno, lista_delle_foto]
# album = [gruppo_1, gruppo_2, ...]

# un album quindi risulta ad esempio come:
# album = [
#     [
#         2019,
#         [
#             ["P001", "Tramonto sul mare", "Elena Conti", 7, 2019],
#             ["P011", "Vecchio faro", "Luca Neri", 5, 2019]
#         ]
#     ],
#     [
#         2021,
#         [
#             ["P002", "Montagne innevate", "Marco Bruni", 1, 2021]
#         ]
#     ]
# ]

#importo reader e writer da csv
from csv import reader, writer

def carica_da_file(file_path):
    """Carica le foto dal CSV, raggruppandole per anno."""
    #creo la lista album inizialmente vuota
    album = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # legge e scarta la riga delle intestazioni
            file.readline()

            #utilizzo la funzione reader che restituisce un oggetto iterabile dove per ogni iterazione viene restituita una lista di stringhe
            lettore = reader(file)

            #leggo tutte le righe e salvo i campi in una lista per ogni foto (converto anche mesi e anni in interi)
            for riga in lettore:
                codice = riga[0].strip()
                titolo = riga[1].strip()
                autore = riga[2].strip()
                mese = int(riga[3])
                anno = int(riga[4])

                foto = [
                    codice,
                    titolo,
                    autore,
                    mese,
                    anno
                ]

                #supponiamo inizialmente che l'anno non sia stato trovato
                anno_trovato = False

                #controlliamo che l'anno non sia già presente nell'album, se è presente aano_trovato diventa True
                for gruppo in album:
                    if gruppo[0] == anno:
                        gruppo[1].append(foto)
                        anno_trovato = True
                        break

                #se l'anno non è stato trovato allora aggiungo un nuovo_gruppo all'album
                if not anno_trovato:
                    nuovo_gruppo = [anno, [foto]]
                    album.append(nuovo_gruppo)

        return album

    except FileNotFoundError:
        return None

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto al CSV e all'album."""

    #controllo il mese
    if mese < 1 or mese > 12:
        return None

    #controllo che il codice sia unico
    for gruppo in album:
        for foto_esistente in gruppo[1]:
            if foto_esistente[0] == codice:
                return None

    #creo la nuova foto
    foto = [
        codice,
        titolo,
        autore,
        mese,
        anno
    ]

    try:
        #controllo che il file esista.
        #la modalità "a", da sola, creerebbe il file.
        with open(file_path, "r", encoding="utf-8"):
            pass

        #apro nuovamente il file aggiungendo in fondo usando writer
        with open(file_path, "a", encoding="utf-8") as file:
            scrittore = writer(file)
            scrittore.writerow(foto)

    except FileNotFoundError:
        return None

    #la scrittura è riuscita: aggiorno l'album
    #controlliamo che l'anno non sia già presente nell'album
    anno_trovato = False

    for gruppo in album:
        if gruppo[0] == anno:
            gruppo[1].append(foto)
            anno_trovato = True
            break

    if not anno_trovato:
        nuovo_gruppo = [anno, [foto]]
        album.append(nuovo_gruppo)

    return foto

def cerca_foto(album, codice):
    """Cerca una foto tramite il suo codice."""
    #passo tutte le foto di tutti gli album controlando che il codice sia uguale a quello ricercato poi ritorno le informazioni della foto
    for gruppo in album:
        for foto in gruppo[1]:
            if foto[0] == codice:
                return (
                    f"{foto[0]}, {foto[1]}, {foto[2]}, "
                    f"{foto[3]}, {foto[4]}"
                )

    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Restituisce i titoli di un anno ordinati alfabeticamente."""
    #cerco in tutti i gruppi di album quello con lo stesso anno richiesto, poi ordino e stampo i titoli in ordine alfabetico
    for gruppo in album:
        if gruppo[0] == anno:
            titoli = []

            for foto in gruppo[1]:
                titoli.append(foto[1])

            titoli.sort()
            return titoli

    return None


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
