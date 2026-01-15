from pynput import keyboard
from pynput.keyboard import Key, Controller
import os
import sys

class HD2MiniGame() :
    '''
    *stratType* : str = None, pass through which specific stratagem type to ONLY use OR pass nothing for ALL types. Stratagem types include :
    'Offensive: Orbital', 'Offensive: Eagle', 'Supply: Support Weapons', 'Supply: Backpacks', 'Supply: Vehicles', 'Defensive', 'Mission Stratagems'
    Anything else will result in the program crashing!
    *arrowify* : bool = True, this determines if arrows will show (🠉) or raw text (keyboard.Key.up), it is preferred to keep this setting on.
    '''
    
    def __init__(self, stratType : str = None, arrowify : bool = True) -> None:
        
        stratType = stratType
        arrowify = arrowify
        self.isArrow                    = arrowify
        self.run                        = True
        self.score                      = 0
        self.stratagemsStorage          = None
        self.stratagems = {
            'Offensive: Orbital'        : None,
            'Offensive: Eagle'          : None,
            'Supply: Support Weapons'   : None,
            'Supply: Backpacks'         : None,
            'Supply: Vehicles'          : None,
            'Defensive'                 : None,
            'Mission Stratagems'        : None
        }
        self.playerStorage              = None
        self.playerStatsStorage         = None
        self.playerData = {
            'player'                    : None,
            'playerID'                  : None,
            'player_stats' : {
                'highscore'             : None,
                'keys_pressed'          : None,
                'inputs_correct'        : None,
                'inputs_wrong'          : None,
                'attempts'              : None,
                'time_elapsed'          : None
            }
        }
        self.arrowCodes = {
            'up_arrow'                  : '🠉',
            'down_arrow'                : '🠋',
            'left_arrow'                : '🠈',
            'right_arrow'               : '🠊'
        }
        self.playerStats = self.playerData['player_stats']
        try :
            self.__initJSON__()
            strat1 = self.random_stratagem(stratType='Offensive: Eagle')
            strat2 = self.random_stratagem(arrowify=False)
            print("TEST RANDOM STRATS\n----------------------------\nSTRATAGEM 1: ",strat1,"\nSTRATAGEM 2: ",strat2,"\n----------------------------", sep="")
            self.runMain(stratType=stratType, arrowify=arrowify)
        except Exception as e:
            print(f"ERROR: Running class init functions -> {e}")
    
    @staticmethod
    def findPath(name: str, path: str) -> str | None:
        '''
        find any specified path using a root path, edit exclude for large, unnecessary directories
        PARAMS
        :name: = str() name of file/directory to find
        :path: = str() root path to search onward from
        '''
        exclude = set(['.venv', '.vscode'])
        for root, dirs, files in os.walk(path, topdown=True):
            dirs[:] = [d for d in dirs if d not in exclude]
            if name in files:
                return os.path.join(root, name)
    
    def __initJSON__(self) -> None :
        '''
        fetch JSON contents for stratagems and player data
        '''
        import json
        #load all the stratagems in .\HD2minigm\stratagems.json
        print("INITIALIZING stratagems.json...",end="..")
        path            =   os.getcwd()
        newPath         =   self.findPath("HD2minigm_main.py", path)
        newPath         =   newPath.removesuffix("\\HD2minigm_main.py")
        path            =   os.chdir(newPath)
        cwd             =   os.getcwd()
        stratagemsJson  =   None
        stratagemsPath  =   cwd+"\\stratagems.json"
        
        try :
            with open(stratagemsPath, 'r', encoding='utf-8') as file :
                print("OK\nLOADING JSON...",end="..")
                data = json.load(file)
                if data is not None :
                    print("OK")
                else : raise json.JSONDecodeError
                
            try :
                print("LOADING STRATAGEMS...",end="..")
                stratagemsJson = data['stratagems']
                self.stratagemsStorage = stratagemsJson[0]
                self.stratagems['Offensive: Orbital']       =   self.stratagemsStorage['Offensive: Orbital']
                self.stratagems['Offensive: Eagle']         =   self.stratagemsStorage['Offensive: Eagle']
                self.stratagems['Supply: Support Weapons']  =   self.stratagemsStorage['Supply: Support Weapons']
                self.stratagems['Supply: Backpacks']        =   self.stratagemsStorage['Supply: Backpacks']
                self.stratagems['Supply: Vehicles']         =   self.stratagemsStorage['Supply: Vehicles']
                self.stratagems['Defensive']                =   self.stratagemsStorage['Defensive']
                self.stratagems['Mission Stratagems']       =   self.stratagemsStorage['Mission Stratagems']
            except Exception as e :
                print(f"ERROR: Loading stratagems -> {e}")
            else :
                print("OK")
        except FileNotFoundError:
            print(f"ERROR: The file '{path}' was not found")
        except json.JSONDecodeError:
            print("ERROR: Failed to decode JSON from the file (invalid syntax)")
            
        #load all the scores in .\HD2minigm\players.json
        print("INITALIZING players.json...",end="..")
        path            =   os.getcwd()
        newPath         =   self.findPath("HD2minigm_main.py", path)
        newPath         =   newPath.removesuffix("\\HD2minigm_main.py")
        path            =   os.chdir(newPath)
        cwd             =   os.getcwd()
        playersJson     =   None
        playersPath     =   cwd+"\\players.json"
        
        try :
            with open(playersPath, 'r', encoding='utf-8') as file:
                print("OK\nLOADING JSON...",end="..")
                data = json.load(file)
                if data is not None :
                    print("OK")
                else : raise json.JSONDecodeError
                
            try :
                print("LOADING PLAYER DATA...",end="..")
                playersJson = data['players']
                self.playerStorage = playersJson[0]
                self.playerStatsStorage = self.playerStorage['player_stats'][0]
                self.playerData['player']           =   self.playerStorage['player']
                self.playerData['playerID']         =   self.playerStorage['playerID']
                self.playerStats['highscore']       =   self.playerStatsStorage['highscore']
                self.playerStats['keys_pressed']    =   self.playerStatsStorage['keys_pressed']
                self.playerStats['inputs_correct']  =   self.playerStatsStorage['inputs_correct']
                self.playerStats['inputs_wrong']    =   self.playerStatsStorage['inputs_wrong']
                self.playerStats['attempts']        =   self.playerStatsStorage['attempts']
                self.playerStats['time_elapsed']    =   self.playerStatsStorage['time_elapsed']
            except Exception as e :
                print(f"ERROR: Loading player data -> {e}")
            else:
                print("OK")
        
        except FileNotFoundError:
            print(f"ERROR: The file '{path}' was not found")
        except json.JSONDecodeError:
            print("ERROR: Failed to decode JSON from the file (invalid syntax)")
        
        
        #keep on bottom of func
        del path, newPath, cwd, stratagemsJson, stratagemsPath, playersJson, playersPath, data, json
        return
    
    def check_input(self, stratKeys, stratLength) :
        #holy if statements, but honestly I have no clue how else to do it, feel free to optimize for me lol
        keyBoard = Controller()
        if self.keyList :
            if self.keyList[0] == stratKeys[0] :
                if len(self.keyList) > 1 :
                    if self.keyList[1] == stratKeys[1] :
                        if len(self.keyList) > 2 :
                            if self.keyList[2] == stratKeys[2] :
                                if stratLength == 3 :
                                    self.correct_sequence = True
                                    print("|",end="")
                                    print("\nCorrect, good Job!")
                                    keyboard.Listener.stop
                                    keyBoard.press(Key.right)
                                    keyBoard.release(Key.right)
                                    return
                                elif len(self.keyList) > 3 :
                                    if self.keyList[3] == stratKeys[3] :
                                        if stratLength == 4 :
                                            self.correct_sequence = True
                                            print("|",end="")
                                            print("\nCorrect, good Job!")
                                            keyboard.Listener.stop
                                            keyBoard.press(Key.right)
                                            keyBoard.release(Key.right)
                                            return
                                        elif len(self.keyList) > 4:
                                            if self.keyList[4] == stratKeys[4] :
                                                if stratLength == 5 :
                                                    self.correct_sequence = True
                                                    print("|",end="")
                                                    print("\nCorrect, good Job!")
                                                    keyboard.Listener.stop
                                                    keyBoard.press(Key.right)
                                                    keyBoard.release(Key.right)
                                                    return
                                                elif len(self.keyList) > 5 :
                                                    if self.keyList[5] == stratKeys[5] :
                                                        if stratLength == 6 :
                                                            self.correct_sequence = True
                                                            print("|",end="")
                                                            print("\nCorrect, good Job!")
                                                            keyboard.Listener.stop
                                                            keyBoard.press(Key.right)
                                                            keyBoard.release(Key.right)
                                                            return
                                                        elif len(self.keyList) > 6 :
                                                            if self.keyList[6] == stratKeys[6] :
                                                                if stratLength == 7 :
                                                                    self.correct_sequence = True
                                                                    print("|",end="")
                                                                    print("\nCorrect, good Job!")
                                                                    keyboard.Listener.stop
                                                                    keyBoard.press(Key.right)
                                                                    keyBoard.release(Key.right)
                                                                    return
                                                                elif len(self.keyList) > 7 :
                                                                    if self.keyList[7] == stratKeys[7] :
                                                                        if stratLength == 8 :
                                                                            self.correct_sequence = True
                                                                            print("|",end="")
                                                                            print("\nCorrect, good Job!")
                                                                            keyboard.Listener.stop
                                                                            keyBoard.press(Key.right)
                                                                            keyBoard.release(Key.right)
                                                                            return
                                                                        elif len(self.keyList) > 8 :
                                                                            #8 keys should be the longest input.
                                                                            self.keyList = []
                                                                    else : self.keyList = []
                                                                else : return
                                                            else :
                                                                print("|",end="")
                                                                print("\nIncorrect, try again!")
                                                                print(f"\n----------------------------\nInput the correct sequence!\n\n{self.stratagem['name']}\n{self.stratagem['input_code']}\n")
                                                                self.keyList = []
                                                        else : return
                                                    else :
                                                        print("|",end="")
                                                        print("\nIncorrect, try again!")
                                                        print(f"\n----------------------------\nInput the correct sequence!\n\n{self.stratagem['name']}\n{self.stratagem['input_code']}\n")
                                                        self.keyList = []
                                                else : return
                                            else :
                                                print("|",end="")
                                                print("\nIncorrect, try again!")
                                                print(f"\n----------------------------\nInput the correct sequence!\n\n{self.stratagem['name']}\n{self.stratagem['input_code']}\n")
                                                self.keyList = []
                                        else : return
                                    else :
                                        print("|",end="")
                                        print("\nIncorrect, try again!")
                                        print(f"\n----------------------------\nInput the correct sequence!\n\n{self.stratagem['name']}\n{self.stratagem['input_code']}\n")
                                        self.keyList = []
                                else : return
                            else :
                                print("|",end="")
                                print("\nIncorrect, try again!")
                                print(f"\n----------------------------\nInput the correct sequence!\n\n{self.stratagem['name']}\n{self.stratagem['input_code']}\n")
                                self.keyList = []
                        else : return
                    else :
                        print("|",end="")
                        print("\nIncorrect, try again!")
                        print(f"\n----------------------------\nInput the correct sequence!\n\n{self.stratagem['name']}\n{self.stratagem['input_code']}\n")
                        self.keyList = []
                else : return
            else :
                print("|",end="")
                print("\nIncorrect, try again!")
                print(f"\n----------------------------\nInput the correct sequence!\n\n{self.stratagem['name']}\n{self.stratagem['input_code']}\n")
                self.keyList = []
        return
    
    def on_key_release_strat(self, key) :
        stratKeys = self.stratagem['input_code']
        stratLength = len(self.stratagem['input_code'])
        if self.correct_sequence == True:
            keyboard.Listener.stop
            return False
        else:
            if key == Key.right :
                sys.stdout.write(" 🠊 ")
                if not self.isArrow : self.keyList.append('keyboard.Key.right')
                else : self.keyList.append(self.arrowCodes['right_arrow'])
                self.check_input(stratKeys, stratLength)
            elif key == Key.left :
                sys.stdout.write(" 🠈 ")
                if not self.isArrow : self.keyList.append('keyboard.Key.left')
                else : self.keyList.append(self.arrowCodes['left_arrow'])
                self.check_input(stratKeys, stratLength)
            elif key == Key.down :
                sys.stdout.write(" 🠋 ")
                if not self.isArrow : self.keyList.append('keyboard.Key.down')
                else : self.keyList.append(self.arrowCodes['down_arrow'])
                self.check_input(stratKeys, stratLength)
            elif key == Key.up :
                sys.stdout.write(" 🠉 ")
                if not self.isArrow : self.keyList.append('keyboard.Key.up')
                else : self.keyList.append(self.arrowCodes['up_arrow'])
                self.check_input(stratKeys, stratLength)
            elif key == Key.esc :
                print("Quitting..")
                keyboard.Listener.stop
                self.run = False
                return False

    def on_key_release_exit(self, key) :
        if key == Key.esc :
            print('Quitting!')

    def random_stratagem(self, stratType : str = None, arrowify : bool = True) -> dict:
        '''
        *stratType* is a string specifying which kind of stratagem is wanted i.e. 'Offensive: Eagle' *CASE SENSITIVE* by default it will use any and all types, including mission stratagems
        \n\t*arrowify* is a boolean which enables converting stratagem input to arrow characters rather than the raw key. NOT recommended to turn off!
        '''
        import random as ran
        #this could likely be condensed further I just honestly don't see how, I can feel it tho..
        stratagem = dict
        if stratType is not None :
            stratagem = self.stratagems[stratType][ran.randrange(0, len(self.stratagems[stratType]), 1)]
        elif stratType == None :
            i = ran.choice(['Offensive: Orbital', 'Offensive: Eagle', 'Supply: Support Weapons', 'Supply: Backpacks', 'Supply: Vehicles', 'Defensive', 'Mission Stratagems'])
            stratagem = self.stratagems[i][ran.randrange(0, len(self.stratagems[i]), 1)]
        else :
            raise ValueError
        #change stratagem input to arrows
        if arrowify:
            for i in range(len(stratagem['input_code'])):
                if stratagem['input_code'][i] == 'keyboard.Key.up' : stratagem['input_code'][i] = stratagem['input_code'][i].replace('keyboard.Key.up', self.arrowCodes['up_arrow'])
                if stratagem['input_code'][i] == 'keyboard.Key.down' : stratagem['input_code'][i] = stratagem['input_code'][i].replace('keyboard.Key.down', self.arrowCodes['down_arrow'])
                if stratagem['input_code'][i] == 'keyboard.Key.left' : stratagem['input_code'][i] = stratagem['input_code'][i].replace('keyboard.Key.left', self.arrowCodes['left_arrow'])
                if stratagem['input_code'][i] == 'keyboard.Key.right' : stratagem['input_code'][i] = stratagem['input_code'][i].replace('keyboard.Key.right', self.arrowCodes['right_arrow'])
        del ran
        return stratagem

    def runMain(self, stratType : str = None, arrowify : bool = True) :
        print('\n'*10)
        self.stratagem = None
        self.keyList = []
        self.correct_sequence = False
        print("Press ESC to quit the program!\n")
        while self.run :
            self.stratagem = self.random_stratagem(stratType, arrowify)
            while True :
                if self.stratagem is not None:
                    print(f"\n----------------------------\nInput the correct sequence!\n\n{self.stratagem['name']}\n{self.stratagem['input_code']}\n")
                    print("|",end="")
                    with keyboard.Listener(on_press=self.on_key_release_strat) as listener:
                        listener.join()
                    if self.correct_sequence :
                        self.score += 1
                        self.keyList = []
                        self.correct_sequence = False
                        break
                    if self.run == False : break
                else :
                    print("ERROR: stratagem found as : None")
                    raise ValueError
        self.exitSeq()
        return
    
    def exitSeq(self) :
        print(f"Your score was :\t{self.score}")
        exit()
    
if __name__ == "__main__" :
    HD2MiniGame()