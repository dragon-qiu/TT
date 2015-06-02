#!/usr/bin/env python
# Filename: insertTagsToTable.py

import MySQLdb, sys, getopt

DBHOST = 'ud43d7ec95f7352d90876.ant.amazon.com'
DBNAME = 'aws_support_remedy_bjs'
DBTABLE = 'tags'
DBUSER = 'support'
PASSWORD = 'bjssupport'

#   show columns from tags;
# +-------+----------+------+-----+---------+-------+
# | Field | Type     | Null | Key | Default | Extra |
# +-------+----------+------+-----+---------+-------+
# | tag   | char(64) | NO   | PRI | NULL    |       |
# +-------+----------+------+-----+---------+-------+

def Usage():
	print 'insertTagsToDB.py usage:'
	print '-h, --help: 	print help message.'
	print '--debug: 	Set debug print. Default False '
	print '-o, --output: 	Write tags to file. Default tags.txt'

def main(argv):
	DEBUG = False
	FILENAME = 'tags.txt'

	try:
		opts, args = getopt.getopt(argv[1:], 'ho:', ['debug', 'output=', 'help'])
	except getopt.GetoptError, err:
		print str(err)
		Usage()
		sys.exit(2)
	for o, arg in opts:
		if o in ('-h', '--help'):
			Usage()
			sys.exit(1)
		else:
			if o in ('-o', '--output'):
				FILENAME = arg
			if o == '--debug':
				DEBUG = True

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

		sum = 0
		n_abort = 0
		n_modified = 0
		i = 0

		lines = file.readlines()
		for line in lines:
			record = line.split('\r')[0].split('\n')[0]

			exist = cur.execute('select * from ' + DBTABLE + ' where tag ="' + record + '"')
			# if doesn't exist, insert it into db
			if exist == 0:
				cur.execute('insert into ' + DBTABLE + ' values(%s)', record)
				i += 1
			else:
				n_abort += 1

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

		print 'Total ' + str(sum) + ' new records have been inserted into database: ' + DBNAME + '.' + DBTABLE
		print str(n_modified) + ' records\'s tags have been changed.'
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
