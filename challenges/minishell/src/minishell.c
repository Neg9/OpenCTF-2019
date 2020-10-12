#include <stdlib.h>
#include <stdio.h> 
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
//#include <sys/stat.h>
//#include <sys/sendfile.h>
//#include <errno.h>
#include <dirent.h>

static char *PROMPT = "$ ";
char *env_passwd = NULL;
char cwd[512];
char iobuf[256];
char *cmd;
char *arg;
char BUF[128];
int loop_main = 0;
int loop_cmp = 0;
int lock_delta = 0;
int errno = 0;


int cat(char* fname) {
   int fd = -1;
   int count = 0;
   fd = open(fname, O_RDONLY);
   if (fd < 0) {
      perror("open failed");
      return -1;
   }
   count = read(fd, iobuf, 256);
   while (count > 0){ 
      write(1, iobuf, count);
      count = read(fd, iobuf, 256);
   }
   if (count == -1){
      perror("read");
   }

   close(fd);
   return 0;
}



void ls(void) {
    struct dirent *de = NULL;  
    DIR *dr = opendir("."); 
    errno = 0;
    if ((dr == NULL) && (errno != 0)) { 
      perror("ls");
    } 
    while ((de = readdir(dr)) != NULL) {
       if (de->d_name[0] != '.'){
	  dprintf(1, "%s\n", de->d_name);
       }
    }
    closedir(dr);     
}


void get_cmd(void){
   char buf[128];
   size_t count = -1;
   
   write(1, PROMPT, 2);
   count = read(0, buf, 133);
   memcpy(BUF, buf, 128);
   
   if ((count > 0) && (count <= 128)) {
      BUF[count] = 0;
   }
   else {
      BUF[127] = 0;
   }

   cmd = strtok(BUF, " \r\n");
   arg = strtok(NULL, " \r\n");
   return; 
}



int main(int argc, char *argv[]) 
{ 
   char usr_passwd[] = "CCCCCCCC";
   
   env_passwd = getenv("PASSWORD");
   if (env_passwd == NULL){
      dprintf(1, "error: password was not set\n");
      exit(0);
   }

   for (loop_main=0; loop_main<100; loop_main++){
      cmd = NULL;
      arg = NULL;
      get_cmd();
            
      if (cmd != NULL) {
	 // memcmp - count the number of bytes that differ
	 lock_delta = 0;
	 for (loop_cmp=0; loop_cmp<8; loop_cmp++){
	    if (env_passwd[loop_cmp] != usr_passwd[loop_cmp]){
	       lock_delta++;
	    }
	 }
	 if (strcmp(cmd, "cat") == 0) {
	    if (arg != NULL){
	       if (lock_delta == 0 || strstr(arg, "flag") == NULL ) {
		  cat(arg);
	       } else {
		  dprintf(1, "%s\n", "Lol, nice try");
	       }
	    }
	 }
	 else if (strcmp(cmd, "echo") == 0){
	    if (arg != NULL){
	       dprintf(1, "%s\n", arg);
	    }
	 }
	 else if (strcmp(cmd, "cd") == 0){
	    if (arg != NULL){
	       errno = chdir(arg);
	       if (errno == -1){
		  perror("chdir");
	       }
	    }
	 }
	 else if (strcmp(cmd, "ls") == 0){
	    ls();
	 }
	 else if (strcmp(cmd, "pwd") == 0){
	    getcwd(cwd, 512);
	    dprintf(1, "%s\n", cwd); 
	 }
	 else if (strcmp(cmd, "quit") == 0 || (strcmp(cmd, "exit") == 0)){
	    exit(0);
	 }
	 else if (strcmp(cmd, "help") == 0) {
	    dprintf(1, "%s\n", "Yeah, you look like you need help alright.");
	 }
	 else if (strcmp(cmd, "sudo") == 0) {
	    dprintf(1, "%s\n", "Make me a sandwitch!");
	 }
	 //else if (cmd[0] == '\0'){
	    // empty string 
	// }
	 else {
	    dprintf(1, "command not found\n");
	 }
   
      } // end if null 
   } // end loop

   dprintf(1, "%s\n", "goodbye");
   exit(0);
} // end main

