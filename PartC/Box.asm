// Make the Computer Draw a Box
// K = 47
// Width = 64 pixels (4 words)
// Height = 20 rows
// Starting screen address = 17888

(LOOP)
    // Check keyboard
    @KBD
    D=M
    @BLACK
    D;JNE

    // No key pressed: white
    @color
    M=0
    @DRAW
    0;JMP

(BLACK)
    // Key pressed: black
    @color
    M=-1

(DRAW)
    // Starting address = SCREEN + 32*47
    @SCREEN
    D=A
    @1504
    D=D+A
    @addr
    M=D

    // Draw 20 rows
    @20
    D=A
    @rows
    M=D

(ROWLOOP)
    // Draw 4 words in each row
    @4
    D=A
    @cols
    M=D

(COLLOOP)
    @color
    D=M
    @addr
    A=M
    M=D

    // Move to next word
    @addr
    M=M+1

    @cols
    MD=M-1
    @COLLOOP
    D;JGT

    // Move to next screen row
    @addr
    D=M
    @28
    D=D+A
    @addr
    M=D

    @rows
    MD=M-1
    @ROWLOOP
    D;JGT

    // Repeat forever
    @LOOP
    0;JMP
