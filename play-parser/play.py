class PlayData:
    def __init__(self,raw_row=None):
        #no raw_row
        if raw_row is None:
            raw_row = {'gameid':'','season':'','off':'','def':'','down':'',
                'togo':'','qtr':'','min':'','sec':'','offscore':'',
                'defscore':'','ydline':'','qtr':'','description':''}
        columns = {}
        #copy these fields
        columns['gameid'] = raw_row['gameid']
        columns['season'] = to_num(raw_row['season'])
        columns['off'] = raw_row['off']
        columns['def'] = raw_row['def']
        columns['down'] = to_num(raw_row['down'])
        columns['togo'] = to_num(raw_row['togo'])
        columns['qtr'] = raw_row['qtr']
        columns['min'] = to_num(raw_row['min'], 60)
        columns['sec'] = to_num(raw_row['sec'])
        columns['offscore'] = to_num(raw_row['offscore'])
        columns['defscore'] = to_num(raw_row['defscore'])
        columns['ydline'] = to_num(raw_row['ydline'])
        columns['description'] = raw_row['description']
        
        #store some helpful information
        columns['scorediff'] = columns['offscore'] - columns['defscore']
        self.columns = columns
        self.desc_lower = columns['description'].lower()
        self.desc_words = self.desc_lower.split(" ")
        
    def next_play_data_factory(self,raw_row):
        new_play = PlayData(raw_row)
        new_play.last = self
        self.last = None
        return new_play
    
def to_num(s, default=0):
    if s.isdigit():
        return int(s)
    else:
        return default
