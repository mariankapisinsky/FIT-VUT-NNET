/* PRL 2021 - Mesh Multiplication
 * Bc. Marian Kapisinsky, xkapis00
 * 3.5.2021
 * */

#include <iostream>
#include <fstream>
#include <queue>
#include <stack>
#include <iomanip>
#include <mpi.h>
#include <time.h>


using namespace std;

#define TAG 0

/* Structure for storing matrices */
typedef struct {
	vector < vector <int> > matrix;
	int rows;
	int cols;
} matrix_t;


/* Read matrix 1 */
matrix_t readMat1() {

	matrix_t mat1;

	fstream fin;
	fin.open("mat1", ios::in);

	int rows;
	fin >> rows;

	vector <int> numbers;
	int number;

	while (fin >> number) {
		numbers.push_back(number);
	}

	fin.close();

	int cols = numbers.size() / rows;

	mat1.rows = rows;
	mat1.cols = cols;

	vector <int> row;

	for (size_t i = 0; i < numbers.size(); ++i) {

		row.push_back(numbers[i]);
		if (row.size() % cols == 0) {
			mat1.matrix.push_back(row);
			row.clear();
		}
	}

	return mat1;
}

/* Read matrix 2 */
matrix_t readMat2() {

	matrix_t mat2;

	fstream fin;
	fin.open("mat2", ios::in);

	int cols;
	fin >> cols;

	vector <int> numbers;
	int number;

	while (fin >> number) {
		numbers.push_back(number);
	}

	fin.close();

	int rows = numbers.size() / cols;

	mat2.rows = rows;
	mat2.cols = cols;

	vector <int> row;

	for (size_t i = 0; i < numbers.size(); ++i) {

		row.push_back(numbers[i]);
		if (row.size() % cols == 0) {
			mat2.matrix.push_back(row);
			row.clear();
		}
	}

	return mat2;
}

/* Print matrix */
void printMat(matrix_t mat) {

	cout << mat.rows << ':' << mat.cols << endl;

	int num;
	for (size_t i = 0; i < mat.rows; ++i) {
		for (size_t j = 0; j < mat.cols; ++j) {
			num = mat.matrix[i][j];
			cout << num << ' ';
		}
		cout << endl;
	}
}

/* Queue reverse */
void reverseQueue(queue<int> &q) {

	stack<int> s;
	while (!q.empty()) {
		s.push(q.front());
		q.pop();
	}
	while (!s.empty()) {
		q.push(s.top());
		s.pop();
 	}
}

int main ( int argc, char **argv ) {

	int nprocs;
	int id;
	MPI_Status status;

	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
	MPI_Comm_rank(MPI_COMM_WORLD, &id);

	// Main process
	if ( id == 0 ) {

		// Read matrices
		matrix_t mat1 = readMat1();
		matrix_t mat2 = readMat2();
		matrix_t mat3;

		// Check wether the number of column of matrix 1 == number of rows of matrix 2
		if (mat1.cols != mat2.rows) {
			cerr << "Wrong matrix sizes" << endl;
			MPI_Abort(MPI_COMM_WORLD, 1);
		}

		mat3.rows = mat1.rows;
		mat3.cols = mat2.cols;

		vector <queue<int>> aQ;
		vector <queue<int>> bQ;

		// Prepare input queues for edge processes
		for (size_t i = 0; i < mat1.rows; ++i) {
			queue<int> q;
			for (size_t j = 0; j < mat1.cols; ++j) {
				q.push(mat1.matrix[i][j]);
			}
			reverseQueue(q);
			aQ.push_back(q);
		}

		for (size_t i = 0; i < mat2.cols; ++i) {
			queue<int> q;
			for (size_t j = 0; j < mat2.rows; ++j) {
				q.push(mat2.matrix[j][i]);
			}
			reverseQueue(q);
			bQ.push_back(q);
		}

		// Broadcast the final matrix size and input matrices shared dimmension
		MPI_Bcast(&mat3.rows, 1, MPI_INT, TAG, MPI_COMM_WORLD);
		MPI_Bcast(&mat3.cols, 1, MPI_INT, TAG, MPI_COMM_WORLD);
		MPI_Bcast(&mat1.cols, 1, MPI_INT, TAG, MPI_COMM_WORLD);

		// Send queues to edge processes
		int num;
		for (size_t i = 1; i < mat3.rows; ++i) {
			while (!aQ[i].empty()) {
				num = aQ[i].front();
				MPI_Send(&num, 1, MPI_INT, i * mat3.cols, TAG, MPI_COMM_WORLD);
				aQ[i].pop();
			}
		}

		for (size_t i = 1; i < mat3.cols; ++i) {
			while (!bQ[i].empty()) {
				num = bQ[i].front();
				MPI_Send(&num, 1, MPI_INT, i, TAG, MPI_COMM_WORLD);
				bQ[i].pop();
			}
		}

		int a;
		int b;
		int c = 0;

		/*** START TIME MEASURING ***/
		
    //struct timespec begin, end;
    //clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &begin);

		// Process the input queue and forward processed numbers
		while (!aQ[0].empty() && !bQ[0].empty()) {

			a = aQ[0].front();
			b = bQ[0].front();

			// Multiply and sum
			c += a * b;

			// Forward right
			if (mat3.cols > 1)
				MPI_Send(&a, 1, MPI_INT, id+1, TAG, MPI_COMM_WORLD);

			// Forward down
			if (mat3.rows > 1)
				MPI_Send(&b, 1, MPI_INT, mat3.cols, TAG, MPI_COMM_WORLD);

			aQ[0].pop();
			bQ[0].pop();
		}

		// Collect and store the results
		vector <int> row;
		if (nprocs == 1) {
			row.push_back(c);
			mat3.matrix.push_back(row);
		}
		else {
			for (size_t i = 0; i < nprocs; ++i) {

				if (i == 0)
					num = c;
				else
					MPI_Recv(&num, 1, MPI_INT, i, TAG, MPI_COMM_WORLD, &status);

				row.push_back(num);

				if (row.size() % mat3.cols == 0) {
					mat3.matrix.push_back(row);
					row.clear();
				}
			}
		}


		/*** STOP TIME MEASURING AND PRINT ***/

		//clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
		//long seconds = end.tv_sec - begin.tv_sec;
		//long nanoseconds = end.tv_nsec - begin.tv_nsec;
		//double elapsed = (seconds + nanoseconds*1e-9) * 1000;

		//printf("Time measured: %.9f milliseconds.\n", elapsed);

		// Print the final matrix
		printMat(mat3);
	}
	else {

		int rows;
		int cols;
		int n;

		// Get the final matrix size and input matrices shared dimmension
		MPI_Bcast(&rows, 1, MPI_INT, TAG, MPI_COMM_WORLD);
		MPI_Bcast(&cols, 1, MPI_INT, TAG, MPI_COMM_WORLD);
		MPI_Bcast(&n, 1, MPI_INT, TAG, MPI_COMM_WORLD);

		int a;
		int b;
		int c = 0;

		// Top edge processes
		if (id < cols) {

			queue<int> bQ;

			// Get input queue
			int num;
			for (size_t i = 0; i < n; ++i) {

				MPI_Recv(&num, 1, MPI_INT, 0, TAG, MPI_COMM_WORLD, &status);
				bQ.push(num);
			}

			for (size_t i = 0; i < n; ++i) {

				// Get numbers
				MPI_Recv(&a, 1, MPI_INT, id - 1, TAG, MPI_COMM_WORLD, &status);
				b = bQ.front();

				// Multiply and sum
				c += a * b;

				// Forward right
				if ((id + 1) % cols != 0)
					MPI_Send(&a, 1, MPI_INT, id + 1, TAG, MPI_COMM_WORLD);

				// Forward down
				if (id < (rows - 1) * cols)
					MPI_Send(&b, 1, MPI_INT, id + cols, TAG, MPI_COMM_WORLD);

				bQ.pop();
			}

		}
		// Left edge processses
		else if (id % cols == 0) {

			queue<int> aQ;

			// Get input queue
			int num;
			for (size_t i = 0; i < n; ++i) {

				MPI_Recv(&num, 1, MPI_INT, 0, TAG, MPI_COMM_WORLD, &status);
				aQ.push(num);
			}

			for (size_t i = 0; i < n; ++i) {

				// Get numbers
				a = aQ.front();
				MPI_Recv(&b, 1, MPI_INT, id - cols, TAG, MPI_COMM_WORLD, &status);

				// Multiply and sum
				c += a * b;

				// Forward right
				if ((id + 1) % cols != 0)
					MPI_Send(&a, 1, MPI_INT, id + 1, TAG, MPI_COMM_WORLD);

				// Forward down
				if (id < (rows - 1) * cols)
					MPI_Send(&b, 1, MPI_INT, id + cols, TAG, MPI_COMM_WORLD);

				aQ.pop();
			}

		}
		// All other processes
		else {

			for (size_t i = 0; i < n; ++i) {

				// Get numbers
				MPI_Recv(&a, 1, MPI_INT, id - 1, TAG, MPI_COMM_WORLD, &status);
				MPI_Recv(&b, 1, MPI_INT, id - cols, TAG, MPI_COMM_WORLD, &status);

				// Multiply and sum
				c += a * b;

				// Forward right
				if ((id + 1) % cols != 0)
					MPI_Send(&a, 1, MPI_INT, id + 1, TAG, MPI_COMM_WORLD);

				// Forward down
				if (id < (rows - 1) * cols)
					MPI_Send(&b, 1, MPI_INT, id + cols, TAG, MPI_COMM_WORLD);

			}

		}

		// Send the result to the main process
		MPI_Send(&c, 1, MPI_INT, 0, TAG, MPI_COMM_WORLD);
	}

	MPI_Finalize();
	return 0;
}
