Play-By-Play Effectiveness Tools
================================

This project parses [AdvancedNFLStats.com's play-by-play data set](http://www.advancednflstats.com/2010/04/play-by-play-data.html) for ingest into a relational database. The primary contribution is parsing the text descriptions of plays to determine the type of play (i.e. run or pass) and how drives ended. The project also includes a simple web application for filtering the plays and generating some play and drive statistics. A running version of this application can be found here: [http://football.10flow.com](http://football.10flow.com).

If you would like to contribute, please check issues for ideas.

Components
----------

### raw-data

This folder contains CSV files of the raw AdvancedNFLStats.com dataset, as downloaded from Google Docs at the end of the 2012 regular season. Check the original source for updates.

### play-parser

This folder contains Python scripts for parsing the text play descriptions and ingesting them into a relational database. The main script to run is `play_parser.py`. There are some configuration settings at the top of that file you should check out before running. If you wish to ingest plays int oa database, [SQLAlchemy](http://www.sqlalchemy.org) is required, as well as a supported database, such as SQLite, MySQL or PostgreSQL.

### web

This folder contains the responsive web application for filtering the plays and viewing simple statistics. `index.html` contains all markup and Javascript. Queries are handled by `football.php`, which issues SQL queries to the database and returns JSON for visualization.

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
