.MODEL SMALL

Sseg SEGMENT STACK
    DB 256 DUP (?)
Sseg ENDS

Dseg SEGMENT
    X1 DW -17
    X2 DD 73593
    X3 DD -77922
    X4 DW 4329
Dseg ENDS

Cseg SEGMENT
    ASSUME CS:Cseg, DS:Dseg, SS:Sseg

Main PROC FAR
    PUSH DS
    XOR AX, AX
    PUSH AX
    
    MOV AX, Dseg
    MOV DS, AX
    
    ;X3+X2
    MOV AX, X3
    ADD AX, X2
                    
     ;X1/X3               
    MOV AX, X1
    CWD
    IDIV X3
      
     ;X2xorX1 
    MOV AX, X2
    XOR AX, X1
     
     ;X3-X1-CF
    MOV AX, X3
    SBB AX, X1
     
     ;X4*2^4
    MOV AX, X4
    MOV CL, 4
    SHL AX, CL

    RET
Main ENDP

Cseg ENDS
END Main