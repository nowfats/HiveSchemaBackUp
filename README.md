# HiveSchemaBackUp
Back up hive meta data
### REQUIREMENTS
Make sure hive CLI works on your cluster
### How to use
Write down the table name that you want to back up the schema  to TBLS file.
If the table is on database other than default, using DBname.Table instead of just table.
For example, you want to back up table test on default database and test2 on dababase D1, write down the following line to the TBLS file.
	
	test1
	D1.test2

After saving the TBLS file, run

	python exportHiveMeta.py

The result file will be saved to the $user_hive/ql directory, it contains the hive DDL of creating table and adding partition.
