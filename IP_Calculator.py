__coder__ = "KhodeXenon"
__my_email__ = "KhodeXenon@gmail.com"

from modules import BinaryOctet, DecimalConversion
checked_ip = ""
checked_subnet = ""
checked_prefix = ""
checked_ip_class = ""
checked_net_id = ""
checked_total_host = ""
checked_broadcast = ""

def IpCalc():
    '''calculate ip address information'''

    # set allowed and disallowed ip and subnets
    allowed_masks = [0, 128, 192, 224, 240, 248, 252, 254, 255]
    disallowed_first_ip_octets = [0, 127]
    default_subnet_masks = {"A":"255.0.0.0", "B":"255.255.0.0", "C":"255.255.255.0"}


    ip_checking = True
    while ip_checking :

        try :
            ip_address = input("IP address :")
            subnet_mask = input("Subnet mask :")
            ip_address_octets = ip_address.split(".")
            int_ip_address_octets = [int(x) for x in ip_address_octets]
            # seting default subnet masks
            if subnet_mask == "" :
                if 1 <= int_ip_address_octets[0] <= 126 :
                    subnet_mask = default_subnet_masks["A"]
                elif 128 <= int_ip_address_octets[0] <= 191 :
                    subnet_mask = default_subnet_masks["B"]
                elif 192 <= int_ip_address_octets[0] <= 223 :
                    subnet_mask = default_subnet_masks["C"]
            # ip address checking
            if len(int_ip_address_octets) == 4 and \
                    (1 <= int_ip_address_octets[0] <= 223) and \
                    (int_ip_address_octets[0] not in disallowed_first_ip_octets) and \
                    (0 <= int_ip_address_octets[1] <= 255) and \
                    (0 <= int_ip_address_octets[2] <= 255) and \
                    (0 <= int_ip_address_octets[3] <= 254) :
                checked_ip = ip_address
            else:
                print("Invalid IP address !")
                continue
            # subnet mask checking
            subnet_mask_octets = subnet_mask.split(".")
            int_subnet_mask_octets = [int(y) for y in subnet_mask_octets]

            if int_subnet_mask_octets[0] == 255 and \
                    int_subnet_mask_octets[1] in allowed_masks and \
                    int_subnet_mask_octets[2] in allowed_masks and \
                    int_subnet_mask_octets[3] in allowed_masks and \
                    int_subnet_mask_octets[3] <= 252 and \
                    (int_subnet_mask_octets[0] >= int_subnet_mask_octets[1] >= int_subnet_mask_octets[2] >= int_subnet_mask_octets[3]):
                checked_subnet = subnet_mask
            else:
                print("Invalid subnet mask !")
                continue



            # set a dictionary for subnet calculations and prefix
            equal_zero_subnet = {"255": 0, "254": 1, "252": 2, "248": 3, "240": 4, "224": 5, "192": 6, "128": 7, "0": 8}
            subnet_oct1_zeros = equal_zero_subnet[subnet_mask_octets[0]]
            subnet_oct2_zeros = equal_zero_subnet[subnet_mask_octets[1]]
            subnet_oct3_zeros = equal_zero_subnet[subnet_mask_octets[2]]
            subnet_oct4_zeros = equal_zero_subnet[subnet_mask_octets[3]]
            #this is host zeros not network zeros
            total_HOST_zeros = subnet_oct1_zeros + subnet_oct2_zeros + subnet_oct3_zeros + subnet_oct4_zeros
            checked_prefix = 32 - total_HOST_zeros

            # set ip class (A,B,C)
            if 1 <= int_ip_address_octets[0] <= 126 :
                checked_ip_class = "A"
            elif 128 <= int_ip_address_octets[0] <= 191 :
                checked_ip_class = "B"
            elif 192 <= int_ip_address_octets[0] <= 223 :
                checked_ip_class = "C"

            # set number of hosts per network

            hosts = 2 ** total_HOST_zeros - 2
            checked_total_host = hosts

            #set net ID and broadcast ID

            total_NETWORK_zeros = 32 - total_HOST_zeros

            # converting normal *SUBNET MASK* bins into 8 length bins
            complete_SUBNET_8_length_bin = []
            for subnet_bins in int_subnet_mask_octets :
                subnet_bin_changing = BinaryOctet(subnet_bins)
                complete_SUBNET_8_length_bin.append(subnet_bin_changing)
            # converting normal *IP ADDRESS* bins into 8 length bins
            complete_IP_8_length_bin = []
            for network_bins in int_ip_address_octets :
                network_bin_changing = BinaryOctet(network_bins)
                complete_IP_8_length_bin.append(network_bin_changing)

            #network id calculating
            netid_IP_8_length_bin = complete_IP_8_length_bin[:]
            #convert 8-15 prefixes
            if (8 <= total_NETWORK_zeros <= 15) :
                set_end_main_seq = total_NETWORK_zeros - 8
                main_seq = complete_IP_8_length_bin[1]
                main_seq = main_seq[0:set_end_main_seq]
                zero_network_number = 16 - total_NETWORK_zeros
                str_zero_network_number = ""
                for str_zero in range(0,zero_network_number):
                    str_zero_network_number += "0"
                new_network_id_oct2 = main_seq + str_zero_network_number
                new_network_id_oct3 = "00000000"
                new_network_id_oct4 = "00000000"
                netid_IP_8_length_bin[1] = new_network_id_oct2
                netid_IP_8_length_bin[2] = new_network_id_oct3
                netid_IP_8_length_bin[3] = new_network_id_oct4
            # convert 16-23 prefixes
            elif (16 <= total_NETWORK_zeros <= 23) :
                set_end_main_seq = total_NETWORK_zeros - 16
                main_seq = complete_IP_8_length_bin[2]
                main_seq = main_seq[0:set_end_main_seq]
                zero_network_number = 24 - total_NETWORK_zeros
                str_zero_network_number = ""
                for str_zero in range(0, zero_network_number):
                    str_zero_network_number += "0"
                new_network_id_oct3 = main_seq + str_zero_network_number
                new_network_id_oct4 = "00000000"
                netid_IP_8_length_bin[2] = new_network_id_oct3
                netid_IP_8_length_bin[3] = new_network_id_oct4
            # convert 24-30 prefixes
            elif  (24 <= total_NETWORK_zeros <= 30) :
                set_end_main_seq = total_NETWORK_zeros - 24
                main_seq = complete_IP_8_length_bin[3]
                main_seq = main_seq[0:set_end_main_seq]
                zero_network_number = 32 - total_NETWORK_zeros
                str_zero_network_number = ""
                for str_zero in range(0, zero_network_number):
                    str_zero_network_number += "0"
                new_network_id_oct4 = main_seq + str_zero_network_number
                netid_IP_8_length_bin[3] = new_network_id_oct4
            # convert to decimal and convert it to string number
            net_decimal_list = []
            for decimal_net_num in netid_IP_8_length_bin :
                new_dec = DecimalConversion(decimal_net_num)
                net_decimal_list.append(new_dec)

            checked_net_id = ".".join(net_decimal_list)


            # broadcast calculating
            broadcast_IP_8_length_bin = complete_IP_8_length_bin[:]
            # convert 8-15 prefixes
            if (8 <= total_NETWORK_zeros <= 15):
                set_end_main_seq = total_NETWORK_zeros - 8
                main_seq = complete_IP_8_length_bin[1]
                main_seq = main_seq[0:set_end_main_seq]
                zero_network_number = 16 - total_NETWORK_zeros
                str_zero_network_number = ""
                for str_zero in range(0, zero_network_number):
                    str_zero_network_number += "1"
                new_broadcast_oct2 = main_seq + str_zero_network_number
                new_broadcast_oct3 = "11111111"
                new_broadcast_oct4 = "11111111"
                broadcast_IP_8_length_bin[1] = new_broadcast_oct2
                broadcast_IP_8_length_bin[2] = new_broadcast_oct3
                broadcast_IP_8_length_bin[3] = new_broadcast_oct4
            # convert 16-23 prefixes
            elif (16 <= total_NETWORK_zeros <= 23):
                set_end_main_seq = total_NETWORK_zeros - 16
                main_seq = complete_IP_8_length_bin[2]
                main_seq = main_seq[0:set_end_main_seq]
                zero_network_number = 24 - total_NETWORK_zeros
                str_zero_network_number = ""
                for str_zero in range(0, zero_network_number):
                    str_zero_network_number += "1"
                new_broadcast_oct3 = main_seq + str_zero_network_number
                new_broadcast_oct4 = "11111111"
                broadcast_IP_8_length_bin[2] = new_broadcast_oct3
                broadcast_IP_8_length_bin[3] = new_broadcast_oct4
            # convert 24-30 prefixes
            elif (24 <= total_NETWORK_zeros <= 30):
                set_end_main_seq = total_NETWORK_zeros - 24
                main_seq = complete_IP_8_length_bin[3]
                main_seq = main_seq[0:set_end_main_seq]
                zero_network_number = 32 - total_NETWORK_zeros
                str_zero_network_number = ""
                for str_zero in range(0, zero_network_number):
                    str_zero_network_number += "1"
                new_broadcast_oct4 = main_seq + str_zero_network_number
                broadcast_IP_8_length_bin[3] = new_broadcast_oct4
            #convert to decimal and convert it to string number
            broadcast_decimal_list = []
            for decimal_broadcast_num in broadcast_IP_8_length_bin:
                new_dec = DecimalConversion(decimal_broadcast_num)
                broadcast_decimal_list.append(new_dec)

            checked_broadcast = ".".join(broadcast_decimal_list)


        # error handling
        except ValueError :
            print("Invalid IP address or subnet mask !")
            again_or_not = input("again ? (y) :").lower()
            if again_or_not == "y" or again_or_not == "yes" :
                ip_checking = True
            else:
                ip_checking = False

        except KeyboardInterrupt :
            print("Canceled by user ...")

        except IndexError :
            print("Invalid IP address or subnet mask !")
            again_or_not = input("again ? (y) :").lower()
            if again_or_not == "y" or again_or_not == "yes":
                ip_checking = True
            else:
                ip_checking = False

        except KeyError :
            print("Invalid IP address or subnet mask !")
            again_or_not = input("again ? (y) :").lower()
            if again_or_not == "y" or again_or_not == "yes":
                ip_checking = True
            else:
                ip_checking = False

        # error handling

        else:

            try :

                print("\n")

                print("the Entered IP address : ", checked_ip)

                print("")

                print("the Entered Subnet mask : ", checked_subnet)

                print("")

                print("Prefix length : ", checked_prefix)

                print("")

                print("IP class : ", checked_ip_class)

                print("")

                print("Network ID : ", checked_net_id)

                print("")

                print("Total hosts per network : ", abs(checked_total_host))

                print("")

                print("Broadcast : " , checked_broadcast)

                print("")
            except TypeError :
                print("Invalid information")
                again_or_not = input("again ? (y) :").lower()
                if again_or_not == "y" or again_or_not == "yes":
                    ip_checking = True
                else:
                    ip_checking = False


IpCalc()