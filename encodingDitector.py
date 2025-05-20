"""
@file encodingDitector.py
@brief ファイルのエンコーディングを検出する関数を提供します。
@details UniversalDetector を使用してファイルのエンコーディングを判定します。
"""

from chardet.universaldetector import UniversalDetector

def encordingDItector(filepath):
    """
    @brief ファイルのエンコーディングを検出します。
    @param filepath (str): エンコーディングを検出するファイルのパス。
    @return (str): 検出されたエンコーディング。
    @details ファイルを読み込み、UniversalDetector でエンコーディングを判定します。
    """
    with open(filepath, 'rb') as f:  
        detector = UniversalDetector()
        for line in f:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result.get("encoding")