/* PRL 2021 - Pipeline-Merge Sort
 * Bc. Marian Kapisinsky, xkapis00
 * 9.4.2021
 * */
	
#include <iostream>
#include <fstream>
#include <queue>
#include <math.h>
#include <mpi.h>

using namespace std;

#define TAG 0

int main ( int argc, char **argv ) {
	
	int nprocs;
	int id;
	int num;
	MPI_Status status;
	
	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
	MPI_Comm_rank(MPI_COMM_WORLD, &id);

	if (id == 0) {
		
		char input[] = "numbers";
		int number;
		fstream fin;
		
		fin.open(input, ios::in);
		
		while (fin.good()) {
			number = fin.get();
			if (!fin.good()) break;
			cout << number << " ";
			MPI_Send(&number, 1, MPI_INT, id + 1, TAG, MPI_COMM_WORLD);
		}
		cout << endl;
		fin.close();
	}
	else {
	
		int size = pow(2, id - 1);
		queue<int> q1, q2;
		
		int received = 0;
		int received1 = 0;
		int received2 = 0;
		
		for (size_t i = 0; i < size + 1; ++i) {
			
			MPI_Recv(&num, 1, MPI_INT, id - 1, TAG, MPI_COMM_WORLD, &status);
			++received;
			
			if (q1.size() != size) {
				q1.push(num);
				++received1;
			}
			else {
				q2.push(num);
				++received2;
			}
		}

		int size1 = size;
		int size2 = size;
		
		while (q1.size() > 0 || q2.size() > 0) {
			
			// 1. Send
			if (size1 == 0 && size2 >= 1) {
				
				if (id != (nprocs - 1))
					MPI_Send(&q2.front(), 1, MPI_INT, id + 1, TAG, MPI_COMM_WORLD);
				else
					cout << q2.front() << endl;
					
				q2.pop();
				--size2;
			}			
			else if (size2 == 0 && size1 >= 1) {
				
				if (id != (nprocs - 1))
					MPI_Send(&q1.front(), 1, MPI_INT, id + 1, TAG, MPI_COMM_WORLD);
				else
					cout << q1.front() << endl;
					
				q1.pop();
				--size1;
			}
			else if (size1 > 0 && size2 > 0) {
				if (q1.front() < q2.front()) {
					if (id != (nprocs - 1))
						MPI_Send(&q1.front(), 1, MPI_INT, id + 1, TAG, MPI_COMM_WORLD);
					else
						cout << q1.front() << endl;
					
					q1.pop();
					--size1;
				}
				else {	
					if (id != (nprocs - 1))
						MPI_Send(&q2.front(), 1, MPI_INT, id + 1, TAG, MPI_COMM_WORLD);
					else
						cout << q2.front() << endl;
						
					q2.pop();
					--size2;
				}
			}
			
			if (size1 == 0 && size2 == 0) {	
				size1 = size;
				size2 = size;
			}
			
			// 2. Receive
			if (received != 16) {
				MPI_Recv(&num, 1, MPI_INT, id - 1, TAG, MPI_COMM_WORLD, &status);
				++received;
							
				if (received1 == size && received2 == size) {
					received1 = 0;
					received2 = 0;
				}
				
				// 3. Store to a queue
				if (received1 != size) {
					q1.push(num);
					++received1;
				}
				else {
					q2.push(num);
					++received2;
				}
			}
		}
	}
	
	MPI_Finalize();
	return 0;
}