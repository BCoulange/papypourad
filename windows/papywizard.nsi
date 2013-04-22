; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "Papywizard"
!define PRODUCT_VERSION "2.1.21"
!define PRODUCT_WEB_SITE "http://trac.gbiloba.org/papywizard"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\Papywizard.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Language Selection Dialog Settings
!define MUI_LANGDLL_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_LANGDLL_REGISTRY_KEY  "${PRODUCT_UNINST_KEY}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "NSIS:Language"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE $(license)
; Components page
!insertmacro MUI_PAGE_COMPONENTS
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
;!define MUI_FINISHPAGE_RUN "$INSTDIR\Papywizard.exe"
;!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!define MUI_LANGDLL_ALLLANGUAGES
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "French"
!insertmacro MUI_LANGUAGE "German"
!insertmacro MUI_LANGUAGE "Italian"
!insertmacro MUI_LANGUAGE "Spanish"
!insertmacro MUI_LANGUAGE "Polish"
!insertmacro MUI_LANGUAGE "Czech"
;
LicenseLangString license ${LANG_ENGLISH} "..\licence_CeCILL_V2-en.txt"
LicenseLangString license ${LANG_FRENCH} "..\licence_CeCILL_V2-fr.txt"
LicenseLangString license ${LANG_GERMAN} "..\licence_CeCILL_V2-en.txt"
LicenseLangString license ${LANG_ITALIAN} "..\licence_CeCILL_V2-en.txt"
LicenseLangString license ${LANG_SPANISH} "..\licence_CeCILL_V2-en.txt"
LicenseLangString license ${LANG_POLISH} "..\licence_CeCILL_V2-en.txt"
LicenseLangString license ${LANG_CZECH} "..\licence_CeCILL_V2-en.txt"
;
LangString un_message_1 ${LANG_ENGLISH} "Do you really want to uninstall $(^Name)?"
LangString un_message_1 ${LANG_FRENCH} "�tes-vous certain de vouloir d�sinstaller $(^Name)?"
LangString un_message_1 ${LANG_GERMAN} "Do you really want to uninstall $(^Name)?"
LangString un_message_1 ${LANG_ITALIAN} "Do you really want to uninstall $(^Name)?"
LangString un_message_1 ${LANG_SPANISH} "Do you really want to uninstall $(^Name)?"
LangString un_message_1 ${LANG_POLISH} "Do you really want to uninstall $(^Name)?"
LangString un_message_1 ${LANG_CZECH} "Do you really want to uninstall $(^Name)?"
;
LangString un_message_2 ${LANG_ENGLISH} "$(^Name) has been successfully removed from your computer."
LangString un_message_2 ${LANG_FRENCH} "$(^Name) a �t� supprim� avec succ�s de votre ordinateur."
LangString un_message_2 ${LANG_GERMAN} "$(^Name) has been successfully removed from your computer."
LangString un_message_2 ${LANG_ITALIAN} "$(^Name) has been successfully removed from your computer."
LangString un_message_2 ${LANG_SPANISH} "$(^Name) has been successfully removed from your computer."
LangString un_message_2 ${LANG_POLISH} "$(^Name) has been successfully removed from your computer."
LangString un_message_2 ${LANG_CZECH} "$(^Name) has been successfully removed from your computer."

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "Papywizard_${PRODUCT_VERSION}_Install.exe"
InstallDir "$PROGRAMFILES\Papywizard"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Function .onInit
  !insertmacro MUI_LANGDLL_DISPLAY
FunctionEnd

Section "Papywizard" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  File "dist\w9xpopen.exe"
  CreateDirectory "$SMPROGRAMS\Papywizard"
  CreateShortCut  "$SMPROGRAMS\Papywizard\Papywizard.lnk" "$INSTDIR\Papywizard.exe" "$INSTDIR\papywizard.ico"
  CreateShortCut  "$DESKTOP\Papywizard.lnk" "$INSTDIR\Papywizard.exe" "$INSTDIR\papywizard.ico"
; File "dist\python25.dll" ; already included in library.zip
  File "dist\Papywizard.exe"
  File "dist\msvcr71.dll"
  File "dist\library.zip"
  File "papywizard.ico"
  ;
  ; Package
  SetOutPath "$INSTDIR\papywizard"
  SetOutPath "$INSTDIR\papywizard\common"
  File "..\papywizard\common\papywizard.conf"
  File "..\papywizard\common\presets.xml"
  SetOutPath "$INSTDIR\papywizard\view\ui"
  File "..\papywizard\view\ui\*.ui"
SectionEnd

Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\Papywizard\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\Papywizard\Uninstall.lnk" "$INSTDIR\Uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\Uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\Papywizard.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\Uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\Papywizard.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
SectionEnd

; Section descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC01} "Papywizard software"
!insertmacro MUI_FUNCTION_DESCRIPTION_END

Function un.onInit
!insertmacro MUI_UNGETLANGUAGE
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 $(un_message_1) IDYES +2
  Abort
FunctionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK $(un_message_2)
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\Uninst.exe"
  Delete "$INSTDIR\library.zip"
  Delete "$INSTDIR\msvcr71.dll"
  Delete "$INSTDIR\Papywizard.exe"
  Delete "$INSTDIR\w9xpopen.exe"
  Delete "$INSTDIR\*.log"
  Delete "$INSTDIR\papywizard.ico"
  Delete "$SMPROGRAMS\Papywizard\Uninstall.lnk"
  Delete "$SMPROGRAMS\Papywizard\Website.lnk"
  Delete "$SMPROGRAMS\Papywizard\Papywizard.lnk"
  RMDir  "$SMPROGRAMS\Papywizard"
  Delete "$DESKTOP\Papywizard.lnk"

  ; Sources
  Delete "$INSTDIR\papywizard\common\*.*"
  Delete "$INSTDIR\papywizard\view\ui\*.*"
  Delete "$INSTDIR\papywizard\view\*.*"
  RMDir  "$INSTDIR\papywizard\common"
  RMDir  "$INSTDIR\papywizard\view\ui"
  RMDir  "$INSTDIR\papywizard\view"
  RMDir  "$INSTDIR\papywizard"
  RMDir  "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd