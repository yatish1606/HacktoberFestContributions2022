#include<iostream>
using namespace std;

int main()
{
    for(int i=4;i>=0;i--)
    {
        for(int j=0;j<=i;j++)
        cout<<" ";

        for(int l=1, k=4;k>=i;k--, l++)
        cout<<l<<" ";
        
        cout<<endl;
    }
    return 0;
}

/*

     1 
    1 2
   1 2 3
  1 2 3 4
 1 2 3 4 5

*/