class CSVTimeSeriesFile():
    #inizializzazione del file
    def __init__(self, name):
        self.name = name
       
    #funzione che ritorna una lista di liste coi dati
    def get_data(self):
        #prova ad aprire il file
        try:
            mio_file = open(self.name,'r')
            mio_file.readline()
        #lancia un eccezione se ci sono errori nell'apertura del file               
        except Exception as e:
            raise ExamException(f'Errore in apertura del file:{e}') from e #f-string per formattare l'errore
        else:
            #conta le righe del file per verificare che non sia vuoto
            mio_file = open(self.name, 'r')
            rows = sum(1 for row in mio_file)
            if rows == 0:
                mio_file.close()
                raise ExamException('Il file è vuoto')
            mio_file = open(self.name, 'r')
            list = []
            for line in mio_file:
                line = line.strip()  #elimina gli spazi
                if line and ',' in line: #verifica che la linea non sia vuota e che contenga una virgola
                    elements = line.split(",")
                    test = True
                    test_2 = True
                    if elements[0]!= 'date' and elements[1].isdigit() and elements[1]!=0 and int(elements[1])>0 and '-' in elements[0]:
                        anno_curr = elements[0].split("-")[0]
                        mese_curr = elements[0].split("-")[1]
                        if anno_curr.isdigit() and mese_curr.isdigit():
                            #if 1 <= int(mese_curr) <= 9:
                            #    mese_curr = f"{int(mese_curr):02d}"  #se il mese è nel formato 1,2,..,9, aggiunge uno 0 all'inizio in modo che possa essere accettato
                            #else: str(mese_curr)
                            mesi = ['01','02','03','04','05','06','07','08','09','10','11','12']
                            if mese_curr in mesi and int(anno_curr) >= 0 and int(anno_curr)<=2024: #verifico che il mese e l'anno siano validi (anno max 2024)
                                for item in list:
                                    if elements[0] == item[0]:
                                        test = False
                                    anno_prec = item[0].split("-")[0]
                                    mese_prec = item[0].split("-")[1]
                                    #if 1 <= int(mese_prec) <= 9:
                                    #    mese_prec = f"{int(mese_prec):02d}"  #aggiungo lo zero all'inizio altrimenti non verifica l'ordine
                                    #else: 
                                    #    str(mese_prec)
                                    if int(anno_curr) < int(anno_prec):
                                        test_2 = False
                                    if int(anno_curr) == int(anno_prec) and int(mese_curr)<int(mese_prec):
                                        test_2 = False
                                if not test and not test_2:
                                    mio_file.close()
                                    raise ExamException('Elemento ripetuto e non ordinato')
                                if not test:
                                    mio_file.close()
                                    raise ExamException('Elementi ripetuti')                      
                                if not test_2:
                                    mio_file.close()
                                    raise ExamException('Serie non ordinata')
                                list.append(elements)
                            
            if list == []:
                raise ExamException('La lista è vuota') #alza un'eccezione se non ci sono valori accettabili nel file
            lista_convertita = [[elemento[0], int(elemento[1])] for elemento in list] #list comprehension per convertire a int il secondo valore delle liste interne
            mio_file.close()
            return lista_convertita
             
class ExamException(Exception):
    pass

def find_min_max(time_series):
    dict = {}
    val_min = 0
    val_max = 0
    min = []
    max = []
    for element in time_series:             
        anno = element[0].split("-")[0]
        mese = element[0].split("-")[1]
        valore = element[1]
        if anno not in dict:
            min = []
            max = []
            val_min = valore
            val_max = valore
            min.append(mese)
            max.append(mese)
            dict_interno = {"min": min, "max":max}
            dict[anno] = dict_interno #aggiunge il valore 'dict_interno' alla chiave 'anno'
        else:
            flag = False
            if valore>val_max:
                flag = True
                max.clear()
                val_max = valore
                max.append(mese)
            else: 
                if valore == val_max:
                    flag = True
                    max.append(mese)
            
            if valore<val_min:
                flag = True
                min.clear()
                val_min = valore
                min.append(mese)
            else:
                if valore == val_min:
                    flag = True
                    min.append(mese)
            if flag: #modifica il 'dict_interno' solo se variano le liste max,min
                dict_interno = {"min": min, "max":max}
                dict[anno] = dict_interno #modifica il valore della chiave 'anno' con il nuovo 'dict_interno'
    return dict
