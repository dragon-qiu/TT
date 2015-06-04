#!/usr/bin/env python
# Filename: insertTTsToDB.py

import MySQLdb, sys

FILENAME = 'Cut_TT_by_Support.txt'
DBHOST = 'ud43d7ec95f7352d90876.ant.amazon.com'
DBNAME = 'aws_support_remedy_bjs'
DBTABLE = 'tickets'
DBUSER = 'support'
PASSWORD = 'bjssupport'

#   show columns from tickets;
# +-------------------+---------------+------+-----+---------------------+-------+
# | Field             | Type          | Null | Key | Default             | Extra |
# +-------------------+---------------+------+-----+---------------------+-------+
# | tt_id             | varchar(12)   | NO   | PRI | NULL                |       |
# | tt_ower           | varchar(20)   | NO   |     | support             |       |
# | description       | varchar(512)  | YES  |     | NULL                |       |
# | severity          | char(1)       | NO   |     | NULL                |       |
# | create_datetime   | datetime      | NO   |     | 2006-03-14 00:00:00 |       |
# | last_modified     | datetime      | NO   |     | 2006-03-14 00:00:00 |       |
# | tt_status         | varchar(9)    | NO   |     | NULL                |       |
# | resolved_datetime | datetime      | YES  |     | NULL                |       |
# | tt_tags           | varchar(1024) | YES  |     | NULL                |       |
# +-------------------+---------------+------+-----+---------------------+-------+

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
	n_modified = 0
	i = 0

	lines = file.readlines()
	for line in lines:
		record = line.split('\r')[0].split('\n')[0].split('\t')
		if len(record) > 9 or len(record) < 7:
			if DEBUG == True:
				print '[ERROR] ' +  str(record) + ' parse error.'
			continue

		if len(record) == 7:
			record.append('')
			pass
		if len(record) == 8:
			record.append('')
			pass

		exist = cur.execute('select * from ' + DBTABLE + ' where tt_id ="' + record[0] + '"')
		if exist == 0:
			cur.execute('insert into ' + DBTABLE + ' values(%s, %s, %s, %s, %s, %s, %s, %s, %s)', record)
			i += 1
			if DEBUG == True:
				print '[INFO] ' +  str(record) + ' has been inserted into database.'
		else:
			result = cur.fetchone()
			modified = False
			if str(result[5]) != record[5]:
				updatesql = 'update ' + DBTABLE + ' set last_modified="' + record[5] +'"'
				if result[1] != record[1]:
					updatesql += ', tt_ower="' + record[1] +'"'
					if result[2] != record[2]:
						updatesql += ', description="' + record[2] +'"'
					if result[3] != record[3]:
						updatesql += ', severity="' + record[3] +'"'
					if result[6] != record[6]:
						updatesql += ', tt_status="' + record[6] +'"'
					if result[7] != record[7]:
						updatesql += ', resolved_datetime="' + record[7] +'"'
				updatesql += ' where tt_id="' + record[0] +'"'
				cur.execute(updatesql)
				modified = True
			if result[8] != record[8]:
				updatesql = 'update ' + DBTABLE + ' set tt_tags="' + record[8] + '" where tt_id="' + record[0] +'"'
				cur.execute(updatesql)
				modified = True

			if modified == True:
				i += 1
				n_modified += 1
				if DEBUG == True:
					print '[INFO] ' +  str(record) + ' has been updated into database.'
			else:
				n_abort += 1
				if DEBUG == True:
					print '[DEBUG] ' +  str(record) + ' exists in database.'
				pass
		if i > 99 :
				conn.commit()
				sum += i
				i = 0
				print str(sum) + ' records have been inserted/updated into database: ' + DBNAME + '.' + DBTABLE

	if i > 0:
		conn.commit()
		sum += i
	else:
		pass

	print 'Total ' + str(sum) + ' records have been updated/inserted into database: ' + DBNAME + '.' + DBTABLE
	print str(n_modified) + ' records updated.'
	print str(n_abort) + ' aborted.'
	print 'Done!'

	cur.close()
	conn.close()

except Exception, e:
	raise e
finally:
	file.close()
