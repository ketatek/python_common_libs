from pathlib import Path

from bin.common.utils import (
    get_root_path
)

def test_get_root_path():
    """utils.get_root_path() デコレーターのテスト
    """    

    # 検証対象のプロジェクトルートパスの取得
    path = get_root_path()

    # ログ出力のテスト
    assert path == Path(__file__).parent.parent.joinpath('bin')

