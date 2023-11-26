using System;
using System.Runtime.InteropServices;
using FlareOn;

public class Program
{
    // Import user32.dll (containing the function we need) and define
    // the method corresponding to the native function.
    //[DllImport("FlareOn.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    //private static extern namespace FlareOn;
    
    public static void Main(string[] args)
    {
        // Invoke the function as a regular managed method.
        Flag f = new Flag();
        string s = f.GetFlag("MyV0ic3!");
        Console.WriteLine(s);
    }
}