#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# dinstar-imported.py
# version: 0.1
# Vinicius Marques de Souza
# vmsouza@vmsouza.com.br
#
# dinstar-importer import a call logfile from Dinstar DWG2000
# It can import to mysql database the logfiles from DINSTAR DWG2000
# Dinstar's logs must be generated from syslog log file
#
# PLEASE EDIT dinstar-importer.conf TO CONFIGURE THE IMPORTER
#

#*****************************************************************************
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#*****************************************************************************

import MySQLdb
import sys
import os.path
import string
import fcntl
import ConfigParser

from warnings import filterwarnings

def error(msg):
    print msg
    sys.exit(1)
    
def merror(e):
    print "Erro [%d]: %s " % (e.args[0], e.args[1])
    sys.exit(1)

script_filename = os.path.abspath(__file__)
config_filename = script_filename.replace(".py",".conf")
lock_filename = script_filename.replace(".py",".lock")

if not os.path.exists(config_filename):
    error("Configuration file '%s' do not exists" % (config_filename))

config = ConfigParser.ConfigParser()
config.read(config_filename)
try:
    mygateways=config.options("logs")
except ConfigParser.NoSectionError, e:
    error("Error: %s inside config file '%s'" % (e,config_filename))

try:
    mydatabase=config.options("mysql")
except ConfigParser.NoSectionError, e:
    error("Error: %s inside config file '%s'" % (e,config_filename))

mysqlconfigfields=['host','user','passwd','db']
for field in mysqlconfigfields:
    if not config.has_option("mysql", field):
        error("Option %s not found in section 'mysql'" % (field))
path_items = config.items("mysql")
db={}
for i,j in path_items:
    db.update({i:j})

path_items = config.items("logs")
gateways=[]
for i,j in path_items:
    gateways.append((i,j))

lock_file = open(lock_filename, 'w')
try:
    fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    error('dinstar-importer.py already running, please wait for commit')
try:
    conn = MySQLdb.connect(**db)
except MySQLdb.OperationalError, e:
    merror(e)

res = conn.cursor()

# disable mysql warnings
filterwarnings('ignore', category = MySQLdb.Warning)

# disable zero-date
res.execute("SET @old_sql_mode := @@sql_mode")
res.execute("SET @new_sql_mode := @old_sql_mode")
res.execute("SET @new_sql_mode := TRIM(BOTH ',' FROM REPLACE(CONCAT(',',@new_sql_mode,','),',NO_ZERO_DATE,'  ,','))")
res.execute("SET @new_sql_mode := TRIM(BOTH ',' FROM REPLACE(CONCAT(',',@new_sql_mode,','),',NO_ZERO_IN_DATE,',','))")
res.execute("SET @@sql_mode := @new_sql_mode")

# start transaction
res.execute("START TRANSACTION")

errors=0
imported=0

for gwname, gwfile in gateways:
    if os.path.exists(gwfile):
        file = open(gwfile,"r");
        for line in file:
            if line.replace("\n","") == "":
                continue
            array=line.split(',')
            startdate=array[1].replace("Start Date:","").strip()
            answerdate=array[2].replace("Answer Date:","").strip()
            if (answerdate == ""):
                answerdate = "0000-00-00 00:00:00"
            calldirection=array[3].replace("Call Direction:","").strip()
            source=array[4].replace("Source:","").strip()
            sourceip=array[5].replace("SourceIp:","").strip()
            destination=array[6].replace("Destination :","").strip()
            hangside=array[7].replace("Hangside:","").strip()
            reason=array[8].replace("Reason:","").strip()
            duration=array[9].replace("Duration:","").replace("(s)","").strip()
            rtpsend=array[10].replace("Rtp Send:","").strip()
            rtprecv=array[11].replace("Rtp recv:","").strip()
            rtplossrate=array[12].replace("Rtp loss Rate:","").replace("%","").strip()
            jitter=array[13].replace("jitter:","").strip()

            sql="SELECT * from callhistory where gwname='%s' and startdate='%s' and calldirection='%s' and source='%s' and sourceip='%s' and destination='%s' limit 1" % (gwname,startdate,calldirection,source,sourceip,destination)
            try:
                res.execute(sql)
            except MySQLdb.ProgrammingError, e:
                error(e)
            if (res.rowcount==0):
                sql="INSERT INTO callhistory (gwname,startdate,answerdate,calldirection,source,sourceip,destination,hangside,reason,duration,rtpsend,rtprecv,rtplossrate,jitter) VALUES (" \
                "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                (gwname,startdate,answerdate,calldirection,source, \
                 sourceip,destination,hangside,reason,duration, \
                 rtpsend,rtprecv,rtplossrate,jitter)
                try:
                    res.execute(sql)
                    imported+=1
                except MySQLdb.ProgrammingError, e:
                    print e.args[1] 
                    errors=1

if (errors == 0):
    print "Data ok, committing.\nTotal records imported: %s" % (imported)
    res.execute("COMMIT")
else:
    print "Found erros on sql insert, doing rollback"
    res.execute("ROLLBACK")

res.execute("SET @@sql_mode := @old_sql_mode")
conn.close()
