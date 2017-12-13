/*------------------------------------------------------------------
|			    OTC - Ontology Terminology Comparator              |
|				    FII = IA Project = 2017-2018                   |
|						   File: Main.cpp                          |
|                     Author(s): Rusu Cristian                     |
-------------------------------------------------------------------*/

#include <iostream>
#include <string>
#include <fstream>
#include "StdInc.h"

using namespace std;

int main(int argc, char * argv[])
{
	// Check if program is called with correct number of commandline parameters
	if (argc < 4)
		EXIT_WITH_ERROR("Program called with invalid number of parameters!\n USAGE: otc.exe [input filename] [output filename]"
						" [sourcetext filename]");

	// Try and open each file
	ifstream inputFile(argv[1]);
	if (!inputFile.is_open())
		EXIT_WITH_ERROR("Unable to open inputfile!");

	ofstream outputFile(argv[2]);
	if (!outputFile.is_open())
		EXIT_WITH_ERROR("Unable to open outputfile!");

	ifstream sourceFile(argv[3]);
	if (!sourceFile.is_open())
		EXIT_WITH_ERROR("Unable to open sourcefile!");


	// Close file handles
	sourceFile.close();
	outputFile.close();
	inputFile.close();

	cout << "Sucessfully evaluated all terminology pairs! Exiting..." << endl;

	system("pause"); // To be removed on release
	return 0;
}