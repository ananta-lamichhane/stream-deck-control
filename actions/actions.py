import sys
import actions.open_application
import actions.open_website
import actions.change_volume
import actions.trigger_hotkey
import actions.change_page

def perform_action(acts):
    for a, args in acts:

        ## build module name string
        mod_str = f"actions.{a}"
        ##load the moudule from actions
        mod = sys.modules.get(mod_str)


        ## build a function with the module and function name
        f_to_run = getattr(mod, a)

        print(f"args = {args}")
        args_l = args.split(",")
        print(f"all_args = {args_l}")

        ## rinally run the function
        f_to_run(*args_l)



