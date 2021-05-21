#include <stdio.h>
#include <string.h>

int main (int argc, char *argv[]) {
    if(argc <= 1) return 1;
    FILE *mf;
    char str[1024], firstStr[512], secondStr[512];
    char *estr;

    mf = fopen ("/var/lib/asterisk/documentation/text.txt","r");
    if (mf == NULL) return -1;
    while (1) {
	estr = fgets (str,sizeof(str),mf);
	if (estr == NULL) break;
	strcpy(firstStr, strtok(str, ";")); // First string
	strcpy(secondStr, strtok(NULL, ";")); // Second string
	secondStr[strcspn(secondStr, "\n")] = 0; // Clear \n symbol
	if(strcmp(secondStr, argv[1]) == 0) {
	    printf("SET VARIABLE calleridvar \"%s\"\n", firstStr);
	    fclose(mf);
	    return 0;
	}
    }
    printf ("SET VARIABLE calleridvar \"%s\"\n", argv[1]);
    fclose(mf);
    return 0;
}
