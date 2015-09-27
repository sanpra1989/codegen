#include "codegen.h"
class PY_EXPORTED Class1
{
    
    public:
    enum Class1Types
    {
        CT_TYPE1,
        CT_TYPE2=3,
        CT_TYPE4
    };
     PY_HIDDEN void fn1();
     void fn2();
};


class PY_EXPORTED Class2
{
    
    public:
     void fn1();
    private:
     void fn2();
};
