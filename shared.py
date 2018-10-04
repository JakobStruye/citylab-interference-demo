with open("nodes") as f:
    lines = f.read().split("\n")
    nodes = [str(line) for line in lines]
    nodes = nodes[:-1]
with open("freqs") as f:
    lines = f.read().split("\n")
    freqs = [str(line) for line in lines]
    freqs = freqs[:-1]
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

basedir = "../"
dump_dir_base = basedir + "cnert/"
raw_parse_dir_base = basedir + "raw_parse/"
smooth_dir_base = basedir + "smoothed/"
predict_dir_base = basedir + "predicted/"

weights_dir_base = "./weights/"

coloring_strategy = 'relative' #'relative' or 'absolute'
absolute_thresh_red = -30. #Everything above this is red
absolute_thresh_green = -60 #Everything below this is green
relative_thresh_red = 0.7 #Red above this fraction
relative_thresh_green = 0.3 #Green below this fraction

lb = 300
pred_step = 100
input_shape = (1, lb)
units = 100
epochs = 20
epochs_init = 40
train_size = 11000


def normalize(arr):
    minval = -100
    maxval = -20
    range = maxval - minval
    return (arr - minval) * 2 / (range) - 1

def denormalize(arr):
    minval = -100
    maxval = -20
    range = maxval - minval

    return (arr + 1) * range / 2 + minval
