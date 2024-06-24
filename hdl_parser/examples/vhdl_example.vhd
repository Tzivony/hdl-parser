library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;


package example is
  component demo is
    generic (
      GENERIC1: boolean := false;
      GENERIC2: integer := 100
    );
    port (
      a, b : in std_logic := '1';
      c, d : out std_logic_vector(7 downto 0);
      e, f : inout unsigned(7 downto 0)
    );
  end component;
end package;