import re
 
# Indicamos el fichero de lectura y de escritura del resultado
log_file_path = r"catalina.log"
result_file_path = r"result.log"
# Definimos el patron a encontrar
regex = '\"\s4[\d]{2}\s[\d]{3,4}\s'
read_line = True

match_list = []
# Abrimos el fichero y lo recorremos
with open(log_file_path, "r") as file:
    if read_line == True:
        for line in file:
            for match in re.finditer(regex, line, re.S):
                match_text = match.group()
                match_list.append(line)
    else:
        data = file.read()
        for match in re.finditer(regex, data, re.S):
            match_text = match.group()
            match_list.append(match_text + "\n")
file.close()

result = open(result_file_path,'w')

for error in match_list:
    result.write(str(error))

print("Found " + str(len(match_list)) + " errors.")
print("Adios.")