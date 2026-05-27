from scripts.game_states.dialogue_state import SceneState, DialogueState, DescriptionState

def get_flag(game, flag:str) -> bool:
        if flag in game.flags:
            return True
        return False

def trigger_scene_dialogue(game, scene:str, interaction_id:int):
        dialogue_box = SceneState(game, 'dialogue_test.json', scene, interaction_id)
        dialogue_box.enter_state()
        return

def trigger_character_dialogue(game, character_name:str, interaction_id:int):
        dialogue_box = DialogueState(game, character_name, character_name + '_test.json', interaction_id)
        dialogue_box.enter_state()
        return

def trigger_description_dialogue(game, obj):
        description_state = DescriptionState(game, obj)
        description_state.enter_state()
        return