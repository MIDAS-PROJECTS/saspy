import sasConnection.sasCon as sasCon
import time

port = "/dev/ttyUSB0"
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
sasConnection.connect()
sasConnection.start()


while True:
    #print(f"input buffer: {sasConnection.connection.in_waiting}")
    #print(f"output buffer {sasConnection.connection.out_waiting}")

    #if (sasConnection.connection.in_waiting == 4095):
        
        #print("it was true")
    print(bytearray(sasConnection.connection.read(sasConnection.connection.in_waiting)))
    #print(sasConnection.connection.read(sasConnection.connection.in_waiting))
    time.sleep(.1)

for k in machineID:
    print(f"{k}\t {sasConnection.meters[k]}")

#while True:
#    sasConnection.meters_11_15()
#    for meter in game_meters:
#        print(f"{meter}\t {sasConnection.meters[meter]}")
#    time.sleep(1000)



