#include<stdio.h>
int main()
{
	unsigned char arr[3];
	arr[0] = 0x24;
	arr[1] = 0x47;
	arr[2] = 0x50;
	char arr1[3];
	arr1[0] = (char)arr[0];
	arr1[1] = (char)arr[1];
	arr1[2] = (char)arr[2];
	printf("%c%c%c",arr[0],arr[1],arr[2]);
	return 0;
}
