#include "./sha.h"
#include <string.h>
#include <stdio.h>

using namespace Merak::sha;
using namespace std;

int main() {
	unsigned char digest[20];
	char* str = "hello world";

	SHA_CTX ctx;
	SHA1_Init(&ctx);
	SHA1_Update(&ctx, str, strlen(str));
	SHA1_Final(digest, &ctx);
	char mdString[41]; 
	for (int i = 0; i < 20; i++)  
		sprintf(&mdString[i*2], "%02x", (unsigned int)digest[i]);  
	printf("SHA1 digest: %s\n", mdString);
	return 0;
}