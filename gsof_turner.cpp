#include<stdio.h>
#include<string.h>
#include<math.h>
#include<Windows.h> 
const double pi = 3.1415982;
int main(){
	char lat_[8], lon_[8], head_[4], vel_n_[4], vel_e_[4];
	double lat = 0.0, lon = 0.0;
	float head = 0.0, vel_n = 0.0, vel_e = 0.0;
	FILE *fp;       
	char temp;       
	char buf[1000] = {'a','b','c','d'};
	int len = 0;        
	if((fp=fopen("com6","r"))==NULL) 
		puts("Can't open com6 /n"); 
	else 
		puts("thiw way works!/n");
	printf("%d\n", strlen(buf));  
	memset(buf,'\0',strlen(buf));
	printf("%d\n", strlen(buf));  
	while(1)        
	{   
		if(len < 999){
			temp=0;            
			fscanf(fp,"%c",&temp);
			buf[len] = temp;
			len += 1;
		}
		else{
			//处理字符串； 
			for(int i = 0; i < len; i++){
				if(buf[i] == 20 && buf[i+1] == 100 && i + 103 < len){//找到头 
					int j = i + 15 + 1;//纬度的头 
					int k = 0;
					for(; k < 8; k+=1){
						lat_[k] = buf[j];
						j += 1;
					}
					k = 0;
					for(; k < 8; k+=1){
						lon_[k] = buf[j];
						j += 1;
					}
					k = 0;
					j += 8;
					for(; k < 4; k+=1){
						vel_n_[k] = buf[j];
						j += 1;
					}
					k = 0;
					for(; k < 4; k+=1){
						vel_e_[k] = buf[j];
						j += 1;
					}
					k = 0;
					j += 4*7;
					for(; k < 4; k+=1){
						head_[k] = buf[j];
						j += 1;
					}
					lat = *((double*)lat_) * 180 / pi;
					lon = *((double*)lon_) * 180 / pi;
					vel_n = *((float*)vel_n_);
					vel_e = *((float*)vel_e_);
					head = *((float*)head_);
					printf("%f\t%f\t%f\t%f\t%f\t\n",lat,lon,vel_n,vel_e,head);
				}
			}
			
			len = 0;
			memset(buf,'\0',strlen(buf));
		}
		/*if(temp!=0)                
			putchar(temp);            
		else                
			Sleep(100);
		*/        
	}        
	fclose(fp);        
	return 0; 
	/*
	//char lat[8] = {0x3F, 0xE1, 0xCF, 0x4B,0x0C ,0x28, 0x3E, 0xCC};
	char lat[8]  = {0xCC, 0x3E ,0x28, 0x0C ,0x4B ,0xCF ,0xE1 ,0x3F};
	double* a;
	a = (double*)lat;
	double lati = *a * 180 /pi;
	printf("%f", lati);*/
	
}
