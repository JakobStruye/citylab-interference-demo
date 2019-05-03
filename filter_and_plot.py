import itertools
import subprocess
import sys

from freq_channelnr_map import map_ as channelnr_map

counter = 0
maxes = []
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



### REMOVE SECONDS FROM FILENAMES WITH
### ls -d ??????????????????? | xargs rename 's/.{3}$//'




def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except:# ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order + 1)
    half_window = (window_size - 1) // 2
    # precompute coefficients
    b = np.mat([[k ** i for i in order_range] for k in range(-half_window, half_window + 1)])
    m = np.linalg.pinv(b).A[deriv] * rate ** deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs(y[1:half_window + 1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window - 1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve(m[::-1], y, mode='valid')


def process_point(day, hour, minute):
    signals = []  # Fill with every nf+rssi of dump
    file_name = directory + day + '_' + str(hour).zfill(2) + '-' + str(
        minute).zfill(2)
    try:
        signalstr = subprocess.check_output(
            ['./fft_get_max_rssi.out', file_name]) if not channel_number else subprocess.check_output(
            ['./fft_get_max_rssi.out', file_name, channelnr_map[channel_number]])
    except:
        print(file_name)
        return None
    for line in signalstr.splitlines():
        signals.append(int(line))
    if len(signals) == 1:
        return None
    signals = [signal for signal in signals if signal <=0]
    signals.sort()
    signals.reverse()
    try:
        return signals[filter_num]
    except:
        return None

if __name__ == '__main__':

    maxes = []

    start_hour = 0
    end_hour = 24

    if (len(sys.argv) < 6):
        print("Usage: python plot_rssi.py dump_directory date first_minute filter_num channel_number [prev_day next_day]\n\
               Example: To plot for channel 36 on 2 May 2017, first dump at 2 minutes past the hour ignoring the top 100 results for every dump: \n\
               python plot_rssi.py ../output_dir 2017-05-02 2 100 36 0\n\
               Note that the channel number is required: 0 means all channels\n\
               To use previous and next day's last and first hour to avoid potentially ugly results at end points.\n\
               These are only used in calculations and not actually plotted.")
        exit(0)

    #if len(sys.argv) == 7:
    #    print "Either supply both prev_day and next_day or neither"
    #    exit(1)

    fix_endpoints = len(sys.argv) >= 8

    idx = 1
    directory = sys.argv[idx]
    directory = directory + ('/' if not directory.endswith('/') else '')
    days = []
    idx += 1
    while len(sys.argv[idx]) > 3:
        days.append(sys.argv[idx])
        idx += 1

    first_minute = int(sys.argv[idx])
    idx += 1
    filter_num = int(sys.argv[idx])
    idx += 1
    channel_number = int(sys.argv[idx]) if sys.argv[idx] != '0' else None

    if fix_endpoints:
        prev_day = sys.argv[idx+1]
        next_day = sys.argv[idx+2]
    print("PREV", sys.argv[idx+1], "NEXT", sys.argv[idx+2])
    missings = []
    #TODO NONE POINT FIX FOR ENDPOINTS
    missing_pre = 0
    if fix_endpoints:
        print("FIXING ENDPTS")
        for hour in range(13,24,1):
            for (minute) in range(first_minute, 60, 1):
                max_point = process_point(prev_day, hour, minute)
                if max_point:
                    maxes.append(max_point)
                else:
                    missing_pre += 1
                    print("ERR1")
                    #missings.append((hour-24, minute))
    counter = 0
    for day in days:
        print(day)
        for (hour, minute) in itertools.product(range(start_hour,end_hour), range(first_minute, 60, 1)):
            max_point = process_point(day, hour, minute)
            if max_point:
                maxes.append(max_point)
            else:
                print("Bad", max_point)
                missings.append((counter,hour,minute))
        counter += 1

    missing_post = 0
    if fix_endpoints:
        for hour in range(0,11,1):

            for (minute) in range(first_minute, 60, 1):
                max_point = process_point(next_day, hour, minute)
                if max_point:
                    print("FIXING" + str(max_point))
                    maxes.append(max_point)
                else:
                    missing_post += 1
                    print("ERR2")
                    #missings.append((hour+24, minute))

    # Endpoints fix has 2 hours of additional data
    x = np.linspace(start_hour, len(days) * end_hour, len(days) * 60 * (end_hour - start_hour)) if not fix_endpoints else np.linspace(-11, 24*len(days) + 11, (len(days) * 24 + 22)*60)
    for (day,hour,minute) in missings:
        print(day, hour, minute)
        x = np.delete(x, day * 60 * 24 + hour * 60 + minute)
    for _ in range(missing_pre):
        x = np.delete(x, 0)
        for _ in range(missing_post):
            x = np.delete(x, x.shape[0] - 1)
    y = np.asarray(maxes)

    y_smooth = savitzky_golay(y, 101, 3)
    y_smooth2 = savitzky_golay(y, 1101, 3)
    fig = plt.figure()
    #raw = plt.plot(x, y, marker='.', markersize=2, linestyle='None', color='blue', alpha=0.3)
    #smooth1 = plt.plot(x, y_smooth, color='red')

    smooth2 = plt.plot(x, y_smooth2, color='green')
    # Ticks at even hours
    #plt.xticks(np.arange(0, 24 * len(days) + 1, 2))
    # Cut off endpoints fix; only show current day
    plt.xlim([start_hour, len(days) * end_hour])
    plt.xlabel('Time of day (hours)')
    plt.ylabel('Smoothed received signal strength (dBm)')
    for i in range(len(days)):
        plt.axvline(x=(i*24))
    raw_label = mpatches.Patch(color='blue', label='Highest signal strength (top %d removed)' % filter_num)
    #smooth1_label = mpatches.Patch(color='red', label='Savitzky-Golay filtered, order 3, window size 101')
    smooth2_label = mpatches.Patch(color='green', label='Savitzky-Golay filtered, order 3, window size 1101')
    #Additional 15dBm on top for legend
    #plt.ylim([plt.gca().get_ylim()[0],plt.gca().get_ylim()[1]+15])
    plt.ylim([-50,-25])

    #plt.legend(handles=[raw_label, smooth1_label, smooth2_label])
    plt.legend(handles=[smooth2_label])
    plt.show()
    #fig.savefig(directory + "../images/"  + day + "_" + str(channel_number))
    with open('smooth.out', 'w+') as f:
        for line in y_smooth2:
            f.write(str(line) + '\n')