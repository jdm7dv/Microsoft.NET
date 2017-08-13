// #Conformance #DeclarationElements #MemberDefinitions #MethodsAndProperties 
#light

// Verify property with both getter and setter

type Vector3 = 
    | Vector3 of float * float * float
    member this.Decompose() = match this with Vector3(x, y, z) -> x, y, z

type Vector =
    { mutable Vector3 : Vector3 }
    member this.Length with get () = 
                                let x,y,z = this.Vector3.Decompose()
                                sqrt <| x * x + y * y + z * z
                       and set newLen =
                                this.Vector3 <- Vector3(newLen, newLen, newLen)


let test = { Vector3 = Vector3(0.0, 0.0, 5.0) }

if test.Length <> 5.0 then exit 1

test.Length <- 2.2

let x, y, z = test.Vector3.Decompose()
if x <> y || y <> z || z <> 2.2 then exit 1

exit 0

