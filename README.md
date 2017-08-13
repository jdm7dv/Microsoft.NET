In 2010 I thought up an idea to create a sandboxed or contained computing environment within <a rel="nofollow" href="http://research.microsoft.com/en-us/projects/singularity/">Microsoft Research's Singularity RDK</a>. I have been working on it off and on. I am putting all of my C# and F# projects in this environment and even have a C# Window Manager and File Manager. More on this project later.  

# Research Environment

jdm7dv's research environment is a computional envirnoment, member of the Microsoft Research Group on Gitlab. It is licensed
under the [GNU AFFERO GENERAL PUBLIC LICENSE](LICENSE.txt).

The Resrearch Environment can be built using [Visual Studio][1], or [MSBuild][2]. 

See the [release notes](RELEASE_NOTES) for notes on various stable releases of jdm7dv's Research Environment.

[1]: #building-research-environment-on-windows-using-visual-studio-command-prompt


## Building Research Envirnoment on Windows using Visual Studio Command Prompt

64-bit builds, start with:

```bash
configure.cmd
```
Click on the conmand-line symbolic link or shortcut on the Windows 10 desktop.
Place the System32 directory on your PATH. And you might have to disable you virus
protection to get the assembley language to build.

then:

```bash
cd Distro
msb World.proj
```

![alt text](https://gitlab.com/jdm7dv/research-environment/art/build.gif "Verve Build")
