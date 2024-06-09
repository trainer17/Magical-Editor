evt_scp_offset = 0xAAD600
size = 2125628

data = readROMregion(evt_scp_offset, evt_scp_offset + size)


#Le pasas un array y de bytes lo interpreta como punteros
def readPointers(data):

    punteros = []
    for i in range(0,len(data), 4):
        pointer =  data[i] +  (data[i+1] << 8) +  (data[i+2] << 16) +  (data[i+3] << 24) #Read little endian
        punteros.append(pointer)
    return punteros


punteros = readPointers(data)

addresses = [evt_scp_offset + i*4 for i in range(size)]



