/*------------------------------------------------------------------
|			    OTC - Ontology Terminology Comparator              |
|				    FII = IA Project = 2017-2018                   |
|						   File: StdInc.h                          |
|                     Author(s): Rusu Cristian                     |
-------------------------------------------------------------------*/

#pragma once

#include <string>
#include <Windows.h>

#define EXIT_WITH_ERROR(msg) { MessageBox(NULL, msg, "Error!", MB_OK | MB_ICONERROR); ExitProcess(1); }