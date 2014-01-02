import csv
import play as play_module


class OutputFormat:
    JSON = 0
    CSV = 1
    DATABASE = 2


def play_parser(in_files, out_str, out_format, create_table):
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
    play = play_module.PlayData()

    print('Processing Plays...')
    for csv_file in in_files:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for raw_row in reader:
                play = play.next_play_data_factory(raw_row)
                for processor in processors:
                    processor.process(play)
                plays.append(play.columns)

    #write to JSON
    if out_format == OutputFormat.JSON:
        print('Writing to JSON...')
        import json
        with open(out_str, 'w') as f:
            json.dump(plays, f)

    #write to CSV
    elif out_format == OutputFormat.CSV:
        print('Writing to CSV...')
        #import csv
        header = list(plays[0].keys())
        #header.remove('description')
        with open(out_str, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            for play in plays:
                #del play['description']
                writer.writerow(play)

    #database ingest
    else:
        from plays_db import Base, ingest
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        print('Connecting to database...')
        database_engine = create_engine(out_str, echo=False)
        print('Writing to database (this will take a while)...')
        if create_table:
            Base.metadata.create_all(database_engine)
        Session = sessionmaker(bind=database_engine)
        session = Session()
        ingest(plays, session)
