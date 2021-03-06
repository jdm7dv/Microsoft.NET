//
// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.
//

//----------------------------------------------------------
// SpmiDumpHelper.h - a helper to dump structs that are used in JitEEInterface calls and spmi collections.
//----------------------------------------------------------

#ifndef _SpmiDumpHelper
#define _SpmiDumpHelper

#include "methodcontext.h"

class SpmiDumpHelper
{
public:
    static std::string DumpAgnostic_CORINFO_RESOLVED_TOKENin(
        const MethodContext::Agnostic_CORINFO_RESOLVED_TOKENin& tokenIn);
    static std::string DumpAgnostic_CORINFO_RESOLVED_TOKENout(
        const MethodContext::Agnostic_CORINFO_RESOLVED_TOKENout& tokenOut);
    static std::string DumpAgnostic_CORINFO_RESOLVED_TOKEN(const MethodContext::Agnostic_CORINFO_RESOLVED_TOKEN& token);

private:
    static const int MAX_BUFFER_SIZE = 1000;
};

#endif
