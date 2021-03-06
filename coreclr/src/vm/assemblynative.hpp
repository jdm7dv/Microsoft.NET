// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.
// See the LICENSE file in the project root for more information.

/*============================================================
**
** Header:  AssemblyNative.hpp
**
** Purpose: Implements FCalls for managed Assembly class
**
**


**
===========================================================*/
#ifndef _ASSEMBLYNATIVE_H
#define _ASSEMBLYNATIVE_H

class CLRPrivBinderAssemblyLoadContext;

class AssemblyNative
{
    friend class Assembly;
    friend class BaseDomain;
    friend class DomainAssembly;

public:
    // static FCALLs
    static
    void QCALLTYPE GetEntryAssembly(QCall::ObjectHandleOnStack retAssembly);
   
    static
    void QCALLTYPE GetExecutingAssembly(QCall::StackCrawlMarkHandle stackMark, QCall::ObjectHandleOnStack retAssembly);

    static FCDECL7(Object*,         Load,                       AssemblyNameBaseObject* assemblyNameUNSAFE, 
                                                                StringObject* codeBaseUNSAFE, 
                                                                AssemblyBaseObject* requestingAssemblyUNSAFE,
                                                                StackCrawlMark* stackMark,
                                                                ICLRPrivBinder * pPrivHostBinder,
                                                                CLR_BOOL fThrowOnFileNotFound,
                                                                INT_PTR ptrLoadContextBinder);

    //
    // instance FCALLs
    //

    static 
    void QCALLTYPE GetLocale(QCall::AssemblyHandle pAssembly, QCall::StringHandleOnStack retString);

    static
    INT32 QCALLTYPE GetHashAlgorithm(QCall::AssemblyHandle pAssembly);


    static 
    void QCALLTYPE GetSimpleName(QCall::AssemblyHandle pAssembly, QCall::StringHandleOnStack retSimpleName);

    static 
    void QCALLTYPE GetPublicKey(QCall::AssemblyHandle pAssembly, QCall::ObjectHandleOnStack retPublicKey);

    static
    INT32 QCALLTYPE GetFlags(QCall::AssemblyHandle pAssembly);

    static 
    void QCALLTYPE GetFullName(QCall::AssemblyHandle pAssembly, QCall::StringHandleOnStack retString);

    static 
    void QCALLTYPE GetLocation(QCall::AssemblyHandle pAssembly, QCall::StringHandleOnStack retString);

    static
    void QCALLTYPE GetCodeBase(QCall::AssemblyHandle pAssembly, BOOL fCopiedName, QCall::StringHandleOnStack retString);

    static 
    BYTE * QCALLTYPE GetResource(QCall::AssemblyHandle pAssembly, LPCWSTR wszName, UINT64 * length, QCall::StackCrawlMarkHandle stackMark, BOOL skipSecurityCheck);

    static 
    BOOL QCALLTYPE GetNeutralResourcesLanguageAttribute(QCall::AssemblyHandle pAssembly, QCall::StringHandleOnStack cultureName, INT16& outFallbackLocation);

    static
    FCDECL1(FC_BOOL_RET, IsDynamic, AssemblyBaseObject * pAssemblyUNSAFE);

    static
    void QCALLTYPE GetVersion(QCall::AssemblyHandle pAssembly, INT32* pMajorVersion, INT32* pMinorVersion, INT32*pBuildNumber, INT32* pRevisionNumber);

    static
    void QCALLTYPE LoadModule(QCall::AssemblyHandle pAssembly, 
                                             LPCWSTR wszModuleName,
                                             LPCBYTE pRawModule, INT32 cbModule,
                                             LPCBYTE pRawSymbolStore, INT32 cbSymbolStore,
                                             QCall::ObjectHandleOnStack retModule);

    static 
    void QCALLTYPE GetType(QCall::AssemblyHandle pAssembly, LPCWSTR wszName, BOOL bThrowOnError, BOOL bIgnoreCase, QCall::ObjectHandleOnStack retType, QCall::ObjectHandleOnStack keepAlive);
    
    static 
    INT32 QCALLTYPE GetManifestResourceInfo(QCall::AssemblyHandle pAssembly, LPCWSTR wszName, QCall::ObjectHandleOnStack retAssembly, QCall::StringHandleOnStack retFileName, QCall::StackCrawlMarkHandle stackMark);

    static 
    BOOL QCALLTYPE UseRelativeBindForSatellites();

    static
    void QCALLTYPE GetModules(QCall::AssemblyHandle pAssembly, BOOL fLoadIfNotFound, BOOL fGetResourceModules, QCall::ObjectHandleOnStack retModules);

    static
    void QCALLTYPE GetModule(QCall::AssemblyHandle pAssembly, LPCWSTR wszFileName, QCall::ObjectHandleOnStack retModule);

    static
    void QCALLTYPE GetExportedTypes(QCall::AssemblyHandle pAssembly, QCall::ObjectHandleOnStack retTypes);

    static
    void QCALLTYPE GetForwardedTypes(QCall::AssemblyHandle pAssembly, QCall::ObjectHandleOnStack retTypes);

    static FCDECL1(Object*, GetManifestResourceNames, AssemblyBaseObject * pAssemblyUNSAFE);
    static FCDECL1(Object*, GetReferencedAssemblies, AssemblyBaseObject * pAssemblyUNSAFE);

    static 
    void QCALLTYPE GetEntryPoint(QCall::AssemblyHandle pAssembly, QCall::ObjectHandleOnStack retMethod);

    static FCDECL1(ReflectModuleBaseObject *, GetOnDiskAssemblyModule, AssemblyBaseObject * pAssemblyUNSAFE);
    static FCDECL1(ReflectModuleBaseObject *, GetInMemoryAssemblyModule, AssemblyBaseObject * pAssemblyUNSAFE);

    static 
    void QCALLTYPE GetImageRuntimeVersion(QCall::AssemblyHandle pAssembly, QCall::StringHandleOnStack retString);


    //
    // AssemblyBuilder FCALLs
    //

    static
    void QCALLTYPE PrepareForSavingManifestToDisk(QCall::AssemblyHandle pAssembly, QCall::ModuleHandle pAssemblyModule);


    static
    mdFile QCALLTYPE AddFile(QCall::AssemblyHandle pAssembly, LPCWSTR wszFileName);

    static 
    void QCALLTYPE SetFileHashValue(QCall::AssemblyHandle pAssembly, INT32 tkFile, LPCWSTR wszFullFileName);

    static
    void QCALLTYPE AddStandAloneResource(QCall::AssemblyHandle pAssembly, LPCWSTR wszName, LPCWSTR wszFileName, LPCWSTR wszFullFileName, INT32 iAttribute);

    static
    void QCALLTYPE AddDeclarativeSecurity(QCall::AssemblyHandle pAssembly, INT32 action, PVOID blob, INT32 length);


    static
    void QCALLTYPE GetRawBytes(QCall::AssemblyHandle pAssembly, QCall::ObjectHandleOnStack retRawBytes);

    //
    // PEFile QCalls
    // 
    
    static
    void QCALLTYPE ReleaseSafePEFileHandle(PEFile *pPEFile);

#ifdef FEATURE_APPX
    static
    BOOL QCALLTYPE IsDesignerBindingContext(QCall::AssemblyHandle pAssembly);
#endif

    static INT_PTR QCALLTYPE InitializeAssemblyLoadContext(INT_PTR ptrManagedAssemblyLoadContext, BOOL fRepresentsTPALoadContext);
    static BOOL QCALLTYPE OverrideDefaultAssemblyLoadContextForCurrentDomain(INT_PTR ptrNativeAssemblyLoadContext);
    static BOOL QCALLTYPE CanUseAppPathAssemblyLoadContextInCurrentDomain();
    static void QCALLTYPE LoadFromPath(INT_PTR ptrNativeAssemblyLoadContext, LPCWSTR pwzILPath, LPCWSTR pwzNIPath, QCall::ObjectHandleOnStack retLoadedAssembly);
    static INT_PTR QCALLTYPE InternalLoadUnmanagedDllFromPath(LPCWSTR unmanagedLibraryPath);
    static void QCALLTYPE LoadFromStream(INT_PTR ptrNativeAssemblyLoadContext, INT_PTR ptrAssemblyArray, INT32 cbAssemblyArrayLength, INT_PTR ptrSymbolArray, INT32 cbSymbolArrayLength, QCall::ObjectHandleOnStack retLoadedAssembly);
    static Assembly* LoadFromPEImage(ICLRPrivBinder* pBinderContext, PEImage *pILImage, PEImage *pNIImage);
    static INT_PTR QCALLTYPE GetLoadContextForAssembly(QCall::AssemblyHandle pAssembly);

    static BOOL QCALLTYPE InternalTryGetRawMetadata(QCall::AssemblyHandle assembly, UINT8 **blobRef, INT32 *lengthRef);
};

#endif

