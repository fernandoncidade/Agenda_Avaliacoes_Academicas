; Script adaptado para compatibilidade com Nuitka

#define MyAppName "AGENDA AVALIAÇÕES ACADÊMICAS"
#define MyAppVersion "2026.4.24.0"
#define MyAppPublisher "Fernando Nillsson Cidade"
#define MyAppURL "https://github.com/fernandoncidade"
#define MyAppExeName "Agenda_Avaliacoes_Academicas.exe"
#define NuitkaDistDir "D:\MISCELANEAS\VSCode\Nuitka\Agenda_Avaliacoes_Academicas\main.dist"

[Setup]
AppId={{9D405710-02D6-4742-8474-6F07101764F7}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
UninstallDisplayName={#MyAppName}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
InfoBeforeFile={#NuitkaDistDir}\assets\ABOUT\ABOUT_en_US.txt
LicenseFile={#NuitkaDistDir}\assets\PRIVACY_POLICY\Privacy_Policy_en_US.txt
OutputDir=D:\MISCELANEAS\VSCode\Nuitka\Agenda_Avaliacoes_Academicas
OutputBaseFilename=Agenda_Avaliacoes_Academicas_v2026.4.24.0
SetupIconFile={#NuitkaDistDir}\assets\icones\ReviewsManager.ico
SolidCompression=yes
WizardStyle=modern
ShowLanguageDialog=yes
AllowNoIcons=yes
DisableReadyPage=yes
DisableFinishedPage=no

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"; InfoBeforeFile: "{#NuitkaDistDir}\assets\ABOUT\About_pt_BR.txt"; LicenseFile: "{#NuitkaDistDir}\assets\PRIVACY_POLICY\Privacy_Policy_pt_BR.txt"
Name: "english"; MessagesFile: "compiler:Default.isl"; InfoBeforeFile: "{#NuitkaDistDir}\assets\ABOUT\About_en_US.txt"; LicenseFile: "{#NuitkaDistDir}\assets\PRIVACY_POLICY\Privacy_Policy_en_US.txt"

[CustomMessages]
brazilianportuguese.AppLanguage=Idioma do aplicativo
brazilianportuguese.SelectAppLang=Selecione o idioma padrão do aplicativo
brazilianportuguese.Portuguese=Português
brazilianportuguese.English=Inglês

english.AppLanguage=Application language
english.SelectAppLang=Select the default application language
english.Portuguese=Portuguese
english.English=English

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "langpt_BR"; Description: "{cm:Portuguese}"; GroupDescription: "{cm:AppLanguage}"; Flags: exclusive
Name: "langen_US"; Description: "{cm:English}"; GroupDescription: "{cm:AppLanguage}"; Flags: exclusive unchecked

[Files]
Source: "{#NuitkaDistDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; WorkingDir: "{app}"

[Run]
Filename: "{sys}\icacls.exe"; Parameters: """{app}"" /grant *S-1-5-32-545:(OI)(CI)F"; Flags: runhidden; Description: "Configurando permissões..."
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent; WorkingDir: "{app}"

[ReturnCodes]
6000=UserCancelled
6001=AppAlreadyExists
6002=AnotherInstallationRunning
6003=DiskSpaceFull
6004=RebootRequired
6005=NetworkFailure_DownloadError
6006=NetworkFailure_ConnectionLost
6007=PackageRejectedByPolicy
0=Success

[Code]
procedure CreateLanguageConfigJSON();
var
  FileName: string;
  LanguageCode: string;
  JSONContent: string;
  ConfigDir: string;
begin
  ConfigDir := ExpandConstant('{userappdata}\AgendaAvaliacoesAcademicas');
  FileName := ConfigDir + '\language.json';

  if not DirExists(ConfigDir) then
    ForceDirectories(ConfigDir);

  if (WizardSilent) then
    LanguageCode := 'en_US'
  else if WizardIsTaskSelected('langpt_BR') then
    LanguageCode := 'pt_BR'
  else if WizardIsTaskSelected('langen_US') then
    LanguageCode := 'en_US'
  else
    LanguageCode := 'pt_BR';

  JSONContent := '{' + #13#10;
  JSONContent := JSONContent + '  "idioma": "' + LanguageCode + '"' + #13#10;
  JSONContent := JSONContent + '}';

  SaveStringToFile(FileName, JSONContent, False);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    CreateLanguageConfigJSON();
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  AppPath: string;
  LocalAppDataPath: string;
begin
  if CurUninstallStep = usUninstall then
  begin
    LocalAppDataPath := ExpandConstant('{localappdata}\AgendaAvaliacoesAcademicas');
    if DirExists(LocalAppDataPath) then
    begin
      Log('Removendo o diretório de dados do aplicativo: ' + LocalAppDataPath);
      DelTree(LocalAppDataPath, True, True, True);
    end;

    AppPath := ExpandConstant('{app}');
    if DirExists(AppPath + '\_internal\logs') then
      DelTree(AppPath + '\_internal\logs', True, True, True);

    if DirExists(AppPath + '\_internal') then
      DelTree(AppPath + '\_internal', True, True, True);
  end;
end;

