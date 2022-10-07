// Hint_modified.java: a modified version of decompiled bytecode
// CSC 442-001: Thoth. Challenge 02: Reverse Engineering.

// Thoth's only alteration to Jad's output is the addition of
// a main function on lines 50-53.

// Decompiled by Jad v1.5.8e. Copyright 2001 Pavel Kouznetsov.
// Jad home page: http://www.geocities.com/kpdus/jad.html
// Decompiler options: packimports(3)
// Source File Name:   Hint.java

import java.io.PrintStream;

class Hint
{

    public Hint()
    {
        length = 5;
    }

    public int getLength()
    {
        return length;
    }

    public void setLength(int i)
    {
        if(i > 0)
            length = i;
    }

    private void superprivatefunction()
    {
        String s = "68696e743a20596f752061726520736f20636c6f73652e20596f752073686f756c6420686176652072656365697665642061207368613235362068617368206f66207468652066696e616c2070617373776f726420796f75276c6c206e65656420746f206f70656e20746865207064662e205468652061637475616c2070617373776f7264206973206f6e65206f662074686520746f702031302c3030302070617373776f72647320757365642e2054686572652073686f756c64206265206d756c7469706c652070617373776f72642066696c657320796f752063616e2066696e64206f6e6c696e6520666f7220636f6d70617269736f6e2e20596f75206d69676874206861766520746f2068617368207468656d20616c6c20746f2066696e642074686520636f7272656374206f6e652e";
        StringBuilder stringbuilder = new StringBuilder("");
        int i = length * 2;
        int j = i >= s.length() ? s.length() : i;
        for(int k = 0; k < j; k += 2)
        {
            String s1 = s.substring(k, k + 2);
            stringbuilder.append((char)Integer.parseInt(s1, 16));
        }

        System.out.println(stringbuilder);
    }

    private int length;

    public static void main(String[] argss) {
        Hint i = new Hint();
        i.setLength(634-21);
        i.superprivatefunction();
    }
}
