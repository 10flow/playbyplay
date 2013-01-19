from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()

class Play(Base):
    __tablename__ = 'plays'
    
    id = Column(Integer, primary_key=True)
    gameid = Column(String(16))
    season = Column(Integer)
    defense = Column(String(3), index=True)
    defscore = Column(Integer)
    down = Column(Integer)
    minutes = Column(Integer)
    offense = Column(String(3), index=True)
    offscore = Column(Integer)
    quarter = Column(Integer)
    result = Column(String(10), index=True)
    scorediff = Column(Integer, index=True)
    seconds = Column(Integer)
    success = Column(Integer)
    togo = Column(Integer)
    playtype = Column(String(4))
    yards = Column(Integer, index=True)
    yardline = Column(String(3))
    description = Column(Text)
    
    def populate(self, p):
        self.gameid = p['gameid']
        self.season = p['season']
        self.defense = p['def']
        self.defscore = p['defscore']
        self.down = p['down']
        self.minutes = p['min']
        self.offense = p['off']
        self.offscore = p['offscore']
        self.quarter = p['qtr']
        self.result = p['result']
        self.scorediff = p['scorediff']
        self.seconds = p['sec']
        self.success = p['success']
        self.togo = p['togo']
        self.playtype = p['type']
        self.yards = p['yards']
        self.yardline = p['ydline']
        self.description = p['description'].encode('ascii','ignore')
    
    
def ingest(plays, session):
    for i,p in enumerate(plays):
        if (i % 1000 == 0) and i != 0:
            print str(i) + ' plays written'
        play = Play()
        play.populate(p)
        session.add(play)
        session.commit()
        
