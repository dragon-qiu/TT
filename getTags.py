#!/usr/bin/env python
# Filename: getTags.py

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
	print 'getTags.py usage:'
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
		conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=PASSWORD, db=DBNAME, port=3306)
		cur = conn.cursor()

		exist = cur.execute('select tag from ' + DBTABLE)
		if exist > 0:
			tags = cur.fetchmany(exist)
			file = open(FILENAME,'w')
			for tag in tags:
				file.write(str(tag[0]) + '\n')

			file.close()
			print str(exist) + ' tags have been writen in ' + FILENAME

		cur.close()
		conn.close()

	except Exception, e:
		raise e
	finally:
		pass

if __name__ == '__main__':
	main(sys.argv)
