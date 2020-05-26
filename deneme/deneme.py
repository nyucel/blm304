parca_boyutu  = 100

file_name = "../170401028/serverside_folder/2mb-text.txt"

input = open(file_name, 'rb')

seqno = 0
while True:
    parca = input.read(parca_boyutu)
    if not parca: break
    seqno += 1
    print(seqno)

    data_packet = datapacket.DataPacket("200")
    data_packet = pickle.dumps(data_packet)
    self.ServerSocket.sendto(data_packet, address)