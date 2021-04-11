/* KRY 2021 - Vigenere Cipher Analysis
 * Bc. Marian Kapisinsky, xkapis00
 * 4.4.2021
 * */

#ifndef KRY_H
#define KRY_H

using namespace std;

#define MIN_NGRAM 3
#define MAX_NGRAM 8

/* Letter frequencies in English */
double eng[26] = { 0.08167, // A
									 0.01492, // B
									 0.02782, // C
								   0.04253, // D
							  	 0.12702, // E
								   0.02228, // F
								   0.02015, // G
  								 0.06094, // H
	  							 0.06966, // I
		  						 0.00153,	// J
			  					 0.00772, // K
				  				 0.04025, // L
					  			 0.02406, // M
						  		 0.06749, // N
							  	 0.07507, // O
  								 0.01929, // P
	  							 0.00095, // Q
		  						 0.05987, // R
			  					 0.06327, // S
				  				 0.09056, // T
					  			 0.02758, // U
						  		 0.00978, // V
							  	 0.02360, // W
								   0.00150, // X
					  			 0.01974, // Y
						  		 0.00074 // Z
									};

unsigned count (string str, char c, unsigned length);

unsigned gcd (unsigned a, unsigned b);

double ioc (string str, unsigned length);

double friedman (string cipherText, unsigned length);

unsigned kasiski (string cipherText, unsigned length);

char shiftedFreqAnalysis (string coset);

unsigned getKeyLen (string cipherText, unsigned length);

string breakPasswd (string cipherText, unsigned length, unsigned keyLenght);

string readCipherText (void);

#endif //KRY_H
