.MODEL SMALL

; Stack
Sseg SEGMENT STACK 'stack'
    DB 256 DUP(?)
Sseg ENDS

; Data
Dseg SEGMENT 'data'
    Arr  DB 10, 15, 22, 33, 44, 51, 60, 77, 88, 99  
    N    DW 10     ; elt-s                                 
    Result DB ?                                      
Dseg ENDS

; Code
Cseg SEGMENT 'code'
    ASSUME CS:Cseg, DS:Dseg, SS:Sseg ; inform assembler what is what

; SubProgramm
; Input = BP+4 = address of array, BP+6 = hm elements
; Output = AL, %2 el-ts 
SumEven PROC NEAR
    PUSH BP
    MOV BP, SP     ; SP - ukazatel stack, BP-base pointer

    PUSH SI        ; save SI, CX, DX
    PUSH CX        
    PUSH DX        

    MOV SI, [BP+4] ; SI = address of array
    MOV CX, [BP+6] ; CX = hm el-ts
    XOR AX, AX     ; AX = 0 (start sum)

next_elem:
    MOV DL, [SI]   ; next el-t to DL
    TEST DL, 1     ; logic DL AND 1=== DL[SI] are %2?
    JNZ skip_add   ; jump if Not Zero = skip this 
    ADD AL, DL     ; this %2! summ this!

skip_add:
    INC SI         ; SI++ t onext elt
    LOOP next_elem

    ; result to AL

    POP DX
    POP CX
    POP SI
    POP BP
    RET
SumEven ENDP

; Main Program
Main PROC FAR
    PUSH DS
    MOV AX, 0
    PUSH AX

    MOV AX, Dseg
    MOV DS, AX

    ; Prepare parametrs: lengh, address
    PUSH N          ; hm elt-s (word)
    PUSH OFFSET Arr ; address start of array

    CALL SumEven    ; SubProgram

    ; save result
    MOV Result, AL

    ; exit to DOS
    RET
Main ENDP

Cseg ENDS

END Main