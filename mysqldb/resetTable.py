import re
fread = open("complete_db_structure.sql", 'r')
filedata = fread.readlines()
count = 0

fwrite = open("resetTable.sql", 'w')
fwrite.write("SET FOREIGN_KEY_CHECKS=0; \n")
fwrite.write("SET SQL_MODE=\"NO_AUTO_VALUE_ON_ZERO\"; \n")

for line in filedata:
# r1 = re.compile("CREATE TABLE IF NOT EXISTS `(.*?)\s*")
# r2 = re.compile("CREATE TABLE IF NOT EXISTS `.*?`(.*?)`")
    r3 = re.compile("CREATE TABLE IF NOT EXISTS (.*?)\s*`(.*?)`")
    matcher = r3.match(line)
    if matcher is not None:
        print matcher.group(2)
        count += 1
        fwrite.write("TRUNCATE TABLE " + matcher.group(2) + " ;" + "\n")
fwrite.write("SET FOREIGN_KEY_CHECKS=1; \n")
fwrite.close()
fread.close()
print count
