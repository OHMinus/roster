"""
@file main.py
@brief プログラムのエントリーポイントとコマンドライン引数の処理を行います。
@details CUI または GUI モードでプログラムを実行します。
"""
import sys
import datetime
import cui
import core
import withGui

def main():
    """
    @brief プログラムのメイン関数。
    @details コマンドライン引数を処理し、CUI または GUI モードでプログラムを実行します。
    """
    if(index_of(sys.argv, "-h") != -1 or index_of(sys.argv, "--help") != -1):
        print_help()
        sys.exit(1)

    if (index_of(sys.argv, "-c") != -1 or index_of(sys.argv, "--cui") != -1):
        if len(sys.argv) == 4:
            cui.Main(sys.argv[2], sys.argv[3])
        elif len(sys.argv) == 5:
            cui.Main(sys.argv[2], sys.argv[3], sys.argv[4])
        elif len(sys.argv) > 5:
            print("Usage: roster.exe -c [input_dir] [output_file] [output_file_encoding]")
            sys.exit(1)
    else:
        withGui.StartGUI()

def index_of(array:list, target):
    """
    @brief 配列内で指定された要素のインデックスを返します。
    @param array (list): 要素を検索する配列。
    @param target: 検索する要素。
    @return (int): 要素のインデックス。見つからない場合は -1。
    @details 配列を反復処理して、ターゲット要素の最初の出現箇所のインデックスを返します。
    """
    i = 0
    for item in array:
        if item == target:
            return i
        i = i + 1
    return -1

##
#@brief ヘルプメッセージを表示します。
#@details プログラムの使用方法とオプションを表示します。
def print_help():
    print("Usage: roster.exe [options] [input_dir] [output_file] [output_file_encoding]")
    print("List the data of application files as csv format.")
    print("Options:")
    print("  -h, --help      Show this help message and exit")
    print("  -c, --cui       Run in CUI mode (default is GUI)")

#子プロセスとして呼ばれてない時
if __name__ == "__main__":
    main()
