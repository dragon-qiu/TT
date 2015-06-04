#!/usr/bin/env python
# Filename: insertResultToDB.py

import MySQLdb, sys

FILENAME = 'TT_Correspondences_by_Supprt.txt'
DBHOST = 'ud43d7ec95f7352d90876.ant.amazon.com'
DBNAME = 'aws_support_remedy_bjs'
DBTABLE = 'correspondences'
DBUSER = 'support'
PASSWORD = 'bjssupport'

#  show columns from correspondences;
# +--------+-------------+------+-----+---------------------+-------+
# | Field  | Type        | Null | Key | Default             | Extra |
# +--------+-------------+------+-----+---------------------+-------+
# | c_id   | char(15)    | NO   | PRI | NULL                |       |
# | c_ower | varchar(20) | NO   |     | support             |       |
# | tt_id  | varchar(12) | NO   |     | 00000000            |       |
# | c_date | datetime    | NO   |     | 2006-03-14 00:00:00 |       |
# +--------+-------------+------+-----+---------------------+-------+

DEBUG = False

if len(sys.argv) > 1:
	if sys.argv[1].startswith('--') and sys.argv[1][2:] == 'debug':
		DEBUG = True
	else:
		print 'Invalide parameter: ' + sys.argv[1]
else:
	pass

try:
	file = open(FILENAME,'r')
except Exception, e:
	print "The file " + FILENAME + " does not exist!"
	exit()
finally:
	pass

try:
	conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=PASSWORD, db=DBNAME, port=3306)
	cur = conn.cursor()

	file.readline()
	sum = 0
	n_abort = 0
	i = 0

	lines = file.readlines()
	for line in lines:
		record = line.split('\r')[0].split('\n')[0].split('\t')
		if len(record) != 4:
			continue
			pass

		exist = cur.execute('select c_id from ' + DBTABLE + ' where c_id ="' + record[0] + '"')
		if exist == 0:
			cur.execute('insert into ' + DBTABLE + ' values(%s, %s, %s, %s)', record)
			i += 1

			if DEBUG == True:
				print '[OK] ' +  str(record) + ' has been inserted into database.'

			if i > 99 :
				conn.commit()
				sum += i
				i = 0
				print str(sum) + ' records have been inserted into database: ' + DBNAME + '.' + DBTABLE
		elif DEBUG == True:
			print '[WARNING] ' +  str(record) + ' exists in database.'
			n_abort += 1
		else:
			pass

	if i > 0:
		conn.commit()
		sum += i
	else:
		pass

	print 'Total ' + str(sum) + ' records have been inserted into database: ' + DBNAME + '.' + DBTABLE
	print str(n_abort) + ' aborted.'
	print 'Done!'

	cur.close()
	conn.close()

except Exception, e:
	raise e
finally:
	file.close()
