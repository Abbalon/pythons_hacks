import  re

file = open('access.log')

log_contents = filter(None, file.read().split('\n'))

for line in (log_contents):
  entries = re.findall(r'"([^"]*)"', line)
  url = entries[0].split(' ')[1]
  url_parts = url.split('?')

  if(len(url_parts) > 1):
    query = url_parts[1]
    if(query.find('password')>-1):
      print("Found:\t")
      print(query)
      print("\n")

print("End")