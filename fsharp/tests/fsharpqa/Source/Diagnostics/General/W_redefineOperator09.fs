// #Regression #Diagnostics 
// Regression test for FSHARP1.0:3292
// Give a warning when the user attempts to redefine "=", "<", ">", ">=", "<=" or "<>" or define static members with these names
//<Expects id="FS0086" span="(8,6-8,8)" status="warning">The 'or' operator should not normally be redefined\. Consider using a different operator name</Expects>
//<Expects id="FS0086" span="(9,8-9,10)" status="warning">The 'or' operator should not normally be redefined\. Consider using a different operator name</Expects>
//<Expects id="FS0086" span="(11,20-11,22)" status="warning">The name '\(or\)' should not be used as a member name\. If defining a static member for use from other CLI languages then use the name 'or' instead\.$</Expects>
module M
let (or) x y = x + y
let f (or)  = 1 < 2
type C() =
    static member (or) (x:C,y:C) = true


