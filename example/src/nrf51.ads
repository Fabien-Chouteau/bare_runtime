package NRF51 is

   procedure OS_Exit;
   pragma Export (C, OS_Exit, "_exit");

   procedure Putchar (C : Character);
   pragma Export (C, Putchar, "putchar");

end NRF51;
