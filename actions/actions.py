import sys
import actions.open_application
import actions.open_website
import actions.change_volume
from configs.page_key_action_map import page_key_action_map

# # func_name = list(page_key_action_map.get("pages").get("1").get("buttons").get("0").get("actions").keys())

# # print(f" function = {func_name}")

# # f = getattr(actions, func_name)

# # f("firefox")

## load all actions from the mapping dicionary
def get_all_actions(page, button):
    ## create a list of tupels with all the actions and args.
    res = list(page_key_action_map.get("pages").get(f"{page}").get("buttons").get(f"{button}").get("actions").items())
    return res

def perform_action(acts):
    for a, args in acts:
        print(f"{a}, {args}")
        ## build module name string
        mod_str = f"actions.{a}"
        ##load the moudule from actions
        mod = sys.modules.get(mod_str)
        print(f"{mod}")

        ## build a function with the module and function name
        f_to_run = getattr(mod, a)

        ## rinally run the function
        f_to_run(args)



