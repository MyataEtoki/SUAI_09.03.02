.MODEL SMALL
.STACK 256

.DATA
    Mas DB 15, -30, 7, 0, -5, 12, -1, 8, -100, 44

.CODE
MAIN PROC FAR             

    PUSH DS    
    PUSH AX

    MOV AX, @DATA
    MOV DS, AX

    MOV CX, 10             ;hm loops
    LEA SI, Mas            ;load effective address
                              
LOOP_START:
    MOV AL, [SI]

    CMP AL, 0              ;compare
    JE NEXT                ;jump if equal

    JS NEGATIVE            ;jump if sign (s=1)

    OR DL, AL
    JMP NEXT               ;jump to NEXT

NEGATIVE:
    OR DH, AL              ; DH or(logic +) AL

NEXT:
    INC SI                 ;to next element of Mas (SI++)
    LOOP LOOP_START         


    MOV AX, 0
    MOV AL, DL       
    MOV BX, 0
    MOV BL, DH    

    RET                    ;back to DOS
MAIN ENDP

END MAIN