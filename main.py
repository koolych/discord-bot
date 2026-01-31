import utils
import os

def main():
    os.system("cls" if os.name == "nt" else "clear")
    config = utils.Config.read()
    utils.bot.run(config["token"], log_handler = None)

if __name__ == "__main__":
    main()