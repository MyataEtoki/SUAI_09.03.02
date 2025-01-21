#include <iostream>
using namespace std;
 
int main(){
   char s[]="   7   54,  3  33   1,  3  ";
   int *arr,i=0,j=0,*t,p=10,count=0;
 
   t=new int[strlen(s)];
   for(i=0;i<strlen(s);i++)
        t[i]=0;
   i=0;
   while(s[i]!='\0'){
     if(isdigit(s[i])){
         t[j]=p*t[j]+(s[i]-'0');
         if(!isdigit(s[i+1]))j++,count++;
     }
     i++;
   }
   arr=new int[count];
   for(i=0;i<count;i++){
       arr[i]=t[i];
       cout<<arr[i]<<",";
   }
   cout<<"\b";
   delete []t;
   delete []arr;
 
   system("pause");
   return 0;
}