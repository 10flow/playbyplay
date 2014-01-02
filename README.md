Play-By-Play Effectiveness Tools
================================

This project parses [AdvancedNFLStats.com's play-by-play data set](http://www.advancednflstats.com/2010/04/play-by-play-data.html) for ingest into a relational database. The primary contribution is parsing the text descriptions of plays to determine the type of play (i.e. run or pass) and how drives ended. The project also includes a simple web application for filtering the plays and generating some play and drive statistics. A running version of this application can be found here: [http://football.10flow.com](http://football.10flow.com).

Components
----------

### raw-data

This folder contains CSV files of the raw AdvancedNFLStats.com dataset, as downloaded from Google Docs at the end of the 2012 regular season. Check the original source for updates.

### play-parser

This folder contains Python scripts for parsing the text play descriptions and ingesting them into a relational database. The main script to run is `play_parser.py`. There are some configuration settings at the top of that file you should check out before running. If you wish to ingest plays into a database, [SQLAlchemy](http://www.sqlalchemy.org) is required, as well as a supported database, such as SQLite, MySQL or PostgreSQL.

### web

This folder contains the responsive web application for filtering the plays and viewing simple statistics. `index.html` contains all markup and Javascript. Queries are handled by `football.php`, which issues SQL queries to the database and returns JSON for visualization.

Adding Plays
------------

The Python script `play-parser/add_plays.py` is designed to make it easy to insert new plays into the database. Run `python add_plays.py --help` for usage information:

	usage: add_plays.py [-h] [-f OUTPUTFILETYPE] [-t] infiles [infiles ...] output
	
	positional arguments:
	  infiles               one or more CSV files downloaded from
	                        http://www.advancednflstats.com/2010/04/play-by-play-
	                        data.html
	  output                database connection string (example:
	                        'mysql+mysqldb://user:password@hostname/mydatabase')
	                        or output filename when used with --fileout option
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -f OUTPUTFILETYPE, --outputfiletype OUTPUTFILETYPE
	                        output parsed plays to file of specified format
	                        instead of database ('json' or 'csv')
	  -t, --createtable     create the 'plays' database table

Standard usage would be to add a CSV file containing new plays to the database from the command line as follows: `python add_plays.py ../raw-data/new_plays.csv mysql+mysqldb://user:password@hostname/mydatabase`, where `user`, `password`, `hostname`, and `mydatabase` refer to the database username, password, hostname and database name, respectively. Note, [SQLAlchemy](http://www.sqlalchemy.org) and Python 2.x are required to run this script.

Data Enrichment Example
-----------------------

The Python scripts in the `play-parser` folder are designed to be easily extended. Suppose you wanted to add a column to the database that reports the number of characters in the text description of the play (I know this is useless, but it makes a good example). You just need to make a few changes:

**Step 1:** Make changes to `play_db.py` to add the column to the database. On **line 28** add:

	length = Column(Integer)

On **line 49** add:

	self.length = p['length']

**Step 2:** Create a play processor that analyzes the play and generates a value a `length`. To do this, create a new script called `process_length.py` and add this code:

	class LengthProcessor:
	  def process(self, play):
	    play.columns['length'] = len(play.columns['description'])

**Step 3:** Register this new processor, by adding these lines to `play_parser.py` at **line 44**:

	import process_length
	processors.append(process_length.LengthProcessor)

That's it!

Credits
-------

This project was created by [Scott Sawyer](http://www.10flow.com). It includes portions of the following projects:

- [Foundation](http://foundation.zurb.com)
- [jQuery](http://www.jquery.com)
- [jqPlot](http://www.jqplot.com)

License
-------

This software is provided under the MIT License:

	Copyright (c) 2013 Scott Sawyer
	
	Permission is hereby granted, free of charge, to any person
	obtaining a copy of this software and associated documentation
	files (the "Software"), to deal in the Software without
	restriction, including without limitation the rights to use,
	copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the
	Software is furnished to do so, subject to the following
	conditions:
	
	The above copyright notice and this permission notice shall be
	included in all copies or substantial portions of the Software.
	
	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
	OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
	NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
	HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
	WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
	FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
	OTHER DEALINGS IN THE SOFTWARE.
