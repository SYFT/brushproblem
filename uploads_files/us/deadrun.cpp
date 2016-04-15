#include <windows.h>
#include <ctime>
#include <iostream>
#include <unistd.h>
#include <cstdio>
using namespace std;

int main() {
	int index = 0;
	while(clock() < 10000) {
		sleep(3.5);
		printf("case %d\n", index++);
		//cout << index++ << endl;
	}
	return 0;
}
