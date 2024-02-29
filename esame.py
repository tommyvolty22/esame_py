class CSVTimeSeriesFile():
    def __init__(self, name):
        self.name = name
       

    def get_data(self):
        try:
            mio_file = open(self.name,'r')
            mio_file.readline()
                       
        except Exception as e:
            raise ExamException(f'Errore in apertura del file:{e}') from e
        else:
            mio_file = open(self.name, 'r')
            rows = sum(1 for row in mio_file)
            if rows == 0:
                mio_file.close()
                raise ExamException('Il file è vuoto')
            mio_file = open(self.name, 'r')
            list = []
            for line in mio_file:
                line = line.strip()
                if line and ',' in line:
                    elements = line.split(",")
                    test = True
                    test_2 = True
                    if elements[0]!= 'date' and elements[1].isdigit() and elements[1]!=0 and int(elements[1])>0 and '-' in elements[0]:
                        anno_curr = elements[0].split("-")[0]
                        mese_curr = elements[0].split("-")[1]
                        if anno_curr.isdigit() and mese_curr.isdigit():
                            if 1 <= int(mese_curr) <= 9:
                                mese_curr = f"{int(mese_curr):02d}"  
                            else: str(mese_curr)
                            mesi = ['01','02','03','04','05','06','07','08','09','10','11','12']
                            if mese_curr in mesi and int(anno_curr) >= 0 and int(anno_curr)<=2024:
                                for item in list:
                                    if elements[0] == item[0]:
                                        test = False
                                    anno_prec = item[0].split("-")[0]
                                    mese_prec = item[0].split("-")[1]
                                    if 1 <= int(mese_prec) <= 9:
                                        mese_prec = f"{int(mese_prec):02d}"  
                                    else: 
                                        str(mese_prec)
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
                raise ExamException('La lista è vuota')
            lista_convertita = [[elemento[0], int(elemento[1])] for elemento in list]
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
            dict[anno] = dict_interno
        else:
            if valore>val_max:
                max.clear()
                val_max = valore
                max.append(mese)
            else: 
                if valore == val_max:
                    max.append(mese)
            
            if valore<val_min:
                min.clear()
                val_min = valore
                min.append(mese)
            else:
                if valore == val_min:
                    min.append(mese)
            dict_interno = {"min": min, "max":max}
            dict[anno] = dict_interno
    return dict
    
my_file = 'data.csv'
file = CSVTimeSeriesFile(my_file)
time_series = file.get_data()

print(find_min_max(time_series))