from pathlib import Path

def get_root_path() -> Path:
    """設定ファイル、ログ、入出力ファイルのデフォルト配置先の、  
    ルートディレクトリを取得。  

    * code reference by stackoverflow  
    https://stackoverflow.com/a/53465812 

    Returns:
        Path: デフォルトルートディレクトリ
    """
    return Path(__file__).parent.parent

    