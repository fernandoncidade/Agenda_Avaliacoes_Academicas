from utils.ApplicationPathUtils import load_text_file
from utils.LogManager import LogManager
logger = LogManager.get_logger()

try:
    SITE_LICENSES = """
    https://www.gnu.org/licenses/lgpl-3.0.html.en
    https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.en
    https://opensource.org/licenses/BSD-2-Clause
    https://opensource.org/licenses/BSD-3-Clause
    https://www.apache.org/licenses/LICENSE-2.0
    https://python-pillow.org/
    https://opensource.org/licenses/MIT
    https://opensource.org/license/isc-license-txt
    """
    
    LICENSE_TEXT_PT_BR = load_text_file("EULA_pt_BR - Compression Manager.txt", folder="EULA")
    LICENSE_TEXT_EN_US = load_text_file("EULA_en_US - Compression Manager.txt", folder="EULA")

    NOTICE_TEXT_PT_BR = load_text_file("NOTICE_pt_BR.txt", folder="NOTICES")
    NOTICE_TEXT_EN_US = load_text_file("NOTICE_en_US.txt", folder="NOTICES")

    ABOUT_TEXT_PT_BR = load_text_file("ABOUT_pt_BR.txt", folder="ABOUT")
    ABOUT_TEXT_EN_US = load_text_file("ABOUT_en_US.txt", folder="ABOUT")

    Privacy_Policy_pt_BR = load_text_file("Privacy_Policy_pt_BR.txt", folder="PRIVACY_POLICY")
    Privacy_Policy_en_US = load_text_file("Privacy_Policy_en_US.txt", folder="PRIVACY_POLICY")

    History_APP_pt_BR = load_text_file("History_APP_pt_BR.txt", folder="ABOUT")
    History_APP_en_US = load_text_file("History_APP_en_US.txt", folder="ABOUT")

    RELEASE_NOTES_pt_BR = load_text_file("RELEASE NOTES_pt_BR.txt", folder="RELEASE")
    RELEASE_NOTES_en_US = load_text_file("RELEASE NOTES_en_US.txt", folder="RELEASE")

except Exception as e:
    logger.error(f"Erro ao carregar arquivos de licença: {e}", exc_info=True)
