todo viejo, nada de este codigo me sirve
import os
os.chdir('C:/Users/Graciela/Downloads/Games/Romhack/Magical Starsign (USA)/saves')
def crc16(data): #CRC16-CCITT
    table = [0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7,
    0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,
    0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6,
    0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,
    0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485,
    0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,
    0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4,
    0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,
    0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823,
    0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,
    0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12,
    0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,
    0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41,
    0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,
    0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70,
    0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,
    0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F,
    0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,
    0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E,
    0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,
    0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D,
    0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
    0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C,
    0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,
    0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB,
    0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,
    0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A,
    0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,
    0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9,
    0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,
    0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8,
    0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0]

    sum = 0xffff #valor inicials
    print ("Computing checksum...")
    for i in range(len(data)):
        sum = (sum << 8)^table[data[i]^int(bin(sum >> 8)[2:][-8:],2)]
        return (hex(int(bin(sum)[2:][-8:],2)) , hex(int(bin(sum >> 8)[2:][-8:],2)))



#####################################################

#USAR ESTE QUE ANDA BIEN
def crc16_2(data): #bytearray of the data you want to calculate CRC for
    crc = 0xFFFF
    for i in range(0, len(data)):
        crc ^= data[i] << 8
        for j in range(0,8):
            if (crc & 0x8000) > 0:
                crc =(crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return crc & 0xFFFF


def comprobar_todo():

    ##Probar todas las combinaciones de "from:to" hasta encontrar si algun rango hace coincidir el checksum con el crc16
    with open("Female Dark.sav","rb") as f:
        sav = bytearray(f.read())
        address_check = 0x1ec
        check_value = sav[address_check:address_check+2] #array de dos bytes
        check_value = (check_value[1]<<8) + check_value[0] # int

        combinaciones_validas = []
        for f in range(0, 0x100):
            for t in range(0xe0, address_check):
                if(t < f): continue
                calculated_value = crc16_2(sav[f:t])  #int
                if(check_value== calculated_value): combinaciones_validas += [(f,t)]
    return combinaciones_validas

#Ninguno coincide
#Conclusion: No usa crc16-ccitt

###############33
'''
def crc_remainder(input_bitstring, polynomial_bitstring, initial_filler):
    """Calculate the CRC remainder of a string of bits using a chosen polynomial.
    initial_filler should be '1' or '0'.
    """
    polynomial_bitstring = polynomial_bitstring.lstrip('0')
    len_input = len(input_bitstring)
    initial_padding = (len(polynomial_bitstring) - 1) * initial_filler
    input_padded_array = list(input_bitstring + initial_padding)
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(polynomial_bitstring)):
            input_padded_array[cur_shift + i] \
            = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
    return ''.join(input_padded_array)[len_input:]

def crc_check(input_bitstring, polynomial_bitstring, check_value):
    """Calculate the CRC check of a string of bits using a chosen polynomial."""
    polynomial_bitstring = polynomial_bitstring.lstrip('0')
    len_input = len(input_bitstring)
    initial_padding = check_value
    input_padded_array = list(input_bitstring + initial_padding)
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(polynomial_bitstring)):
            input_padded_array[cur_shift + i] \
            = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
    return ('1' not in ''.join(input_padded_array)[len_input:])
'''

#Toma un valor (en hex) y lo devuelve como string de bits
def h2b(h):
    pad, rjust, size, kind = '0', '>', 42, 'b'
    return f'{h:{pad}{rjust}{size}{kind}}'


#Toma un string de bits y lo devuelve como string de hex
def b2h(b):
    return hex(int(b, 2))

def crc16ccitt(hexArray):#poly 0x1021, initial value 0xffff, xorout =0
    s = ''
    for a in hexArray: s += h2b(a)
    return b2h(crc_remainder(s, h2b(0x1021), '0'))


######################################################################################3

##Pruebo todas las combinaciones de from:to y calculo un checksum propio hasta ver si alguna coincide con el valor almacenado
def comprobar_todo2():


    with open("Female Dark.sav","rb") as f:
        sav = bytearray(f.read())
        address_check = 0x1ec
        check_value = sav[address_check:address_check+2] #array de dos bytes little endian
        check_value = (check_value[1]<<8) + check_value[0] # int

        combinaciones_validas = []
        for f in range(0, 0x100):
            for t in range(0xe0, 0x100):
                if(t<f): continue
                sum = 0
                sumLong1 = 0
                sumLong2 = 0
                for address in range(f, t): sum +=sav[address]
                for address in range(f, t,2): sumLong1 += (sav[address+1]<<8) + sav[address]
                for address in range(f+1, t+1,2): sumLong2 += (sav[address+1]<<8) + sav[address] #misal

                sum &= 0xFFFF
                sumLong1 &= 0xFFFF
                sumLong2 &= 0xFFFF

                if(check_value in [sum, sumLong1, sumLong2]): combinaciones_validas += [(f,t)]


    return combinaciones_validas


