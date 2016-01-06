import os,sys,shutil
import getpass

DEFAULT = "default"

def genTableInfo(workingDir, file):
    """
       Generate hive table schema and partition
       table is for hql and partition file name
       tableName is using for hive query 
    """
    tables = open(file, "r")
    for table in tables:
        if "." in table :
            databaseName = table.split(".")[0]
            tableName = table.split(".")[1]
        else :
            databaseName = DEFAULT
            tableName = table
        schemacommand = "use %s;show create table %s" %(databaseName, tableName)
        partcommand = "use %s;show partitions %s" %(databaseName, tableName)
        os.system("/usr/bin/hive  -e \"%s\" > %s/schema/%s" %(schemacommand,workingDir,table))
        os.system("/usr/bin/hive  -e \"%s\" > %s/part/%s" %(partcommand,workingDir,table))
    tables.close()
def mergeTableInfo(workingDir, file):
    """merge the hive schema and partition info into hql file"""
    tables = open(file, "r")
    for table in tables:
        tableName = table.split()[0]
        tableSQLGene(workingDir, tableName)

def tableSQLGene(workingDir, tableName):
    """generate the create table sql and alter table ... add partitions... sql into tableName.hql file"""
    tableSQLFile = workingDir + "/sql/" + tableName + ".hql"
    tableSchemaFile = workingDir + "/schema/" + tableName
    tablePartFile = workingDir + "/part/" + tableName
    writeFile = open (tableSQLFile, "w")
    schemaFile = open(tableSchemaFile, "r")
    partFile = open(tablePartFile, "r")
    if "." in tableName :
        databaseName = tableName.split(".")[0]
        tableName = tableName.split(".")[1]
    else :
        databaseName = DEFAULT
    writeFile.write("use %s;\n" % databaseName)
    if os.stat(tableSchemaFile).st_size != 0:
        for line in schemaFile:
            if "STORED" in line:
                break
            else : 
                writeFile.write(line)
        writeFile.write(";\n")
    schemaFile.close()
    if os.stat(tablePartFile).st_size != 0:
        for line in partFile:
            partInfo = line.split()[0]
            writeFile.write(getAddPartitionSQL(partInfo, tableName))
    writeFile.close()
    partFile.close()

def getAddPartitionSQL(partInfo, tableName):
    """parsing the partition info into add partition query"""
    partSQL = ""
    partKeys = partInfo.split("/")
    partKeys = map(lambda x : x.split("=")[0]+ "='" + x.split("=")[1] + "'", partKeys)
    partString = ','.join(map(str, partKeys))
    partSQL += "alter table " + tableName + " add if not exists partition(" + partString + ");\n"
    return partSQL
    
def main():
    user = getpass.getuser()
    workingDir = os.getcwd() + "/" + user+"_hive"
    if not os.path.exists(workingDir):
        os.makedirs(workingDir)
    if not os.path.exists(workingDir + "/part"):
        os.makedirs(workingDir + "/part")
    if not os.path.exists(workingDir + "/schema"):
        os.makedirs(workingDir + "/schema")
    if not os.path.exists(workingDir + "/sql"):
        os.makedirs(workingDir + "/sql")

    genTableInfo(workingDir, "TBLS")
    mergeTableInfo(workingDir, "TBLS")
    shutil.rmtree(workingDir + "/part")
    shutil.rmtree(workingDir + "/schema")


if __name__=="__main__":
    main()


