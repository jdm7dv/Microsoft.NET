﻿// Copyright (c) Microsoft.  All Rights Reserved.  Licensed under the Apache License, Version 2.0.  See License.txt in the project root for license information.

using System;
using System.IO;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.Host;
using Microsoft.VisualStudio.LanguageServices.Implementation.TaskList;
using Microsoft.VisualStudio.Shell.Interop;
using Microsoft.VisualStudio.TextManager.Interop;
using Roslyn.Utilities;

namespace Microsoft.VisualStudio.LanguageServices.Implementation.ProjectSystem.CPS
{
    internal sealed partial class CPSProject : AbstractProject
    {
        public CPSProject(
            VisualStudioProjectTracker projectTracker,
            Func<ProjectId, IVsReportExternalErrors> reportExternalErrorCreatorOpt,
            string projectDisplayName,
            string projectFilePath,
            IVsHierarchy hierarchy,
            string language,
            Guid projectGuid,
            string binOutputPath,
            IServiceProvider serviceProvider,
            VisualStudioWorkspaceImpl visualStudioWorkspaceOpt,
            HostDiagnosticUpdateSource hostDiagnosticUpdateSourceOpt,
            ICommandLineParserService commandLineParserServiceOpt)
            : base(projectTracker, reportExternalErrorCreatorOpt, projectDisplayName, projectFilePath,
                   hierarchy, language, projectGuid, serviceProvider, visualStudioWorkspaceOpt, hostDiagnosticUpdateSourceOpt, commandLineParserServiceOpt)
        {
            if (binOutputPath != null)
            {
                // Ensure that binOutputPath is either null or a rooted path.
                // CPS might provide such invalid paths during initialization or when project is in unrestored state.
                if (binOutputPath == String.Empty)
                {
                    binOutputPath = null;
                }
                else if (!PathUtilities.IsAbsolute(binOutputPath))
                {
                    // Make it a rooted path.
                    var basePath = PathUtilities.IsAbsolute(projectFilePath) ? PathUtilities.GetDirectoryName(projectFilePath) : Path.GetTempPath();
                    binOutputPath = PathUtilities.CombineAbsoluteAndRelativePaths(basePath, binOutputPath);
                }
            }

            // We need to ensure that the bin output path for the project has been initialized before we hookup the project with the project tracker.
            SetBinOutputPathAndRelatedData(binOutputPath);

            // Now hook up the project to the project tracker.
            projectTracker.AddProject(this);
        }

        // We might we invoked from a background thread, so schedule the disconnect on foreground task scheduler.
        public sealed override void Disconnect()
        {
            if (IsForeground())
            {
                DisconnectCore();
            }
            else
            {
                InvokeBelowInputPriority(DisconnectCore);
            }
        }

        private void DisconnectCore()
        {
            // clear code model cache and shutdown instances, if any exists.
            _projectCodeModel?.OnProjectClosed();

            base.Disconnect();
        }
    }
}
