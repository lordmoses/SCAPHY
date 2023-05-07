# Scripts

Assumes that ScadaBR has been run and captured API calls with Process Monitor.

## Run Attack Experiment

1. Clone the ScadaBR repository. (https://github.com/ScadaBR/ScadaBR)
2. Install Eclipse (version 2019-09) and JDK 8 to compile the ScadaBR project.
3. Modify the file `https://github.com/ScadaBR/ScadaBR/blob/master/src/com/serotonin/mango/rt/dataSource/modbus/ModbusDataSource.java`, and compile it with Eclipse. It will output a file `ModbusDataSource.class`. The attack source code can be found in `Attack_Scripts/ModbusDataSource.java`.
4. Replace the compiled `ModbusDataSource.class` with the current installed ScadaBR file `C:\Program Files\ScadaBR\tomcat\webapps\ScadaBR\WEB-INF\classes\com\serotonin\mango\rt\dataSource\modbus\ModbusDataSource.class`.
5. Put the attack config `Attack_Scripts/AttackConfig.txt` into `C:\Program Files\ScadaBR\tomcat\conf\AttackConfig.txt`. `ModbusDataSource.class` will read this config file to perform attacks.
6. Restart ScadaBR, the attack log will be created in `C:\Program Files\ScadaBR\tomcat\logs\AttackLog.txt`.