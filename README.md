# 4d-plugin-get-localized-name

```4d
$folder:=Folder(fk desktop folder)
$name:=Get localized name($folder)
$file:=Folder(fk desktop folder).file("spreadsheet.xlsx")
$name:=Get localized name($file)
```

### macOS

```json
{
 "localizedName":"デスクトップ",
 "localizedTypeDescription ":"フォルダ"
}

{
 "localizedName":"spreadsheet.xlsx",
 "localizedTypeDescription":"Microsoft Excel Workbook (.xlsx)",
 "localizedDescription":"Office Open XMLスプレッドシート"
}
```

### Windows

```json
{
 "localizedName":"デスクトップ",
 "localizedTypeDescription ":"ファイル フォルダー"
}

{
 "localizedName":"spreadsheet.xlsx",
 "localizedTypeDescription":"XLSX ファイル"
 "localizedDescription":"XLSX ファイル"
}
```

