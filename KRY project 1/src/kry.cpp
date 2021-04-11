/* KRY 2021 - Vigenere Cipher Analysis
 * Bc. Marian Kapisinsky, xkapis00
 * 4.4.2021
 * */

#include <iostream>
#include <algorithm>
#include <numeric>
#include <string>
#include <vector>
#include <unordered_set>

#include "kry.hpp"

using namespace std;

unsigned count (string str, char c, unsigned length) {
	
	unsigned occur = 0;
	
	for (size_t i = 0; i < length; ++i)
		if (str[i] == c) ++occur; 

	return occur;
}

unsigned gcd (unsigned a, unsigned b) {
	
  if (a == 0) 
		return b;
	
  return gcd(b % a, a); 
} 

double ioc (string str, unsigned length) {
	
	unsigned letterCount[26];
	
	for (size_t i = 0; i < 26; ++i) {
		
		letterCount[i] = count(str, 'A' + i, length);
	}

	unsigned long sum = 0;
	
	/* Get letter counts in the cipher text */
	for (size_t i = 0; i < 26; ++i) {

		sum += letterCount[i] * (letterCount[i] - 1);
	}
	
	return ((double) sum) / ((double) (length * (length - 1)));
}

double friedman (string cipherText, unsigned length) {
	
	/* Calculate the index of coincidence */
	double coincidence =  ioc(cipherText, length);
	
	/* Calculate the key length using the Friedman test */
	return ( ( ( 0.065 - 0.0385 ) * (double) length ) / ( ( ( ( (double) length ) - 1 ) * coincidence ) - ( 0.0385 * (double) length ) + 0.065 ) );
}

unsigned kasiski (string cipherText, unsigned length) {
	
	vector<size_t> gcds;
	unordered_set<string> seen;
	
	for (size_t i = MAX_NGRAM; i >= MIN_NGRAM; --i) {
		
		for (size_t offset = 0; offset < (length - i + 1); ++offset) {
		
			vector<size_t> positions;
			vector<size_t> distances;
			
			/*Select an ngram*/
			string ngram = cipherText.substr(offset, i);
			
			/* Skip if seen */
			if (seen.find(ngram) == seen.end())
				seen.insert(ngram);
			else
				continue;
				
			size_t pos = cipherText.find(ngram);
			
			/*Get all positions of ngram occurecne*/
			while (pos != string::npos) {
				
				positions.push_back(pos);
				pos = cipherText.find(ngram,pos+1);
			}
			
			/*Skip if the ngram appears only once*/
			if (positions.size() < 2 ) continue;
			
			/* Calculate distances */
			for (size_t j = 0; j < positions.size() - 1; ++j) {
					
				size_t distance = positions[j+1] - positions[j];
				distances.push_back(distance);
			}
			
			/*Calculate the greatest common divisor for each vector of distances*/
			unsigned result = distances[0];
			for (size_t i = 1; i < distances.size(); ++i) {
				
				unsigned tmp = gcd(distances[i], result);
				/*Skip possible random ngram occurecne*/
				if (tmp == 1) continue;
				result =  tmp;
			}
			
			/*Skip very unlikely key lengths of 1, 2 or 3*/
			if (result > 3) gcds.push_back(result);
		}
	}
	
	sort(gcds.begin(), gcds.end());
	
	unsigned currentFreq = 0;
	unsigned maxFreq = 0;
	unsigned mostFreq = 0;
	unsigned lastSeen = 0;
	
	/* Find the most freqeunt gcd */
	for( auto &gcd : gcds ) {
		
    if( gcd == lastSeen ) {
			++currentFreq;
		}
    else {
			
      if( currentFreq > maxFreq ) {
				
        maxFreq = currentFreq;
        mostFreq = lastSeen;
			}

			lastSeen = gcd;
      currentFreq = 1;
		}
 }
	
	unsigned kasiski = mostFreq;
	
	return kasiski;
}

char shiftedFreqAnalysis (string substring) {

	unsigned length = substring.length();
	double letterFreq[26];
	
	/* Calculate letter frequencies in the substring */
	for (size_t i = 0; i < 26; ++i)
		letterFreq[i] = ((double) count(substring, 'A' + i, length)) / (double) length;
		
	double result[26];
	
	/* Perform the shifted frequency analysis */
	for (size_t i = 0; i < 26; ++i) {
		
		double sum = 0;
		double tmp[26];
		
		for (size_t j = 0; j < 26; ++j) {
			tmp[j] = letterFreq[(i + j) % 26] * eng[j];
		}
		
		for (size_t j = 0; j < 26; ++j) {
			sum += tmp[j];
		}
		
		result[i] = sum;
	}
	
	unsigned letter;
	double max = 0.0;
	
	/* Find the letter with highest value of coincidence */
	for (size_t i = 0; i < 26; ++i) {
		
		if ( result[i] > max ) {
			
			max = result[i];
			letter = i;
		}
	}

	return ('A' + letter);
}

string breakPasswd (string cipherText, unsigned length, unsigned keyLenght) {
	
	string substrings[keyLenght];
	
	/* Get all substrings */
	for (size_t i = 0; i < length; ++i)
		substrings[i % keyLenght] += cipherText[i];
	
	string passwd = "";
	
	/* Use the shifted frequency analysis and break the password */
	for (size_t i = 0; i < keyLenght; ++i)
		passwd += shiftedFreqAnalysis(substrings[i]);
	
	return passwd;
}

unsigned getKeyLen (string cipherText, unsigned length) {
	
	/* Minimal key length */
	unsigned keyLenght = 4;
	
	/* Try all key lengths from 4 to 200 */

	while (keyLenght <= 200) {
				
		string substring = "";
			
		/* Get substring */
		for (size_t i = 0; i < length; ++i)
			if (i % keyLenght == 0) substring += cipherText[i];
		
		double coincidence = ioc(substring, substring.length());

		if (coincidence >= 0.060) return keyLenght;
		
		++keyLenght;
	}
	
	return 0;
}

string readCipherText (void) {
	
	string cipherText;
	
	/* Read stdin */
	for (string line; getline(cin, line);)
    cipherText.append(line);
	
	/* Remove punctuation and white spaces */
  for (size_t i = 0, len = cipherText.size(); i < len; i++) { 

    if (!isalpha(cipherText[i])) {
		
      cipherText.erase(i--, 1);
      len = cipherText.size();
    }
  }
	
	/* Convert to upper case */
	for (auto &c : cipherText)
		c = toupper(c);

	return cipherText;
}

int main (void) {

	string cipherText = readCipherText();
	
	unsigned length = cipherText.length();
	
	/* Friedman's test */
	double friedmanResult = friedman(cipherText, length);

	/* Kasiski's test */
	unsigned kasiskiResult = kasiski(cipherText, length);

	/* Key Length Estimation */
	unsigned keyLenght = getKeyLen(cipherText, length);

	/* Key Estimation */
	string passwd = breakPasswd(cipherText, length, keyLenght);
	
	cout << friedmanResult << ";" << kasiskiResult << ";" << keyLenght << ";" << passwd << endl;
	
	return 0;
}