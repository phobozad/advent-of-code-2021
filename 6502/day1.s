PORTB = $6000
PORTA = $6001
DDRB = $6002
DDRA = $6003

; Division variables
value = $0200		; 2 bytes - Value stored in RAM at this address
mod10 = $0202		; 2 bytes - Mod10 (remainder, left-hand side) stored in RAM at this address
ascii_out = $0204	; 6 bytes (16 bit number = 65535 + null terminating character)

; Day1 Part1 variables
last_depth = $0220	; 2 bytes
result_len = $0222	; 1 byte
result = $0223		; Multi-byte array of length `resultlength`
bigindex = $00		; 16-bit index to use with Y register

; Port B Bits
LCD_RS =	%00100000	; LCD Register Select Pin
LCD_RW =	%01000000	; LCD Read/Write Pin
LCD_EN =	%10000000	; LCD Enable Pin
LCD_BUSY =	%10000000	; LCD Busy Pin (D7)

LED_ON =	%00000001	; Status LED


  .org $8000	; Set base address from processor perspective (0x0000 -> 0x8000)

reset:
  ldx #$ff		
  txs			; Set stack pointer to start at 0xFF
 
  lda #%11111111	; Set to output mode
  sta DDRB		; Send mode to I/O B on 6523
  sta DDRA		; Send mode to I/O A on 6522



lcd_init:
  ; Set Function ( Bit mode [DL], Num Lines [N], Char Size[F] )
  lda #%00111000	; Function Set, use 8-bit mode (DL = 1)
  jsr lcd_instruction
  
  ;lda #%11001100	; Function Set, Two Lines (N = 1), 5x8 Chars (F = 1)
  ;sta PORTB
  ;jsr wait_for_lcd	; Wait for write


  ; Display Control Set: Display On (D = 1 ), Cursor On (C = 1 ), Blink Cursor On (B = 1 )
  lda #%00001111	; D,C,B = 1
  jsr lcd_instruction
  

  ; Entry mode set: Increment (I/D = 1), Display shift off (S = 0)
  lda #%00000110
  jsr lcd_instruction


  ; Clear display
  lda #%00000001
  jsr lcd_instruction
  


day1:
  ldy #<data		; Load low byte of data location
  sty bigindex		
  ldy #>data		; Load high byte of data location
  sty bigindex + 1

  ldy #0		; Y register for looping
  sty result
  sty result + 1	; Initialize 16-bit result variable to zero
day1p1_loop:
;  lda #"."
;  jsr print_char

;  lda (bigindex),y	; Load datapoint
  lda data,y		; Load datapoint
  cmp last_depth	; Compare to last datapoint
  beq next		; If data[x] = last_depth, ignore
  bcs increment		; If carry bit set, data[x] >= last_depth (but not equal b/c we already checked for that
  jmp next		; If data[x] < last_depth, we will ignore this
increment:
  cpy #0		; If this is the first iteration,
  beq next		; then don't count it
  ; Increment our depth counter
  ; 16-bit addition
  clc
  pha			; Push A onto stack so we can restore it later
  lda #1		; We will increment counter by 1
  adc result		; Add low bits
  sta result		; Store low bits result back to memory
  lda #0		; Only incrementing by 1 so high-bits are zero
  adc result + 1	; Add high bits
  sta result + 1	; Store high bits result to memory
  pla			; Pull A off the stack to restore it
  ; end 16-bit addition

next:
  iny			; Increment our index
;  bne notoverflow
;  inc bigindex		; if Y overflows, increment high byte of bigindex by 1 to get the next 256 values
  
notoverflow:
  sta last_depth	; Save our last datapoint for the next loop 
  
  ; 16-bit.... if data location + datalength == value at bigcounter + y, then we are done

  ; 
;  lda bigindex
;  cmp #<data_end	; Compare high bytes
;  bne day1p1_loop	; If the values are not the same jump back to start of loop

;  tya			; Put Y value into accumulator
;  clc
;  adc bigindex + 1	; Add Y value (in accumulator) to the address stored in low bye of bigindex
;  cmp #>data_end	; Compare low bytes
;  bne day1p1_loop	; If the values are not the same jump back to start of loop

  cpy datalength	; Compare counter to length of our data array
  bne day1p1_loop	; and repeat the loop if result is not equal (i.e. we're not at the end of the data yet)
  
  ; End of Loop

  lda #2
  sta result_len	; Set result length to 2 (single 16-bit number/element)
  jsr print_array	; Print our resulting depth counter

  jmp end		; Terminate program

compare_16:
  ; Compare two 16-bit values





print_array:
; Prints out a list of values stored in `result` with length `resultlength`
  ldx #0		; Use X register for looping through the list
print_array_loop:
  ; Load number we want to divide into RAM (2 bytes)
  lda result,x
  sta value
  lda result + 1,x
  sta value + 1

  ; Initialize ASCII output
  lda #0
  sta ascii_out		; Set first byte of string to zero (null-terminated)
  
  jsr divide		; Do our "division" to convert to ASCII & print out
  
  lda #" "		; Print a space between output numbers
  jsr print_char

  inx			; Increment counter
  inx			; Twice b/c 16-bit values

  cpx result_len	; Compare counter to length of our data array
  bne print_array_loop	; and repeat the loop if result is not equal (i.e. we're not at the end of the data yet)
  
  rts

end:
  ; Infinite loop to stop the program
  jmp end


  ; Need to divide by 10 repeatedly to get decimal digits
  ;
  ; rotate left
  ; set carry bit
  ; subtract 10
  ; if carry bit = 0, 10 didn't divide into the number so ignore and repeat
  ; if carry bit still = 1, 10 did divide into the number
  ;   take the result of that subtraction and use that as the left-hand side of the rotating bits
  ;   then repeat

  ; repeat the rotate left 16 times (16 bits)
  ; at the end of 16 rotations, the left-hand side of the bits is the remainder (the first digit)
  ; with one more rotation (17 total), 
  ;   the right-hand side of the bits is the result of the division which becomes the input for the next
  ;   round of division for the next digits.  clear the remainder bits (left-hand side) and start again
divide:
  ; Push A, X and Y registers onto the stack so other subroutines can call this
  ; and we will clean up and restore state when done dividing
  pha
  txa
  pha
  tya
  pha
divide_number:
  ; Initialize remainder to all zeros
  lda #0
  sta mod10
  sta mod10 + 1
  clc			; Clear carry bit before starting
  
  ; We need to loop 16 times. Track this using x register
  ldx #16
divide_loop:
  ; Rotate quotient and remainder
  rol value
  rol value + 1
  rol mod10
  rol mod10 + 1

  sec			; Set carry bit
  lda mod10		; Load low byte into A register
  sbc #10		; Subtract by 10 with carry
  tay			; Save low byte of subtraction result into Y register
  lda mod10 + 1		; Load high byte into A register
  sbc #0		; Subtract zero (our divisor of 10 fits into the first 8 bits, rest of bits are 0)
  
  ; a & y register now have the contents of the dividend and divisor

  ; If carry bit is clear, then ignore the result (it didn't divide into the number)
  bcc ignore_result

  ; Otherwise we got an answer - it divided
  ; Take the result we got and put them into the mod10 bits (left-hand side)
  sty mod10
  sta mod10 + 1

ignore_result:
  dex			; Decrement our loop counter
  bne divide_loop	; Loop if our loop counter isn't zero
  ; After 16 iterations, save our remainder (lower half of mod10 variable) and repeat
  ; Do one last rotation to get our answer from the division into the value variable
  ; Need to do this before we clear carry bit for ASCII conversion
  rol value
  rol value + 1
  ; Now we can do the ASCII conversion next while our mod10 values are still correct

  lda mod10		; Load remainder
  ; Convert the remainder from number to an ASCII character code
  clc
  adc #"0"		; Add ASCII 0 to convert the number
  jsr push_char

  ; Repeat the division process if we aren't done yet
  ; We're done when the result of our division process is zero
  ; if value != 1
  lda value
  ; Bitwise or the two value bytes.  If any bits are set then the result will be non-zero
  ora value + 1
  bne divide_number	; Branch to divide (repeat) if the OR result is not zero

  ; Otherwise we are done

  ; Print out the message
  ldx #0		; Initialize X for looping
  ldy #0		; Initialize Y for looping
labelprint:
  lda data_label,y
  beq print
  jsr print_char
  iny
  jmp labelprint
print:
  lda ascii_out,x
  beq end_divide	; If we get 0 (null termination) we are done reading the string
  jsr print_char
  inx
  jmp print
end_divide:
  ; Pull original A, X, and Y registers back off the stack and restore them before returning
  pla
  tay
  pla
  tax
  pla
  
  rts





  


lcd_instruction:
  jsr lcd_wait
  sta PORTB
  lda #00			; Clear RS/RW/E bits
  sta PORTA
  lda #(LED_ON | LCD_EN)	; Toggle E bit
  sta PORTA
  lda #00			; Clear RS/RW/E bits
  sta PORTA
  rts

push_char:
  ; Push character into ASCII variable
  ; Character will be in A register.  Add this to the beginning of the
  ; null-terminated string (ascii_out)
  pha			; Push the character we're going to write into the string variable onto the stack
  ldy #0		; Use Y as the index position for the string

char_loop:  
  lda ascii_out,y	; Get character in the string and
  tax			; put into the X register for safe keeping

  pla			; Pull new character we're writing back off the stack and
  sta ascii_out,y	; store this into the string variable in place of the character we moved into X

  iny			; move to the next character of the string
  txa
  pha			; Push character from the sting onto the stack
  bne char_loop		; If A not zero, we are not the end of the string (null-terminator) so repeat

  ; Otherwise we are at the end of the string
  pla			; We still have the null terminator stored on the stack so pull it off
  sta ascii_out,y	; and write it into the end of the string variable

  rts



print_char:
  jsr lcd_wait
  sta PORTB
  lda #LCD_RS		; Set RS bit
  sta PORTA
  lda #(LED_ON | LCD_RS | LCD_EN) ; Set RS and E bit
  sta PORTA
  lda #LCD_RS		; Clear RW/E bit
  sta PORTA
  rts



lcd_wait:
  pha
  lda #%01111111	; Setup LCD Busy pin to input mode
  sta DDRB		; Send I/O config to B
lcd_wait_loop:
  lda #LCD_RW		; RW = 1
  sta PORTA
  lda #(LED_ON | LCD_RW | LCD_EN) ; RS = 0, RW = 1 to read Busy flag; set busy lap (bit 8), E=1
  sta PORTA

  lda PORTB		; Read port B to get Busy Flag
  and #LCD_BUSY		; Compare LCD_Busy flag with A register
  bne lcd_wait_loop	; If (A & LCD_BUSY) != 0, loop until it isn't busy 

  lda #LCD_RW
  sta PORTA
  lda #%11111111	; Setup all pins back to output mode
  sta DDRB		; Send I/O config to B
  pla
  rts			; Return once LCD_BUSY is no longer set


;datalength: .byte 10*2
;data: .word 199,200,208,210,200,207,240,269,260,263
datalength: .byte 10
data: .byte 199,200,208,210,200,207,240,250,245,253
data_label: .asciiz "D1,P1: "
data_end: .word data + 10

  .org $fffc	; Reset vector - start program at 0x8000 (based on reset label)
  .word reset
  .word $0000	; Padding to hit exactly 32k ROM filesize
