import hashlib

test1 = open("Python & Web Applications/ForensicExploration/test1.txt", 'r').read().strip().strip('-').strip().encode('utf-8')
test2 = open("Python & Web Applications/ForensicExploration/test2.txt", 'r').read().strip().strip('-').strip().encode('utf-8')

hash1 = hashlib.md5(test1).hexdigest()
hash2 = hashlib.md5(test2).hexdigest()

print(test1)
print(test2)