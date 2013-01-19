class PlaytypeProcessor:

    #Determine if play is run or pass. Note drives that
    #end in turnovers or touchdowns.

    def process(self,play):
        play.columns['yards'] = 0
        if not play.is_play:
            play.columns['type'] = 'n/a'
        else:
            d_words = play.desc_words #abbreviation
            d = play.desc_lower
            #play type
            if ('pass' in d_words) or ('sacked' in d_words) or ('passed' in d_words):
                play.columns['type'] = 'pass'
            elif ('yards' in d_words or 'yards.' in d_words or 'no gain' in d or 
                'yard' in d_words or 'yard.' in d_words):
                    play.columns['type'] = 'run'
            elif ('fumbles' in d_words):
                play.columns['type'] = 'pass'
            else:
                play.columns['type'] = 'n/a'
                #print 'Unknown play type: ' + d
            
            #yardage
            yards = '?'
            if 'incomplete' in d_words or 'incomplete.' in d_words:
                yards = 0
            if 'no gain' in d:
                yards = 0
            i = []
            for item in ['yards','yards.','yard','yard.']:
                if item in d_words:
                    i.append(d_words.index(item))
            if len(i) > 0:
                i = min(i)
                try:
                    yards = int(d_words[i-1])
                except ValueError:
                    yards = '?'
            if yards == '?':
                #print 'Unknown yardage: ' + d
                yards = 0
                
            play.columns['yards'] = yards
            
            first_down = yards >= play.columns['togo']
            
            #downs
            if (play.columns['down'] == 4) and (not first_down):
                play.columns['result'] = 'downs'
            
            #turnovers
            if 'intercepted' in d_words or 'intercepted.' in d_words:
                play.columns['result'] = 'int'
            if ('fumbles' in d_words) and ('recovered' in d_words):
                #who recovered
                i = d_words.index('recovered')
                recovered = d_words[i+2].split('-')[0] #recovered by X
                if recovered == play.columns['def'].lower():
                    play.columns['result'] = 'fumble'
                elif recovered != play.columns['off'].lower():
                    pass
                    #print 'Who recovered the fumble? ' + d
                    
            #touchdown
            if 'TOUCHDOWN' in play.columns['description']:
                play.columns['result'] = 'td'
        
            
