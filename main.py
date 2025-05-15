#from sasConnection import SasConnection
import argparse
import tkinter as tk
from gui.gui_interface import MainFrame

def run_gui():
    root = tk.Tk()
    root.title("SAS Connection")
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit())
    #root.resizable(False,False)
    app = MainFrame(root)
    root.focus_force()
    root.mainloop()

def main():
    parser = argparse.ArgumentParser(
        prog = "SAS connection host parser Implementation",
        description = "Python script that sends and receives messages from a gaming machines",
        epilog = "this stuff is still under construction so xd"
    )

    subparsers = parser.add_subparsers(dest="mode", help = "Execution mode")

    ##CONFIG FILE:
    config_parser = subparsers.add_parser("configfiles", help = "Run using a configuration file")
    config_parser.add_argument("file", type=str, help = "Path to JSON configuration file")

    #CLI flags mode
    flags_parser = subparsers.add_parser("cli", help = "Run using command-line arguments")
    flags_parser.add_argument("--port", type=str, required = True, help = "Port name for serial connection")
    flags_parser.add_argument("--address", type=int, required = True, help = "Gaming machine SAS address")
    
    #GUI mode
    gui_parser = subparsers.add_parser("gui", help = "Run in GUI mode")

    args = parser.parse_args()

    if args.mode is None or args.mode == "gui":
        print("start in GUI mode")
        run_gui()
    elif args.mode == "configfile":
        print("start in configFile mode")
    elif args.mode == "cli":
        print("start in cli mode")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

