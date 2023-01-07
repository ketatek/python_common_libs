#-----------------------------------------
# バッチアプリの設定 の アクセッサなどを実装
# Python 3.11 でtoml パーサーが提供されるようになったため、
# tomlを前提とすることにした。
#-----------------------------------------
import tomllib
import os 
from pprint import pprint
import utils

class AppSettings():
"""
# 設定ファイル(toml)の取扱クラス

issue:  
* ファイルの有無による動作を定義できるようにしたい。
    * ファイルなしを許容するなら、デフォルト値を定義
    * ファイルなしを許容しないなら、その場で例外スロー
* globalな設定を前提とするため、singltonな形式で提供したい。
* validaterの実装が必要。
"""

    def __init__(self, settings_path:str=None):
        """

        Args:
            settings_path (str, optional): 設定ファイルパス。 Defaults to None.
        """

        # 設定ファイルのパスを指定
        self.settings_path = settings_path

        # 設定ファイルを読込
        self._load_settings()        

    @property
    def settings_raw(self) -> dict:
        """
        Returns:
            dict: 設定ファイル読込データの生データ
        """
        return self._settings

    @property
    def settings_path(self) -> str:
        """設定ファイルのパスを取得
            self.__settings_path is None ならデフォルトのパスを返す。

            default path:
                    <app_settings.py(this scripts) in dir>/../../config/settings.toml
        Returns:
            str: 設定ファイルのパス
        """

        # 設定ファイルのパスを設定
        ret = self.__settings_path

        # 設定ファイルのパス指定がなければ、デフォルトのパスを返す。
        if ret is None:
            ret = str(utils.get_root_path() / 'config' / 'settings.toml')

        return ret

    @property
    def settings_path(self) -> str:
        """設定ファイルのパスを取得  
            self.__settings_path is None ならデフォルトのパスを返す。

            * default path:  
                * <app_settings.py(this scripts) in dir>/../../config/settings.toml
        Returns:
            str: 設定ファイルのパス
        """

        # 設定ファイルのパスを設定
        ret = self.__settings_path

        # 設定ファイルのパス指定がなければ、デフォルトのパスを返す。
        if ret is None:
            ret = str(utils.get_root_path() / 'config' / 'settings.toml')

        return ret

    @property.setter
    def settings_path(self, value: str) -> str:
        """
        Args:
            value (str): 設定ファイルのパスを指定

        Returns:
            str: 設定ファイルのパス
        """

        if not os.path.exists(value):
            raise Error(f"指定されたパスは存在しません。> {value}")

        # 設定ファイルのパスを設定
        self.__settings_path = value

        return self.__settings_path

    def _load_settings(self) -> dict:
        """self.settings_path のパスに配置されている、
        設定ファイルをを読込んで、self.__settingsに設定

        Returns:
            dict: 設定ファイルデータ
        """

        path = self.settings_path
        with open(path, mode="rb") as f:
            self.settings = tomllib.load(f)

        return self.settings