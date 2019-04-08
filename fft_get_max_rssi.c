/*
 * Copyright (C) 2012 Simon Wunderlich <sw@simonwunderlich.de>
 * Copyright (C) 2012 Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V.
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of version 2 of the GNU General Public
 * License as published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
 * 02110-1301, USA
 *
 */

/*
 * This program has been created to aid open source spectrum
 * analyzer development for Qualcomm/Atheros AR92xx and AR93xx
 * based chipsets.
 */

#ifdef __APPLE__
#include <libkern/OSByteOrder.h>
#define CONVERT_BE16(val)	val = OSSwapBigToHostInt16(val)
#define CONVERT_BE64(val)	val = OSSwapBigToHostInt64(val)
#else
#define _BSD_SOURCE
#ifdef    __FreeBSD__
#include <sys/endian.h>
#else

#include <endian.h>

#endif	/* __FreeBSD__ */
#define CONVERT_BE16(val)    val = be16toh(val)
#define CONVERT_BE64(val)    val = be64toh(val)
#endif

#include <errno.h>
#include <stdio.h>
#include <math.h>
//#include <SDL.h>
//#include <SDL_ttf.h>
#include <inttypes.h>
#include <unistd.h>
#include <time.h>
#include <stdlib.h>

typedef int8_t s8;
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint64_t u64;

enum ath_fft_sample_type {
    ATH_FFT_SAMPLE_HT20 = 1,
    ATH_FFT_SAMPLE_HT20_40 = 2,
    ATH_FFT_SAMPLE_ATH10K = 3,
};

enum nl80211_channel_type {
    NL80211_CHAN_NO_HT,
    NL80211_CHAN_HT20,
    NL80211_CHAN_HT40MINUS,
    NL80211_CHAN_HT40PLUS
};

/*
 * ath9k spectral definition
 */
#define SPECTRAL_HT20_NUM_BINS          56
#define SPECTRAL_HT20_40_NUM_BINS        128

struct fft_sample_tlv {
    u8 type;        /* see ath_fft_sample */
    u16 length;
    /* type dependent data follows */
} __attribute__((packed));

struct fft_sample_ht20 {
    struct fft_sample_tlv tlv;

    u8 max_exp;

    u16 freq;
    s8 rssi;
    s8 noise;

    u16 max_magnitude;
    u8 max_index;
    u8 bitmap_weight;

    u64 tsf;

    u8 data[SPECTRAL_HT20_NUM_BINS];
} __attribute__((packed));

struct fft_sample_ht20_40 {
    struct fft_sample_tlv tlv;

    u8 channel_type;
    u16 freq;

    s8 lower_rssi;
    s8 upper_rssi;

    u64 tsf;

    s8 lower_noise;
    s8 upper_noise;

    u16 lower_max_magnitude;
    u16 upper_max_magnitude;

    u8 lower_max_index;
    u8 upper_max_index;

    u8 lower_bitmap_weight;
    u8 upper_bitmap_weight;

    u8 max_exp;

    u8 data[SPECTRAL_HT20_40_NUM_BINS];
} __attribute__((packed));

/*
 * ath10k spectral sample definition
 */

#define SPECTRAL_ATH10K_MAX_NUM_BINS            256

struct fft_sample_ath10k {
    struct fft_sample_tlv tlv;
    u8 chan_width_mhz;
    uint16_t freq1;
    uint16_t freq2;
    int16_t noise;
    uint16_t max_magnitude;
    uint16_t total_gain_db;
    uint16_t base_pwr_db;
    uint64_t tsf;
    s8 max_index;
    u8 rssi;
    u8 relpwr_db;
    u8 avgpwr_db;
    u8 max_exp;

    u8 data[0];
} __attribute__((packed));


struct scanresult {
    union {
        struct fft_sample_tlv tlv;
        struct fft_sample_ht20 ht20;
        struct fft_sample_ht20_40 ht40;
        struct {
            struct fft_sample_ath10k header;
            u8 data[SPECTRAL_ATH10K_MAX_NUM_BINS];
        } ath10k;
    } sample;
    struct scanresult *next;
};

#define WIDTH    1600
#define HEIGHT    650
#define BPP    32

#define X_SCALE    10
#define Y_SCALE    4

#define    RMASK    0x000000ff
#define RBITS    0
#define    GMASK    0x0000ff00
#define GBITS    8
#define    BMASK    0x00ff0000
#define    BBITS    16
#define    AMASK    0xff000000


//static SDL_Surface *screen = NULL;
//static TTF_Font *font = NULL;
static struct scanresult *result_list;
static int scanresults_n = 0;
static int color_invert = 0;


/* read_file - reads an file into a big buffer and returns it
 *
 * @fname: file name
 *
 * returns the buffer with the files content
 */
static char *read_file(char *fname, size_t *size) {
    FILE *fp;
    char *buf = NULL;
    char *newbuf;
    size_t ret;

    fp = fopen(fname, "r");

    if (!fp)
        return NULL;

    *size = 0;
    while (!feof(fp)) {

        newbuf = realloc(buf, *size + 4097);
        if (!newbuf) {
            free(buf);
            return NULL;
        }

        buf = newbuf;

        ret = fread(buf + *size, 1, 4096, fp);
        *size += ret;
    }
    fclose(fp);

    if (buf)
        buf[*size] = '\0';

    return buf;
}

/*
 * read_scandata - reads the fft scandata and compiles a linked list of datasets
 *
 * @fname: file name
 *
 * returns 0 on success, -1 on error.
 */
static int read_scandata(char *fname) {
    char *pos, *scandata;
    size_t len, sample_len;
    size_t rel_pos, remaining_len;
    struct scanresult *result;
    struct fft_sample_tlv *tlv;
    struct scanresult *tail = result_list;
    int handled, bins;

    scandata = read_file(fname, &len);
    if (!scandata)
        return -1;

    pos = scandata;

    while ((uintptr_t)(pos - scandata) < len) {
        rel_pos = pos - scandata;
        remaining_len = len - rel_pos;

        if (remaining_len < sizeof(*tlv)) {
            fprintf(stderr, "Found incomplete TLV header at position 0x%x\n", rel_pos);
            break;
        }

        tlv = (struct fft_sample_tlv *) pos;
        CONVERT_BE16(tlv->length);
        sample_len = sizeof(*tlv) + tlv->length;
        pos += sample_len;

        if (remaining_len < sample_len) {
            fprintf(stderr, "Found incomplete TLV at position 0x%x\n", rel_pos);
            break;
        }

        if (sample_len > sizeof(*result)) {
            fprintf(stderr, "sample length %zu too long\n", sample_len);
            continue;
        }

        result = malloc(sizeof(*result));
        if (!result)
            continue;

        memset(result, 0, sizeof(*result));
        memcpy(&result->sample, tlv, sample_len);

        handled = 0;
        switch (tlv->type) {
            case ATH_FFT_SAMPLE_HT20:
                if (sample_len != sizeof(result->sample.ht20)) {
                    fprintf(stderr, "wrong sample length (have %zd, expected %zd)\n",
                            sample_len, sizeof(result->sample.ht20));
                    break;
                }

                CONVERT_BE16(result->sample.ht20.freq);
                CONVERT_BE16(result->sample.ht20.max_magnitude);
                CONVERT_BE64(result->sample.ht20.tsf);

                handled = 1;
                break;
            case ATH_FFT_SAMPLE_HT20_40:
                if (sample_len != sizeof(result->sample.ht40)) {
                    fprintf(stderr, "wrong sample length (have %zd, expected %zd)\n",
                            sample_len, sizeof(result->sample.ht40));
                    break;
                }

                CONVERT_BE16(result->sample.ht40.freq);
                CONVERT_BE64(result->sample.ht40.tsf);
                CONVERT_BE16(result->sample.ht40.lower_max_magnitude);
                CONVERT_BE16(result->sample.ht40.upper_max_magnitude);

                handled = 1;
                break;
            case ATH_FFT_SAMPLE_ATH10K:
                if (sample_len < sizeof(result->sample.ath10k.header)) {
                    fprintf(stderr, "wrong sample length (have %zd, expected at least %zd)\n",
                            sample_len, sizeof(result->sample.ath10k.header));
                    break;
                }

                bins = sample_len - sizeof(result->sample.ath10k.header);

                if (bins != 64 &&
                    bins != 128 &&
                    bins != 256) {
                    fprintf(stderr, "invalid bin length %d\n", bins);
                    break;
                }

                CONVERT_BE16(result->sample.ath10k.header.freq1);
                CONVERT_BE16(result->sample.ath10k.header.freq2);
                CONVERT_BE16(result->sample.ath10k.header.noise);
                CONVERT_BE16(result->sample.ath10k.header.max_magnitude);
                CONVERT_BE16(result->sample.ath10k.header.total_gain_db);
                CONVERT_BE16(result->sample.ath10k.header.base_pwr_db);
                CONVERT_BE64(result->sample.ath10k.header.tsf);

                handled = 1;
                break;
            default:
                fprintf(stderr, "unknown sample type (%d)\n", tlv->type);
                break;
        }

        if (!handled) {
            free(result);
            continue;
        }

        if (tail)
            tail->next = result;
        else
            result_list = result;

        tail = result;

        scanresults_n++;
    }

    //fprintf(stderr, "read %d scan results\n", scanresults_n);
    free(scandata);

    return 0;
}

static void free_scandata(void) {
    struct scanresult *list = result_list;
    struct scanresult *next;

    while (list) {
        next = list->next;
        free(list);
        list = next;
    }

    result_list = NULL;
}

static int compare( const void* a, const void* b) {
     int int_a = * ( (int*) a );
     int int_b = * ( (int*) b );

     if ( int_a == int_b ) return 0;
     else if ( int_a < int_b ) return -1;
     else return 1;
}


int main(int argc, char *argv[]) {
    int ch;
    char *ss_name = NULL;
    char *fontdir = NULL;
    char *prog = NULL;
    struct scanresult *result;
    int max_signal = -200;
    int avg_signal = 0;
    int counter = 0;
    int channel_freq = 0;
    int val = 0;
    double percentile = 0.95;
    if (argc >= 1)
        prog = argv[1];

    while ((ch = getopt(argc, argv, "f:h")) != -1) {
        switch (ch) {
            case 'f':
                if (fontdir)
                    free(fontdir);
                fontdir = strdup(optarg);
                break;
            case 's':
                if (ss_name)
                    free(ss_name);
                ss_name = strdup(optarg);
                break;
        }
    }
    argc -= optind;
    argv += optind;

    if (argc >= 1)
        ss_name = argv[0];

    // If a channel is specified, pass it to the eval function, only look at the channel with that center frequency
    if (argc >= 2)
        channel_freq = atoi(argv[1]);
    //fprintf(stderr, "WARNING: Experimental Software! Don't trust anything you see. :)\n");
    //fprintf(stderr, "\n");

    if (fontdir == NULL) {
        fontdir = strdup("./font/");
    }
    if (ss_name == NULL) {
        fprintf(stderr, "ERROR: need scan file\n");
        exit(127);
    }

    if (read_scandata(ss_name) < 0) {
        fprintf(stderr, "Couldn't read scanfile ...\n");
        return -1;
    }

    for (result = result_list; result; result = result->next) {
	
        if (argc < 2) {
            counter++;
            
        } else {
            if (result->sample.ath10k.header.freq1 == channel_freq) {
                counter++;
            }
        }
    }

    int rssi_arr[counter];
    counter = 0;

    for (result = result_list; result; result = result->next) {
	
        if (argc < 2) {
            val = result->sample.ath10k.header.noise + result->sample.ath10k.header.rssi;
            rssi_arr[counter] = val;
            counter++;
            if ((val) > max_signal) {
                max_signal = val;
            }
        } else {
            if (result->sample.ath10k.header.freq1 == channel_freq) {
                val = result->sample.ath10k.header.noise + result->sample.ath10k.header.rssi;
                //printf("%d\n", val);
                rssi_arr[counter] = val;
                counter++;
                avg_signal += val;
                
                if (val > max_signal) {
                    max_signal = val;
                }
            }
        }
    }
    qsort(rssi_arr, counter, sizeof(int), compare);
    //for (int j = 0; j < counter; j++) {
    //   printf("%d\n", rssi_arr[j]);
    //}

    struct timespec t;
    clock_gettime(CLOCK_REALTIME, &t);
    char **endp;
    uint64_t millitime = strtol(argv[2], NULL, 0);//S64(argv[3]);
    //printf("%x\n", millitime);
    //printf("%" PRId64, millitime);
    //printf("0x%" PRIx64 "\n", millitime);
    FILE* outfile = fopen(argv[3], "a");
    FILE* outfile2 = fopen(argv[4], "a");
    for (int shifter=0; shifter < 64; shifter += 8) {    
        fprintf(outfile, "%c", (unsigned int) ((millitime >> (56 - shifter)) &0xFF));
    }
    unsigned short meas_count = sizeof(rssi_arr)/sizeof(rssi_arr[0]);
    for (int shifter=0; shifter < 16; shifter += 8) {
        fprintf(outfile, "%c", (unsigned int) ((meas_count >> (8 - shifter)) & 0xFF));
    }
    for(int j=0; j<sizeof(rssi_arr)/sizeof(rssi_arr[0]); j++) {
        //printf("%x", ((char) rssi_arr[j]) & 0xff );
        //printf("%d \n", rssi_arr[j]);
        fprintf(outfile, "%c", (char) rssi_arr[j]);
    }

    fprintf(outfile2, "%d\n", rssi_arr[(int) round(counter * percentile) - 1]);
    //fprintf(outfile, "\n");
    fclose(outfile);
    fclose(outfile2);
    //printf("%d\n", sizeof(rssi_arr) / sizeof(rssi_arr[0]));
    //avg_signal /= counter;
    //printf("%d\n", avg_signal);
    //printf("%d\n", counter);
    //printf("%d\n", max_signal);
    free(fontdir);
    free_scandata();

    return 0;
}
