PROGRAM main
  VAR
    I_levelSensor AT %IW100.1 : UINT;
    I_flowMeter AT %IW101.1 : UINT;
    I_setpointDial AT %IW103.1 : UINT;
    O_intakePump AT %QW100 : UINT;
    O_outputPump AT %QW101 : UINT;
  END_VAR
  VAR
    PID0 : PID;
  END_VAR
  VAR
    kp AT %MD0 : REAL := 2.0;
    ki AT %MD1 : REAL := 0.5;
    kd AT %MD2 : REAL := 0.0;
    x_0 AT %MD3 : REAL := 0.0;
    scale AT %MD4 : REAL := 100.0;
  END_VAR
  VAR
    _TMP_UINT_TO_REAL18_OUT : REAL;
    _TMP_DIV10_OUT : REAL;
    _TMP_UINT_TO_REAL19_OUT : REAL;
    _TMP_DIV11_OUT : REAL;
    _TMP_MUL15_OUT : REAL;
    _TMP_REAL_TO_UINT14_OUT : UINT;
  END_VAR

  _TMP_UINT_TO_REAL18_OUT := UINT_TO_REAL(I_levelSensor);
  _TMP_DIV10_OUT := DIV(_TMP_UINT_TO_REAL18_OUT, scale);
  _TMP_UINT_TO_REAL19_OUT := UINT_TO_REAL(I_setpointDial);
  _TMP_DIV11_OUT := DIV(_TMP_UINT_TO_REAL19_OUT, scale);
  PID0(AUTO := TRUE, PV := _TMP_DIV10_OUT, SP := _TMP_DIV11_OUT, X0 := x_0, KP := kp, TR := ki, TD := kd, CYCLE := T#50ms);
  _TMP_MUL15_OUT := MUL(PID0.XOUT, scale);
  _TMP_REAL_TO_UINT14_OUT := REAL_TO_UINT(_TMP_MUL15_OUT);
  O_intakePump := _TMP_REAL_TO_UINT14_OUT;
  O_outputPump := _TMP_REAL_TO_UINT14_OUT;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : main;
  END_RESOURCE
END_CONFIGURATION
