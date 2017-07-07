#include <windows.h>
#include <process.h>
#include <tlhelp32.h>
#include <winbase.h>

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "user32.lib")

const char* blacklist[] = {
  "agar.io",
  "blockor.io",
  "bonk.io",
  "diep.io",
  "krew.io",
  "lazerdrive.io",
  "limax.io",
  "mope.io",
  "space1.io",
  "slay.one",
  "slither.io",
  "splix.io",
  "supersnake.io",
  "tanker.io",
  "tankwars.io",
  "tanx.io",
  "vanar.io",
  "vertix.io",
  "wings.io",
  "wormate.io",
  "zlap.io",
  "io-games.io",

  "spotify",
  "youtube",
  "espn.com",
  "super slime soccer",
  "silvergames.com",
};

void pressKey (WORD vk) {
  INPUT in = { 0 };
  in.type = INPUT_KEYBOARD;
  in.ki.wVk = vk;
  SendInput(1, &in, sizeof(INPUT));
}

void releaseKey (WORD vk) {
  INPUT in = { 0 };
  in.type = INPUT_KEYBOARD;
  in.ki.wVk = vk;
  in.ki.dwFlags = KEYEVENTF_KEYUP;
  SendInput(1, &in, sizeof(INPUT));
}

void checkWindow (void) {
  HWND hActive = GetForegroundWindow();
  if (!hActive)
    return;

  int length = GetWindowTextLength(hActive);
  if (length == 0 || length >= 256)
    return;

  char buffer[256] = { 0 };
  GetWindowText(hActive, buffer, sizeof(buffer));
  for (int i = 0; i < length; ++i)
    buffer[i] = tolower(buffer[i]);

  for (int i = 0; i < sizeof(blacklist) / sizeof(*blacklist); ++i) {
    if (strstr(buffer, blacklist[i])) {
      pressKey(VK_CONTROL);
      pressKey('W');
      Sleep(103);
      releaseKey('W');
      releaseKey(VK_CONTROL);
      Sleep(373);
      pressKey(VK_RETURN);
      Sleep(103);
      releaseKey(VK_RETURN);
    }
  }
}

void killProcess (const char* process) {
  DWORD cID = GetCurrentProcessId();
  HANDLE hSnapShot = CreateToolhelp32Snapshot(TH32CS_SNAPALL, 0);
  PROCESSENTRY32 pEntry;
  pEntry.dwSize = sizeof(pEntry);
  BOOL hRes = Process32First(hSnapShot, &pEntry);
  while (hRes) {
    if (pEntry.th32ProcessID != cID && strcmp(pEntry.szExeFile, process) == 0) {
      HANDLE hProcess = OpenProcess(PROCESS_TERMINATE, 0, (DWORD)pEntry.th32ProcessID);
      if (hProcess != 0) {
        TerminateProcess(hProcess, 9);
        CloseHandle(hProcess);
      }
    }
    hRes = Process32Next(hSnapShot, &pEntry);
  }
  CloseHandle(hSnapShot);
}

bool registerStartup (char const* name) {
  char path[MAX_PATH];
  GetModuleFileName(0, path, MAX_PATH);

  HKEY hKey = NULL;
  LONG lResult = 0;
  bool fSuccess = true;
  DWORD dwSize;

  char szValue[MAX_PATH] = { 0 };
  sprintf(szValue, "\"%s\"", path);

  lResult = RegCreateKeyEx(
    HKEY_CURRENT_USER,
    "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
    0, 0, 0, (KEY_WRITE | KEY_READ), 0, &hKey, 0);

  fSuccess = (lResult == 0);

  if (fSuccess) {
    dwSize = strlen(szValue) + 1;
    lResult = RegSetValueEx(hKey, name, 0, REG_SZ, (BYTE*)szValue, dwSize);
    fSuccess = (lResult == 0);
  }

  if (hKey != 0) {
    RegCloseKey(hKey);
    hKey = 0;
  }

  return fSuccess;
}

int CALLBACK WinMain (
  HINSTANCE hInstance,
  HINSTANCE hPrev,
  LPSTR lpCmdLine,
  int nCmdShow)
{
  srand(time(0));
  registerStartup("Coding Circle Updater");
  killProcess("ccupdate.exe");
  for (;;) {
    checkWindow();
    Sleep(10000 + rand() % 20000);
  }
  return 0;
}
