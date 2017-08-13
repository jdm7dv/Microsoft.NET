// Copyright (c) Microsoft.  All Rights Reserved.  Licensed under the Apache License, Version 2.0.  See License.txt in the project root for license information.

using System;

namespace Microsoft.VisualStudio.LanguageServices.CSharp.CodeModel
{
    [Flags]
    internal enum ModifierFlags
    {
        // Note: These are in the order that they appear in modifier lists as generated by Code Model.

        Public = 1 << 0,
        Protected = 1 << 1,
        Internal = 1 << 2,
        Private = 1 << 3,
        Virtual = 1 << 4,
        Abstract = 1 << 5,
        New = 1 << 6,
        Override = 1 << 7,
        Sealed = 1 << 8,
        Static = 1 << 9,
        Extern = 1 << 10,
        Volatile = 1 << 11,
        ReadOnly = 1 << 12,
        Const = 1 << 13,
        Unsafe = 1 << 14,
        Async = 1 << 15,
        Partial = 1 << 16,

        AccessModifierMask = Private | Protected | Internal | Public
    }
}
