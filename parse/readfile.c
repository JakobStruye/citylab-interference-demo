#include <stdio.h>
#include <time.h>
#include <stdint.h>
#include <stdlib.h>
#include <inttypes.h>
#include <string>
int main (int argc, char* argv[])
{
 
  FILE * fileptr;
  unsigned char *buffer;
  int filelen;
  fileptr=fopen (("/mnt/hgfs/host/" + std::string(argv[1]) + "/" + std::string(argv[2]) + ".out").c_str(),"rb");
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
  bool defer = false;
  for (int i=0; i<filelen; i++) {
      if (ctr < 8) {
          time = time << 8;
          
          time = time | (uint64_t) buffer[i];
          if (ctr == 7) {
		  
              //printf("%" PRIu64 "\n", time);
	     }
      } else if (ctr < 10) {
	  defer=false;
          vals = vals << 8;
          vals = vals | (unsigned short) buffer[i];
          if (ctr == 9 && std::string(argv[3]) == "time" && vals > 0) {
              printf("%" PRIu64 "\n", time);
          }
          if (ctr == 9) {
              //printf("Count: %u\n", vals);
          }
      } else {
          if (vals > 0) {
              char val = *(char*) &(buffer[i]);
	      if (std::string(argv[3]) == "vals") {
		 if ( defer || valctr == (int) (atoi(argv[4]) / 100.0 * vals)) {
                     if ((int) val < -110 || (int) val > 0) {
		         defer=true;
	             }
                     else {		     
                         printf("%d\n", (int) val);
			 defer=false;
		     }
	          }
	      }
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
