

nodes = ["70"]#, "14", "16", "18", "21", "23", "25", "28", "33", "35", "4", "7", "9"]


channels = dict({
    1:"2412",
    #2:"2417",
    #3:"2422",
    #4:"2427",
    #5:"2432",
    6:"2437",
    #7:"2442",
    #8:"2447",
    #9:"2452",
    #10:"2457",
    11:"2462",
    36:"5180",
    40:"5200",
    44:"5220" ,
    48:"5240",
    52:"5260",
    56:"5280",
    60:"5300",
    64:"5320",
    100:"5500" ,
    104:"5520",
    108:"5540",
    112:"5560",
    116:"5580",
    120:"5600",
    124:"5620",
    128:"5640",
    132:"5660",
    136:"5680",
    140:"5700",
})

freqs = []
basedir = "/home/jstruye/"
with open(basedir + 'citylab-interference-demo/freqs') as f:
    freqs = f.read().split('\n')[:-1]

dump_dir_base = basedir + "output/"
raw_parse_dir_base = basedir + "raw_parse/"
smooth_dir_base = basedir + "smoothed/"
predict_dir_base = basedir + "predicted/"

weights_dir_base = "./weights/"

coloring_strategy = 'relative' #'relative' or 'absolute'
relative_thresh_red = '-70' #Everything above this is red
relative_thresh_green = '-85' #Everything below this is green
absolute_thresh_red = 0.3 #Top fraction colored red
absolute_thresh_green = 0.3 #Bottom fraction colored green
