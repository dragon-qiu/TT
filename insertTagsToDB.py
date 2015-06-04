#!/usr/bin/env python
# Filename: insertTagsToDB.py

import MySQLdb, sys, getopt
from datetime import datetime, timedelta

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

def Usage():
	print 'insertTagsToDB.py usage:'
	print '-h, --help: 	print help message.'
	print '--debug: 	Set debug print. Default False '
	print '-t, --tag: 	Tag to handle'

def UTC8toUTC(utc8):
	t = datetime.strptime(utc8.replace(' GMT+0800', ''), '%Y-%m-%d %I:%M:%S%p')
	t -= timedelta(hours=8)
	return t.strftime('%Y-%m-%d %H:%M:%S')

def main(argv):
	DEBUG = False
	tag = ''

	try:
		opts, args = getopt.getopt(argv[1:], 'ht:', ['debug', 'tag=', 'help'])
	except getopt.GetoptError, err:
		print str(err)
		Usage()
		sys.exit(2)
	for o, arg in opts:
		if o in ('-h', '--help'):
			Usage()
			sys.exit(1)
		else:
			if o in ('-t', '--tag'):
				tag = arg
			if o == '--debug':
				DEBUG = True

	if tag == '':
		print 'Need parameter: --tag='
		sys.exit(1)

	FILENAME = 'TT_withTag_' + tag + '.txt'
	# print FILENAME
	# sys.exit(0)

	try:
		file = open(FILENAME,'r')
	except Exception, e:
		print 'The file \"' + FILENAME + '\" does not exist!'
		sys.exit(2)
	finally:
		pass

	try:
		conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=PASSWORD, db=DBNAME, port=3306)
		cur = conn.cursor()

		file.readline()
		file.readline()

		sum = 0
		n_abort = 0
		n_modified = 0
		i = 0

		lines = file.readlines()
		for line in lines:
			record = line.split('\r')[0].split('\n')[0].split('","')
			# delete '"'
			if len(record) < 6:
				continue

			record[0] = record[0][1:]
			record[-1] = record[-1][:-1]

			record[6] = record[6].split(' ')[0]
			if len(record) == 7:
				record.append('')

			if len(record) == 8:
				record.append('')

			exist = cur.execute('select * from ' + DBTABLE + ' where tt_id ="' + record[0] + '"')
			# if doesn't exist, insert it into db
			if exist == 0:
				# turn datetime from "2015-04-05 09:42:45PM GMT+0800" to "2015-04-05 13:42:45"
				record[4] = UTC8toUTC(record[4])
				record[5] = UTC8toUTC(record[5])
				record[8] = tag
				cur.execute('insert into ' + DBTABLE + ' values(%s, %s, %s, %s, %s, %s, %s, %s, %s)', record)
				i += 1
			else:
				result = cur.fetchone()
				tags = result[8]
				if tag in tags.split(';'):
					n_abort += 1
					if DEBUG == True:
						print '[DEBUG] TT:' +  record[0] + ' exists in database.'
				else:
					if len(tags) > 0:
						tags += ';' + tag
					else:
						tags = tag

					updatesql = 'update ' + DBTABLE + ' set tt_tags="' + tags + '" where tt_id="' + record[0] +'"'
					cur.execute(updatesql)
					i += 1
					n_modified += 1
					if DEBUG == True:
						print '[INFO] tag:' +  tag + ' has been insert into TT:' + record[0]

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
		print str(n_modified) + ' records\'s tags have been updated.'
		print str(n_abort) + ' aborted.'
		print 'Done!'

		cur.close()
		conn.close()

	except Exception, e:
		raise e
	finally:
		file.close()

if __name__ == '__main__':
	main(sys.argv)
