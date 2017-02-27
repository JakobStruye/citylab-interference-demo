import sys

if __name__ == "__main__":
    if (len(sys.argv) == 4):
        type_of_input = int(sys.argv[1])
        inputfile = sys.argv[2]
        outputfile = sys.argv[3]
    elif (len(sys.argv) < 4):
        print("Usage: python parse.py <type> <inputfile> <outputfile>\n Type: 1 - wlan0-scan, 2 - wireshark text dump")
        sys.exit()

    #1 : wlan0_scan, default
    #2 : wireshark text dump parse

    output = []
    output_ = set()

    if (type_of_input == 1):
        wlan_scan_output = open(inputfile)

        entry = ""

        for line in wlan_scan_output.readlines():
            #order is BSS -> freq -> SSID so print it like that
            if ("BSS" in line and not ("OBSS" in line or "IBSS" in line)):
                entry += " & " + line[:-12][4:] + " \\\\"
                # print(entry)
            elif ("SSID" in line):
                entry = line[7:-1] + entry
                output.append(entry)
                entry = ""
            elif ("freq" in line):
                entry = " & " + line[7:-1] + entry
        wlan_scan_output.close()

    elif (type_of_input == 2):
        wireshark_text = open(inputfile)

        for line in wireshark_text.readlines():
            if ("Tag: DS Parameter set: Current Channel: " in line):
                if (line[-3] == '1'):
                    output_.add(line[-3:-1])
                else:
                    output_.add(line[-2])
                #
                # output_.add(line[-2])

        wireshark_text.close()

    outputstream = open(outputfile, 'a+')
    if (len(output) > 0):
        for out in output:
            outputstream.write(out)
            # print(out)
    elif (len(output_) > 0):
        ctr = 0
        last = len(output_)
        for out in output_:
            outputstream.write( out )
            if (ctr < last-1):
                outputstream.write( "," )
            ctr += 1
        outputstream.write( "\\\\ \hline \n" )
    else:
        print("no output found.")

    outputstream.close()
