import os
import sys
import argparse
import shutil
from datetime import datetime, timedelta

def find_files_by_extension(folder_path, extensions, weeks=1):
    # フォルダ内のファイルを取得
    files = os.listdir(folder_path)

    # 指定した拡張子に合致するファイルを抽出して結果を格納するリスト
    matched_files = []
    
    # 今日の日付を取得
    today = datetime.now()

    for file in files:
        # ファイルのフルパスを取得
        file_path = os.path.join(folder_path, file)

        # ファイルかつ指定した拡張子に合致する場合、リストに追加
        if os.path.isfile(file_path) and file.endswith(tuple(extensions)):
            modified_time = os.path.getmtime(file_path)  # 更新日時を取得
            modified_time = datetime.fromtimestamp(modified_time)

            # 今日からX週間以内の場合、リストに追加
            if today - modified_time <= timedelta(weeks=weeks):
                formatted_time = modified_time.strftime('%Y年%m月%d日 %H:%M:%S')
                matched_files.append((file, formatted_time, folder_path+'\\'+file))

    return matched_files

def write_file_list(file_path, data_list):
    with open(file_path, 'w', encoding='utf-8-sig') as file:
        file.write(f"ファイルパス, 更新日時\n")
        for data in data_list:
            file.write(f'\"{data[2]}\",\"{data[1]}\"\n')

def write_copy_list(file_path, data_list):
    with open(file_path, 'w', encoding='utf-8-sig') as file:
        file.write(f"ファイル, 結果\n")
        for data in data_list:
            file.write(f'\"{data[0]}\",\"{data[1]}\"\n')

def copy_files(file_list, destination_dir):
    try:
        # コピー先ディレクトリが存在しない場合は作成する
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        result_list = []
        for file_path in file_list:
            # コピー元ファイルが存在するか確認する
            if not os.path.isfile(file_path):
                print(f"Error: ファイル '{file_path}' が存在しません。スキップします。")
                result_list.append((file_path,f"Error: ファイル '{file_path}' が存在しません。スキップします。"))
            else:
                # ファイルをコピーする準備
                file_name = os.path.basename(file_path)
                destination_path = os.path.join(destination_dir, file_name)

                # コピー先ディレクトリに同じファイルが存在するか確認する
                if os.path.exists(destination_path):
                    print(f"ファイル '{destination_path}' はすでに存在します。スキップします。")
                    result_list.append((file_name,f"ファイル '{destination_path}' はすでに存在します。スキップします。"))
                else:
                    # ファイルをコピーする（更新日時などの情報を保持したまま）
                    shutil.copy2(file_path, destination_path)
                    print(f"ファイル '{file_path}' を '{destination_path}' にコピーしました。")
                    result_list.append((file_name,f"ファイル '{file_path}' を '{destination_path}' にコピーしました。"))

        # 結果をtxtファイルに書き出す
        now = datetime.now()
        timestamp = now.strftime('%Y%m%d_%H%M%S')
        output_file_path = f"copy_list_{timestamp}.log"
        write_copy_list(output_file_path, result_list)
        print(f"\n結果が {output_file_path} に書き出されました。")
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")

def main(src_folder_path, extensions, weeks, dst_folder_path):
    # ファイル一覧と更新日時の一覧を取得
    matched_files = find_files_by_extension(src_folder_path, extensions, weeks)

    # 結果を表示
    if matched_files:
        src_file_path = []
        print('指定された拡張子に合致するファイル一覧と更新日時:')
        for file_info in matched_files:
            file_name, formatted_time , full_path = file_info
            print(f'{file_name} (更新日時: {formatted_time})')
            src_file_path.append(full_path)

        # 結果をtxtファイルに書き出す
        now = datetime.now()
        timestamp = now.strftime('%Y%m%d_%H%M%S')
        output_file_path = f"file_list_{timestamp}.log"

        # ファイルをコピーする        
        copy_files(src_file_path, dst_folder_path)

    else:
        print('該当するファイルが見つかりませんでした。')

if __name__ == '__main__':
    # 引数のパーサー用意
    parser = argparse.ArgumentParser()
    # 引数設定
    parser.add_argument('src_folder_path')
    parser.add_argument('extensions')
    parser.add_argument('weeks')
    parser.add_argument('dst_folder_path')
    # 引数取得
    args = parser.parse_args()

    if(len(vars(args))==4):
        main(
            args.src_folder_path,
            args.extensions.split(','),
            int(args.weeks),
            args.dst_folder_path,
        )
    else:
        main()
