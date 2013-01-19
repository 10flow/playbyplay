#!/usr/bin/python
import csv
import glob
import play

### START CONFIGURATION ###

#input files
csv_list = glob.glob('../raw-data/*.csv')
csv_list.sort()

#output files
output_json_filename = None #filename or None
output_csv_filename = None #filename or None

#database options

#For no database, uncomment this line:
#database_engine = None

#For SQLAlchemy database, uncomment these lines:
from plays_db import Base, ingest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

create_table = True #or False
#connection string format: mysql+mysqldb://<user>:<password>@<host>/<dbname>
database_engine = create_engine('mysql+mysqldb://root:password@localhost/playtest', echo=False)

### END CONFIGURATION ###


#set up play processors (add new ones here)
processors = []
import process_result
processors.append(process_result.ResultProcessor())
import process_playtype
processors.append(process_playtype.PlaytypeProcessor())
import process_success
processors.append(process_success.SuccessProcessor())
import process_catchall
processors.append(process_catchall.CatchallProcessor())

#process all plays
plays = []
play = play.PlayData()

print 'Processing Plays...'
for csv_file in csv_list:
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for raw_row in reader:
            play = play.next_play_data_factory(raw_row)
            for processor in processors:
                processor.process(play)
            plays.append(play.columns)

#write to JSON
if output_json_filename is not None:
    print 'Writing to JSON...'
    import json
    with open(output_json_filename, 'w') as f:
        json.dump(plays, f)
    
#write to CSV
if output_csv_filename is not None:
    print 'Writing to CSV...'
    import csv
    header = plays[0].keys()
    with open(output_csv_filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for play in plays:
            writer.writerow(play)
    
#database ingest
if database_engine is not None:
    print 'Writing to database (this will take a while)...'
    if create_table:
        Base.metadata.create_all(database_engine)
    Session = sessionmaker(bind=database_engine)
    session = Session()
    ingest(plays, session)
    
