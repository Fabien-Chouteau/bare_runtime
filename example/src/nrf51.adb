with Interfaces;
with System;

package body NRF51 is

   UART_STARTRX  : Interfaces.Unsigned_32
     with Address => System'To_Address (16#40002000#),
     Volatile_Full_Access;
   UART_STARTTX  : Interfaces.Unsigned_32
     with Address => System'To_Address (16#40002008#),
     Volatile_Full_Access;
   UART_RXDRDY   : Interfaces.Unsigned_32
     with Address => System'To_Address (16#40002108#),
     Volatile_Full_Access;
   UART_TXDRDY   : Interfaces.Unsigned_32
     with Address => System'To_Address (16#4000211c#),
     Volatile_Full_Access;
   UART_ENABLE   : Interfaces.Unsigned_32
     with Address => System'To_Address (16#40002500#),
     Volatile_Full_Access;
   UART_PSELTXD  : Interfaces.Unsigned_32
     with Address => System'To_Address (16#4000250c#),
     Volatile_Full_Access;
   UART_PSELRXD  : Interfaces.Unsigned_32
     with Address => System'To_Address (16#40002514#),
     Volatile_Full_Access;
   UART_RXD      : Interfaces.Unsigned_32
     with Address => System'To_Address (16#40002518#),
     Volatile_Full_Access;
   UART_TXD      : Interfaces.Unsigned_32
     with Address => System'To_Address (16#4000251c#),
     Volatile_Full_Access;
   UART_BAUDRATE : Interfaces.Unsigned_32
     with Address => System'To_Address (16#40002524#),
     Volatile_Full_Access;
   UART_CONFIG   : Interfaces.Unsigned_32
     with Address => System'To_Address (16#4000256c#),
     Volatile_Full_Access;
   UART_INTEN    : Interfaces.Unsigned_32
     with Address => System'To_Address (16#40002300#),
     Volatile_Full_Access;
   UART_INTENSET : Interfaces.Unsigned_32
     with Address => System'To_Address (16#40002304#),
     Volatile_Full_Access;
   UART_INTENCLR : Interfaces.Unsigned_32
     with Address => System'To_Address (16#40002308#),
     Volatile_Full_Access;

   AIRCR : Interfaces.Unsigned_32
     with Address => System'To_Address (16#E000ED0C#),
     Volatile_Full_Access;

   -------------
   -- Putchar --
   -------------

   procedure Putchar (C : Character) is
   begin
      UART_TXDRDY := 0;
      UART_TXD := C'Enum_Rep;
   end Putchar;

   -------------
   -- OS_Exit --
   -------------

   procedure OS_Exit is
   begin
      AIRCR := 16#05FA_0004#;
   end OS_Exit;

begin

   UART_BAUDRATE := 16#00275000#;
   UART_CONFIG := 0;
   UART_PSELTXD := 25;
   UART_PSELRXD := 25;
   UART_ENABLE := 16#04#;
   UART_STARTTX := 1;
   UART_STARTRX := 1;
   UART_RXDRDY := 0;
end NRF51;
