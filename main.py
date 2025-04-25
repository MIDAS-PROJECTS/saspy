import sasConnection.sasCon as sasCon
import time

port = "/dev/ttyACM0"
address = 1

machineID = [
    'ASCII_game_ID',
    'ASCII_additional_ID',
    'bin_denomination',
    'bin_max_bet',
    'bin_progressive_mode',
    'bin_game_options',
    'ASCII_paytable_ID',
    'ASCII_base_percentage'
]

game_meters = [
    'total_bet_meter',
    'total_win_meter',
    'total_in_meter',
    'total_jackpot_meter',
    'games_played_meter'
]


sasConnection = sasCon.SasConnection(port, address)
sasConnection.start()

for k in machineID:
    print(f"{k}\t {sasConnection.meters[k]}")

while True:
    sasConnection.meters_11_15()
    for meter in game_meters:
        print(f"{k}\t {sasConnection.meters[k]}")
    time.sleep(1000)



