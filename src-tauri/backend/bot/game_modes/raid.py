import random
from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode


class RaidException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Raid:
    """
    Provides the navigation and any necessary utility functions to handle the Raid game mode.
    """

    _raids_joined = 0
    _GRID_SECTIONS = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]]

    # List of supported raids in the format of "X,Y,Z":
    # X = 1 for Standard tab or 2 for Impossible tab.
    # Y = Position in the 3xN grid reading from left to right, top to bottom.
    # Z = Position in the list reading from top to bottom.
    _list_of_raids = {
        ########## Standard Tab ##########
        # 2 stars
        "Lvl 50 Tiamat Omega": "1,2,1",
        "Lvl 70 Colossus Omega": "1,2,2",
        "Lvl 60 Leviathan Omega": "1,2,3",
        "Lvl 60 Yggdrasil Omega": "1,2,4",
        "Lvl 75 Luminiera Omega": "1,2,5",
        "Lvl 75 Celeste Omega": "1,2,6",

        # 3 stars
        "Lvl 100 Athena": "1,3,1",
        "Lvl 100 Grani": "1,3,2",
        "Lvl 100 Baal": "1,3,3",
        "Lvl 100 Garuda": "1,3,4",
        "Lvl 100 Odin": "1,3,5",
        "Lvl 100 Lich": "1,3,6",

        # 4 stars
        "Lvl 100 Grand Order": "1,4,1",
        "Lvl 100 Proto Bahamut": "1,4,2",
        "Lvl 100 Huanglong": "1,4,3",
        "Lvl 100 Qilin": "1,4,4",

        # 5 stars
        "Lvl 100 Michael": "1,5,1",
        "Lvl 100 Gabriel": "1,5,2",
        "Lvl 100 Uriel": "1,5,3",
        "Lvl 100 Raphael": "1,5,4",

        # 6 stars
        "Lvl 150 Ultimate Bahamut": "1,6,1",

        ########## Impossible Tab ##########
        # 1 stars
        "Lvl 100 Tiamat Omega Ayr": "2,1,1",
        "Lvl 100 Colossus Omega": "2,1,2",
        "Lvl 100 Leviathan Omega": "2,1,3",
        "Lvl 100 Yggdrasil Omega": "2,1,4",
        "Lvl 100 Luminiera Omega": "2,1,5",
        "Lvl 100 Celeste Omega": "2,1,6",

        # 2 stars
        "Lvl 120 Shiva": "2,2,1",
        "Lvl 120 Europa": "2,2,2",
        "Lvl 120 Godsworn Alexiel": "2,2,3",
        "Lvl 120 Grimnir": "2,2,4",
        "Lvl 120 Metatron": "2,2,5",
        "Lvl 120 Avatar": "2,2,6",
        "Lvl 110 Rose Queen": "2,2,7",
        "Lvl 120 Atum": "2,3,1",
        "Lvl 120 Tefnut": "2,3,2",
        "Lvl 120 Bennu": "2,3,3",
        "Lvl 120 Ra": "2,3,4",
        "Lvl 120 Horus": "2,3,5",
        "Lvl 120 Osiris": "2,3,6",

        # 3 stars
        "Lvl 150 Tiamat Malice": "2,4,1",
        "Lvl 150 Leviathan Malice": "2,4,2",
        "Lvl 150 Phronesis": "2,4,3",
        "Lvl 150 Luminiera Malice": "2,4,4",
        "Lvl 150 Anima-Animus Core": "2,4,5",

        # 4 stars
        "Huanglong & Qilin (Impossible)": "2,5,1",
        "Lvl 150 Lucilius": "2,5,2",
        "The Four Primarchs": "2,5,3",
        "Lvl 200 Lindwurm": "2,5,4",

        # 5 stars
        "Lvl 200 Wilnas": "2,6,1",
        "Lvl 200 Wamdus": "2,6,2",
        "Lvl 200 Galleon": "2,6,3",
        "Lvl 200 Ewiyar": "2,6,4",
        "Lvl 200 Lu Woh": "2,6,5",
        "Lvl 200 Fediel": "2,6,6",

        # 6 stars
        "Lvl 150 Proto Bahamut": "2,7,1",
        "Lvl 200 Akasha": "2,7,2",
        "Lvl 200 Grand Order": "2,7,3",
        "Lvl 200 Ultimate Bahamut": "2,7,4",

        # 7 stars
        "Lvl 250 Lucilius": "2,8,1",
        "Lvl 250 Belial": "2,8,2",
        "Lvl 250 Beelzebub": "2,8,3",

        # 8 stars
        "Lvl 275 Mugen": "2,9,1",
        "Lvl 275 Diaspora": "2,9,2",
        "Lvl 275 Siegfried": "2,9,3",
        "Lvl 275 Seofon": "2,9,4",
        "Lvl 275 Agastia": "2,9,5",
        "Lvl 300 Super Ultimate Bahamut": "2,10,1",

        # TODO: Need to see what the next ROTB will look like for the new raid finder.
        # "Lvl 60 Zhuque": "Lv60 朱雀",
        # "Lvl 90 Agni": "Lv90 アグニス",
        # "Lvl 60 Xuanwu": "Lv60 玄武",
        # "Lvl 90 Neptune": "Lv90 ネプチューン",
        # "Lvl 60 Baihu": "Lv60 白虎",
        # "Lvl 90 Titan": "Lv90 ティターン",
        # "Lvl 60 Qinglong": "Lv60 青竜",
        # "Lvl 90 Zephyrus": "Lv90 ゼピュロス",
        # "Lvl 100 Shenxian": "Lv100 四象瑞神",
    }

    @staticmethod
    def _check_for_joined_raids():
        """Check and update the number of raids currently joined.

        Returns:
            None
        """
        from bot.game import Game

        # Make the Recent tab active.
        Game.find_and_click_button("raid_tab_recent")

        # Find out the number of currently joined raids.
        joined_locations = ImageUtils.find_all("joined")

        if joined_locations is not None:
            Raid._raids_joined = len(joined_locations)
            MessageLog.print_message(f"\n[RAID] There are currently {Raid._raids_joined} raids joined.")

        return None

    @staticmethod
    def _clear_joined_raids():
        """Begin process to wait out the joined raids if there are 3 or more currently active.

        Returns:
            None
        """
        from bot.game import Game

        # If the maximum number of raids has been joined, collect any pending rewards with a interval of 30 seconds in between until the number of joined raids is below 3.
        while Raid._raids_joined >= 3:
            MessageLog.print_message(f"\n[RAID] Maximum raids of 3 has been joined. Waiting 30 seconds to see if any finish.")
            Game.wait(30)

            Game.go_back_home(confirm_location_check = True)
            Game.find_and_click_button("quest")

            if Game.check_for_pending():
                Game.find_and_click_button("quest")
                Game.wait(3.0)

            Game.find_and_click_button("raid")
            Game.wait(3.0)
            Raid._check_for_joined_raids()

        return None

    @staticmethod
    def _join_raid():
        """Start the process to join a raid using the Filters. Room codes are not feasible at this time due to Twitter API pricing changes.
        """
        from bot.game import Game

        # A list of available raids to join should have appeared. Join the first one found.
        tries = 100
        recovery_time = 5
        while tries > 0:
            position = ImageUtils.find("raid_time_remaining")
            if position:
                MouseUtils.move_and_click_point(position[0], position[1], "raid_time_remaining")
                MessageLog.print_message("[RAID] Successfully found a raid.")
                break
            else:
                tries -= 1
                if tries <= 0:
                    raise RaidException(f"No raids have been found for a considerable amount of time for {Settings.mission_name}. Exiting now...")

                sleep_time = random.randint(4, recovery_time)
                MessageLog.print_message(f"[RAID] No raids found in the list. Waiting {sleep_time} seconds before refreshing the list. {tries} tries remaining.")
                Game.wait(sleep_time)
                Game.find_and_click_button("reload")

    @staticmethod
    def _navigate():
        """Navigates to the specified Raid.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"\n[RAID] Beginning process to navigate to the raid: {Settings.mission_name}...")

        # Head to the Home screen.
        Game.go_back_home(confirm_location_check = True)

        # Then navigate to the Quest screen.
        if Game.find_and_click_button("raid_red"):
            Game.wait(0.5)

            max_attempts = 3
            for attempt_num in range(max_attempts):
                # Check for the "You retreated from the raid battle" popup.
                if ImageUtils.confirm_location("raid"):
                    Raid._join_raid()
                    break
                elif ImageUtils.confirm_location("you_retreated_from_the_raid_battle", tries=1):
                    Game.find_and_click_button("ok")
            else:  # no break
                Raid.start(False)
                # raise RaidException("Failed to reach the Backup Requests screen.")
        
        else:
            Game.find_and_click_button("quest")

            Game.wait(0.5)

            # Check for the "You retreated from the raid battle" popup.
            if ImageUtils.confirm_location("you_retreated_from_the_raid_battle", tries = 3):
                Game.find_and_click_button("ok")

            # Check for any Pending Battles popup.
            if Game.check_for_pending():
                Game.find_and_click_button("quest")

            # Now navigate to the Raid screen.
            Game.find_and_click_button("raid")

            if ImageUtils.confirm_location("raid"):
                # Check for any joined raids and if the max number of raids joined was reached, clear them.
                Raid._check_for_joined_raids()
                Raid._clear_joined_raids()

                Raid._join_raid()
            else:
                Raid.start(False)
                # raise RaidException("Failed to reach the Backup Requests screen.")

    @staticmethod
    def start(first_run: bool):
        """Starts the process to complete a run for Raid Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            None
        """
        from bot.game import Game

        Raid._navigate()
        Game.wait(1.5)  # delay before summon selection screen popup

        # Check if the bot is at the Summon Selection screen.
        max_attempts = 5
        for attempt_num in range(max_attempts):
            if ImageUtils.confirm_location("select_a_summon", tries=1):
                summon_check = Game.select_summon(Settings.summon_list, Settings.summon_element_list)

                if summon_check:
                    # Select the Party.
                    if Game.find_party_and_start_mission(Settings.group_number, Settings.party_number):
                        # Handle the rare case where joining the Raid after selecting the Summon and Party led the bot to the Quest Results screen with no loot to collect.
                        if ImageUtils.confirm_location("no_loot", disable_adjustment = True):
                            MessageLog.print_message("\n[RAID] Seems that the Raid just ended. Moving back to the Home screen and joining another Raid...")
                        elif CombatMode.start_combat_mode():
                            Game.collect_loot(is_completed = True)
                    else:
                        MessageLog.print_message("\n[RAID] Seems that the Raid ended before the bot was able to join. Now looking for another Raid to join...")
                break
            else:
                if Game.check_for_pending():
                    break
        else:  # no break
            Game.find_and_click_button("reload")
            Raid.start(False)
            # raise RaidException("Failed to arrive at the Summon Selection screen.")

        return None
