class SuccessProcessor:

    #If play is run or pass, classify it as success or failure.
    good = ['td', 'win']
    bad = ['downs','fumble','int','loss','miss','punt']

    def process(self, play):
        play.columns['success'] = False #default
        if (play.columns['type'] == 'pass') or (play.columns['type'] == 'run'):
            #good outcome
            if play.columns['result'] in self.good:
                play.columns['success'] = True

            #bad outcome
            elif play.columns['result'] in self.bad:
                play.columns['success'] = False
                
            #1st or 2nd down, 4+ yards
            elif (play.columns['down'] < 3) and (play.columns['yards'] >= 4):
                play.columns['success'] = True
            
            #got the first down
            elif play.columns['yards'] >= play.columns['togo']:
                play.columns['success'] = True
                
            else:
                play.columns['success'] = False
