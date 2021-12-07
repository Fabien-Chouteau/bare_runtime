# bare_runtime
Minimal Ada/SPARK run-time for embedded or other restricted targets

## Usage

First edit you `alire.toml` file and add the following elements:
 - Add `bare_runtime` in the dependency list:
   ```toml
   [[depends-on]]
   bare_runtime = "*"
   ```
 - Set the architecture build switches, we use ARM Cortex-M4F as an example here:
   ```toml
   [gpr-set-externals]
   BARE_RUNTIME_SWITCHES = "-mlittle-endian -mthumb -mfloat-abi=hard -mcpu=cortex-m4 -mfpu=fpv4-sp-d16"
   ```

Then edit your project file to add the following elements:
 - "with" the run-time project file. With this, gprbuild will compile the run-time before your application
   ```ada
   with "bare_runtime.gpr";
   ```
 - Specify the `Target` and `Runtime` attributes:
   ```ada
      for Target use "arm-eabi";
      for Runtime ("Ada") use Bare_Runtime'Runtime ("Ada");
   ```
