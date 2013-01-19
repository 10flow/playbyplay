class ResultProcessor:
    
    #Determines if this is an offensive play. If not, note
    #how the drive ended (if applicable).
    
    def process(self, play):
        #default
        play.columns['result'] = 'play'
        
        #1. Handle drives that end at the buzzer
        fix_last_result = ''
        last_qtr = play.last.columns['qtr']
        qtr = play.columns['qtr']
        #halftime -- if last qtr is 2 and this qtr is 3
        if last_qtr == '2' and qtr == '3':
            fix_last_result = 'half'
        
        #end of if last qtr is 4 or 5 and this qtr is 1
        elif (last_qtr == '4' or last_qtr == '5') and qtr == '1':
            if play.last.columns['scorediff'] > 0:
                fix_last_result = 'win'
            elif play.last.columns['scorediff'] < 0:
                fix_last_result = 'loss'
            else:
                fix_last_result = 'tie'
                
        #overtime if last qtr is 4 and this qtr is 5
        elif last_qtr == '4' and qtr == '5':
            fix_last_result = 'ot'
            
        #fix the last result if necessary
        if (fix_last_result != '') and (play.last.columns['result'] == 'play'):
            play.last.columns['result'] = fix_last_result
            
            
        #2. Handle reversed plays (remove the play description that was reversed)
        word = ''
        if 'reversed' in play.desc_words:
            word = 'reversed'
        elif 'reversed.' in play.desc_words:
            word = 'reversed.'
        if word != '':
            play.desc_lower = play.desc_lower.split(word)[-1]
            i = play.desc_words.index(word)
            play.desc_words = play.desc_words[i+1:]
        
        
        #3. Is it an offensive play?
        play.is_play = True
        if play.columns['down'] == 0:
            play.is_play = False
        else:
            if 'spiked' in play.desc_words:
                play.is_play = False
                
            if ('penalty' in play.desc_words) and not ('declined' in play.desc_words) \
                and not ('declined.' in play.desc_words):
                    play.is_play = False
                    
            if ('penalty' in play.desc_words):
                    if play.desc_words.index('penalty') <= 2:
                        play.is_play = False
                                    
            if 'punts' in play.desc_words:
                play.is_play = False
                play.columns['result'] = 'punt'
            elif 'field goal' in play.desc_lower:
                play.is_play = False
                if 'is good' in play.desc_lower:
                    play.columns['result'] = 'fg'
                else:
                    play.columns['result'] = 'miss'
            
        
        
        
