#include <stdio.h>
#include <time.h>
#include <stdint.h>
#include <stdlib.h>
#include <inttypes.h>

int main ()
{
 
  FILE * fileptr;
  unsigned char *buffer;
  int filelen;
  fileptr=fopen ("../../raw_parse/74/5240.out","rb");
  fseek(fileptr, 0, SEEK_END);
  filelen = ftell(fileptr);
  rewind(fileptr);

  buffer = (unsigned char *)malloc((filelen+1)*sizeof(unsigned char));
  fread(buffer, filelen, 1, fileptr);
  fclose(fileptr);
  uint64_t time = 0;
  unsigned short vals = 0;
  int ctr = 0;
  int valctr = 0;
  for (int i=0; i<filelen; i++) {
      if (ctr < 8) {
          time = time << 8;
          
          time = time | (uint64_t) buffer[i];
          
          //printf("%x\n", time);
          if (ctr == 7) {
              printf("Time: %" PRIu64 "\n", time);
          }
      } else if (ctr < 10) {
          vals = vals << 8;
          vals = vals | (unsigned short) buffer[i];
          if (ctr == 9) {
              printf("Count: %u\n", vals);
          }
      } else {
          if (vals > 0) {
              char val = *(char*) &(buffer[i]);
              //printf("%d\n", (int) val);
              valctr++;
          }
          if (valctr == vals) {
              //SKIP 1
              if (vals > 0 && buffer[i+1] != 0) {
                  printf("BAD");
              } else if (vals > 0) {
                  i++;
              }
              vals = 0;
              valctr = 0;
              ctr = 0;
              time = 0;
          }
      }
      ctr++;
  }
  struct timespec t;
  clock_gettime(CLOCK_REALTIME, &t);
  int64_t millitime = t.tv_sec * INT64_C(1000) + t.tv_nsec / 1000000;
}

