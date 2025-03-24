import sys
import actions.open_application
import actions.open_website
import actions.change_volume
import actions.trigger_hotkey
import actions.change_page


class Action:
    def __init__(self, name, key, act_type, args):
        self.name = name
        self.act_type = act_type
        self.key = key
        ## string with comma separated values
        self.args = args
    
    def perform_action(self):
        mod_str = f"actions.{self.name}"
        ##load the moudule from actions
        mod = sys.modules.get(mod_str)
        
        ## build a function with the module and function name
        f_to_run = getattr(mod, self.name)

        print(f"args = {self.args}")
        args_l = self.args.split(",")


        # ## finally run the function
        f_to_run(*args_l)



