
#import os
#os.chdir(__file__)

##Regiones importantes - Cada una tiene su checksum propio.
#Header global
checkAdress_Header = 0x1ec
headerRegion = [0x0, 0x100]
header_duplicate_offset = 0x1000

block_header =  [checkAdress_Header, header_duplicate_offset, headerRegion, 0]


#File1
checkAddress_File1 = 0x8006
File1Region = [0x8008, 0xC000]
File1_duplicate_offset = 0x4000
seedGeneral = 0x0001 + 0x564D + 0x2032 #Header de  cada bloque (el mismo para todos), menos para el global

block_File1 = [checkAddress_File1, File1_duplicate_offset, File1Region, seedGeneral]

#File 2
checkAddress_File2 = checkAddress_File1 + 0x8000
File2Region = [File1Region[0]+0x8000, File1Region[1]+0x8000]
File2_duplicate_offset = File1_duplicate_offset

block_File2 = [checkAddress_File2, File2_duplicate_offset, File2Region, seedGeneral]

#File 3
checkAddress_File3 = checkAddress_File1 + 2*0x8000
File3Region = [File1Region[0]+2*0x8000, File1Region[1]+2*0x8000]
File3_duplicate_offset = File1_duplicate_offset

block_File3 = [checkAddress_File3, File3_duplicate_offset, File3Region, seedGeneral]


#Amigo Letters
checkAddress_Amigos = 0x2006
AmigoRegion = [0x2008, 0x4FFF]
Amigo_duplicate_offset = 0x3000
block_Amigo = [checkAddress_Amigos, Amigo_duplicate_offset, AmigoRegion, seedGeneral]


#Todos los bloques a corregir
Blocks = [ block_header, block_File1,block_Amigo, block_File2, block_File3]






##Alelulya!! El checksum que anda. Gracias, gracias a la wiki de Mother 3 por la idea de hacer xor con 0xFFFF tras sumar
#https://datacrystal.romhacking.net/wiki/MOTHER_3:SRAM_map
#savefile = "saveEdit.sav"
def calc_magical_checkum(sav, format = 'h', region = [0x0, 0x100], seed = 0):

    sum = seed
    fro = region[0]
    to = region[1]
    for address in range(fro, to, 2): sum += (sav[address+1]<<8) + sav[address]

    sum &= 0xFFFF
    sum ^= 0xFFFF

    if(format=='h'):  return hex(sum)
    if(format=='i'):  return sum
    if(format=='be'): return (sum>>8)&0xFF, sum&0xFF #devuelve en modo big endian
    if(format=='le'): return sum&0xFF, (sum>>8)&0xFF #devuelve en modo little endian


    #address_check = 0x1ec
    #check_value = sav[address_check:address_check+2] #array de dos bytes little endian
    #check_value = (check_value[1]<<8) + check_value[0] # int


##Recibe un archivo, supuestamente modificado de afuera, y le calcula el checksum correcto que debería tener
def correct_magical_checksums(saveFile_path):

    with open(saveFile_path,"rb") as f:
        sav = bytearray(f.read())

        for block in Blocks:
            address = block[0]
            dp_off = block[1]
            region = block[2]
            seed = block[3]
            checksum = calc_magical_checkum(sav, format = 'le', region=region, seed = seed)

            sav[address:address+2] = checksum
            sav[address+dp_off:address+dp_off+2] = checksum

    with open(saveFile_path, "w+b") as f:
        f.write(sav)
