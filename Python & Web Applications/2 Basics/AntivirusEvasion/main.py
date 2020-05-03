import base64
    
# Writing the file
# bytes = bytearray("print(dict(__import__('os').environ))",'utf-8')
bytes = bytearray("print('Hello')",'utf-8')
    
base64string = base64.b64encode(bytes)

harmless = "Python & Web Applications/2 Basics/AntivirusEvasion/harmless.py"
    
f = open(harmless,'w')
    
f.write(base64string.decode('utf-8'))
    
    
# Reading the file
f = open(harmless, 'r')
    
eval(base64.b64decode(f.readline()).decode('utf-8'))