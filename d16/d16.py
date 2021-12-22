import math
from copy import copy


def hex_to_bin_string(hex_string):
    h_size = len(hex_string) * 4
    return str(bin(int(hex_string, 16))[2:].zfill(h_size))


VERSIONS_SUM = 0


def read_literals(bin_string):
    bin_len = len(bin_string)
    literals = []
    last = 0
    for i in range(0, bin_len - 1, 5):
        last = i + 5
        literals.append(bin_string[i + 1:last])
        if bin_string[i] == '0':
            break

    return literals, last


def read_operator_packets(bin_string, depth):
    length_type_id = bin_string[0]
    all_literals = []
    if length_type_id == '0':
        length = int(bin_string[1:16], 2)
        total_length = 16
        packets_begin = 16
        packet_offset = 0

        while packet_offset < length:
            sub_part = bin_string[packets_begin + packet_offset:packets_begin + length]
            literals, packet_length = read_packet(sub_part, depth + 1)
            for literal in literals:
                all_literals.append(literal)

            total_length += packet_length
            packet_offset += packet_length
    else:
        packets_number = int(bin_string[1:12], 2)
        total_length = 12
        packets_begin = 12
        packet_offset = 0
        for i in range(0, packets_number):
            sub_part = bin_string[packets_begin + packet_offset:]
            literals, packet_length = read_packet(sub_part, depth + 1)
            for literal in literals:
                all_literals.append(literal)
            total_length += packet_length
            packet_offset += packet_length
    return copy(all_literals), total_length


def read_packet(bin_string, depth=0):
    global VERSIONS_SUM
    prefix = f'|' + '-' * depth
    version = bin_string[0:3]
    type_id = int(bin_string[3:6], 2)
    VERSIONS_SUM += int(version, 2)
    if type_id == 4:
        literals, packet_length = read_literals(bin_string[6:])
        literal_str = ''.join(literals)
        literals = [int(literal_str, 2)]
        print(f'{prefix}literal {literals}')
    else:
        literals, packet_length = read_operator_packets(bin_string[6:], depth)
        res_literals = []
        operator = ''
        if type_id == 0:
            operator = 'sum'
            res_literals = [sum(literals)]
        if type_id == 1:
            operator = 'prod'
            res_literals = [math.prod(literals)]
        if type_id == 2:
            operator = 'min'
            res_literals = [min(literals)]
        if type_id == 3:
            operator = 'max'
            res_literals = [max(literals)]
        if type_id == 5:
            operator = 'gt'
            if len(literals) > 2:
                print("ERROR")
            res_literals = [int(literals[0] > literals[1])]
        if type_id == 6:
            operator = 'lt'
            if len(literals) > 2:
                print("ERROR")
            res_literals = [int(literals[0] < literals[1])]
        if type_id == 7:
            operator = 'eq'
            res_literals = [int(literals[0] == literals[1])]

        print(f'{prefix}{operator}({literals}) = {res_literals}')
        literals = copy(res_literals)

    packet_length += 6

    return literals, packet_length


def packet_decoder(hex_string):
    bin_string = hex_to_bin_string(hex_string)
    print(bin_string)
    literals, _ = read_packet(bin_string)
    print(f'part one: {VERSIONS_SUM}')
    print(f'part two: {literals}')


if __name__ == '__main__':
    hex_string_task = '420D4900B8F31EFE7BD9DA455401AB80021504A2745E1007A21C1C862801F54AD0765BE833D8B9F4CE8564B9BE6C5CC011E00D5C001098F11A232080391521E4799FC5BB3EE1A8C010A00AE256F4963B33391DEE57DA748F5DCC011D00461A4FDC823C900659387DA00A49F5226A54EC378615002A47B364921C201236803349B856119B34C76BD8FB50B6C266EACE400424883880513B62687F38A13BCBEF127782A600B7002A923D4F959A0C94F740A969D0B4C016D00540010B8B70E226080331961C411950F3004F001579BA884DD45A59B40005D8362011C7198C4D0A4B8F73F3348AE40183CC7C86C017997F9BC6A35C220001BD367D08080287914B984D9A46932699675006A702E4E3BCF9EA5EE32600ACBEADC1CD00466446644A6FBC82F9002B734331D261F08020192459B24937D9664200B427963801A094A41CE529075200D5F4013988529EF82CEFED3699F469C8717E6675466007FE67BE815C9E84E2F300257224B256139A9E73637700B6334C63719E71D689B5F91F7BFF9F6EE33D5D72BE210013BCC01882111E31980391423FC4920042E39C7282E4028480021111E1BC6310066374638B200085C2C8DB05540119D229323700924BE0F3F1B527D89E4DB14AD253BFC30C01391F815002A539BA9C4BADB80152692A012CDCF20F35FDF635A9CCC71F261A080356B00565674FBE4ACE9F7C95EC19080371A009025B59BE05E5B59BE04E69322310020724FD3832401D14B4A34D1FE80233578CD224B9181F4C729E97508C017E005F2569D1D92D894BFE76FAC4C5FDDBA990097B2FBF704B40111006A1FC43898200E419859079C00C7003900B8D1002100A49700340090A40216CC00F1002900688201775400A3002C8040B50035802CC60087CC00E1002A4F35815900903285B401AA880391E61144C0004363445583A200CC2C939D3D1A41C66EC40'
    hex_string = 'D2FE28'

    packet_decoder(hex_string_task)
