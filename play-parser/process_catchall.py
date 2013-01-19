class CatchallProcessor:

    #Catch weird ends to drives
    
    def process(self, play):
        if ('result' in play.last.columns) and \
            (play.last.columns['result'] == 'play') and \
            (play.last.columns['off'] != play.columns['off']) and \
            ('kicks' not in play.last.desc_words):
                play.last.columns['result'] = 'other'
                #print 'Weird case: drive end not detected -- ' + play.columns['description']
