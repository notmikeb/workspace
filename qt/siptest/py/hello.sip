%Module hello 0

%Import QtCore/QtCoremod.sip

class Hello : QString
{
%TypeHeaderCode
#include "../c++/hello.h"
%End

public:
  Hello();
};
