class DialogueManager:
    """
    Checks game flags and decides which interactions to run
    """
    def __init__(self, game):
        self.game = game

    def check_conditions(self, data):
        current_flags:set = self.game.flags
        data_flags:list = data.get('requires', []) # Return empty list if no requires key is found

        for req_flag in data_flags: # If data flags is empty list you will not enter for loop
            if req_flag not in current_flags:
                return False
        return True
    
    def select_interaction(self, dialogue_json:dict):
        valid = []

        for key, data in dialogue_json.items(): # Tuple unpacking
            repeatable = data.get('repeatable', True) # Return True if no repeatable value is found

            if repeatable == False:
                if key in self.game.used_interactions:
                    print(key)
                    continue

            if self.check_conditions(data):
                valid.append((key, data))
        
        if not valid: # if valid is not an empty list
            return None
        
        # Picks the highest priority data from the list of valid dialogues
        best_key, best_data = max(valid, key=lambda x: x[1].get('priority', 0))
        return best_key, best_data
    
    def select_scene_interaction(self, scene:str, dialogue_json:dict):
        valid = []
        # print(f"scene: {scene}")
        # print(f"json: {dialogue_json}")
        for key, data in dialogue_json[scene].items(): # Tuple unpacking
            repeatable = data.get('repeatable', True) # Return True if no repeatable value is found
            # print(repeatable)
            if repeatable == False:
                # print(key)
                if key in self.game.used_interactions:
                    # print(key)
                    continue

            if self.check_conditions(data):
                valid.append((key, data))
        
        if not valid: # if valid is not an empty list
            return None
        
        # Picks the highest priority data from the list of valid dialogues
        best_key, best_data = max(valid, key=lambda x: x[1].get('priority', 0))
        # print(valid)
        return best_key, best_data        
    
# example: valid = [('intro', {'priority': 0, ...}), ('repeat', {'priority': 1, ...})]
# key is an optional argument in the max() function which lets you modify an object before comparison or compare based on specific index/attribute
# if we just do max(valid) it would look at each tuple at index 1 and get the largest alpabetically ordered string
# what we need is the max priority number in the data for that we use the key= argument
# lambda is a one line anonymous function 
# what were doing when we do key=lambda x: x[1].get('priority', 0) is...
# ('intro', {'priority': 0, ...}) take this tuple and go to index 1 which is our data and return the priority value/num. If its not found return 0 
# finally get the largest of the priority numbers we got.